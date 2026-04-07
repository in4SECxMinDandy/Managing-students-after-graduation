"""Auth API router."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.engine import get_db
from backend.middleware.security import CurrentUser, require_admin, require_all
from backend.schemas.auth import (
    GiangVienCreate,
    GiangVienResponse,
    GiangVienUpdate,
    LoginRequest,
    QuanTriCreate,
    QuanTriResponse,
    QuanTriUpdate,
    RefreshRequest,
    RefreshResponse,
    SinhVienCreate,
    SinhVienResponse,
    SinhVienUpdate,
    TokenResponse,
)
from apps.auth.service import AdminService, AuthService, GiangVienService, SinhVienService
from backend.utils.hash import create_access_token, decode_token

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer(auto_error=False)


# ---- Login ----
@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TokenResponse:
    """Authenticate user and return JWT tokens."""
    service = AuthService(db)
    result = await service.login(data.username, data.password)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return TokenResponse(**result)


@router.post("/refresh", response_model=RefreshResponse)
async def refresh_token(data: RefreshRequest) -> RefreshResponse:
    """Refresh access token using refresh token."""
    payload = decode_token(data.refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    new_token = create_access_token({
        "user_id": payload["user_id"],
        "role": payload["role"],
        "user_type": payload.get("user_type", "admin"),
    })
    return RefreshResponse(access_token=new_token)


# ---- Admin Users ----
@router.post("/admins", response_model=QuanTriResponse, dependencies=[Depends(require_admin)])
async def create_admin(
    data: QuanTriCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> QuanTriResponse:
    """Create a new admin user (admin only)."""
    service = AdminService(db)
    admin = await service.create(data)
    return QuanTriResponse.model_validate(admin)


@router.get("/admins", response_model=list[QuanTriResponse], dependencies=[Depends(require_admin)])
async def list_admins(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[QuanTriResponse]:
    """List all admin users (admin only)."""
    service = AdminService(db)
    admins = await service.get_all(skip=skip, limit=limit)
    return [QuanTriResponse.model_validate(a) for a in admins]


@router.get("/admins/{ma_admin}", response_model=QuanTriResponse, dependencies=[Depends(require_admin)])
async def get_admin(
    ma_admin: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> QuanTriResponse:
    """Get admin by MaAdmin."""
    service = AdminService(db)
    admin = await service.get_by_id(ma_admin)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return QuanTriResponse.model_validate(admin)


@router.put("/admins/{ma_admin}", response_model=QuanTriResponse, dependencies=[Depends(require_admin)])
async def update_admin(
    ma_admin: str,
    data: QuanTriUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> QuanTriResponse:
    """Update admin user."""
    service = AdminService(db)
    admin = await service.update(ma_admin, data)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return QuanTriResponse.model_validate(admin)


@router.delete("/admins/{ma_admin}", status_code=204, dependencies=[Depends(require_admin)])
async def delete_admin(
    ma_admin: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """Soft delete admin user."""
    service = AdminService(db)
    success = await service.delete(ma_admin)
    if not success:
        raise HTTPException(status_code=404, detail="Admin not found")


# ---- Students ----
@router.post("/students", response_model=SinhVienResponse, dependencies=[Depends(require_admin)])
async def create_student(
    data: SinhVienCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SinhVienResponse:
    """Create a new student (admin only)."""
    service = SinhVienService(db)
    existing = await service.get_by_email(data.Email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    sv = await service.create(data)
    return SinhVienResponse.model_validate(sv)


@router.get("/students", response_model=list[SinhVienResponse], dependencies=[Depends(require_all)])
async def list_students(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[SinhVienResponse]:
    """List all students."""
    service = SinhVienService(db)
    students = await service.get_all(skip=skip, limit=limit)
    return [SinhVienResponse.model_validate(s) for s in students]


@router.get("/students/{ma_sv}", response_model=SinhVienResponse, dependencies=[Depends(require_all)])
async def get_student(
    ma_sv: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SinhVienResponse:
    """Get student by MaSV."""
    service = SinhVienService(db)
    sv = await service.get_by_id(ma_sv)
    if not sv:
        raise HTTPException(status_code=404, detail="Student not found")
    return SinhVienResponse.model_validate(sv)


@router.put("/students/{ma_sv}", response_model=SinhVienResponse, dependencies=[Depends(require_all)])
async def update_student(
    ma_sv: str,
    data: SinhVienUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> SinhVienResponse:
    """Update student."""
    service = SinhVienService(db)
    sv = await service.update(ma_sv, data)
    if not sv:
        raise HTTPException(status_code=404, detail="Student not found")
    return SinhVienResponse.model_validate(sv)


@router.delete("/students/{ma_sv}", status_code=204, dependencies=[Depends(require_admin)])
async def delete_student(
    ma_sv: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """Soft delete student."""
    service = SinhVienService(db)
    success = await service.delete(ma_sv)
    if not success:
        raise HTTPException(status_code=404, detail="Student not found")


# ---- Lecturers ----
@router.post("/lecturers", response_model=GiangVienResponse, dependencies=[Depends(require_admin)])
async def create_lecturer(
    data: GiangVienCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> GiangVienResponse:
    """Create a new lecturer (admin only)."""
    service = GiangVienService(db)
    existing = await service.get_by_email(data.Email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    gv = await service.create(data)
    return GiangVienResponse.model_validate(gv)


@router.get("/lecturers", response_model=list[GiangVienResponse], dependencies=[Depends(require_all)])
async def list_lecturers(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[GiangVienResponse]:
    """List all lecturers."""
    service = GiangVienService(db)
    lecturers = await service.get_all(skip=skip, limit=limit)
    return [GiangVienResponse.model_validate(g) for g in lecturers]


@router.get("/lecturers/{ma_gv}", response_model=GiangVienResponse, dependencies=[Depends(require_all)])
async def get_lecturer(
    ma_gv: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> GiangVienResponse:
    """Get lecturer by MaGV."""
    service = GiangVienService(db)
    gv = await service.get_by_id(ma_gv)
    if not gv:
        raise HTTPException(status_code=404, detail="Lecturer not found")
    return GiangVienResponse.model_validate(gv)


@router.put("/lecturers/{ma_gv}", response_model=GiangVienResponse, dependencies=[Depends(require_all)])
async def update_lecturer(
    ma_gv: str,
    data: GiangVienUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> GiangVienResponse:
    """Update lecturer."""
    service = GiangVienService(db)
    gv = await service.update(ma_gv, data)
    if not gv:
        raise HTTPException(status_code=404, detail="Lecturer not found")
    return GiangVienResponse.model_validate(gv)


@router.delete("/lecturers/{ma_gv}", status_code=204, dependencies=[Depends(require_admin)])
async def delete_lecturer(
    ma_gv: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> None:
    """Soft delete lecturer."""
    service = GiangVienService(db)
    success = await service.delete(ma_gv)
    if not success:
        raise HTTPException(status_code=404, detail="Lecturer not found")
