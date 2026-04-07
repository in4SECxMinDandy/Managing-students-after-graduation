"""Authentication and authorization service."""
from typing import Literal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.all_models import GiangVien, QuanTri, SinhVien
from backend.schemas.auth import (
    GiangVienCreate,
    GiangVienUpdate,
    QuanTriCreate,
    QuanTriUpdate,
    SinhVienCreate,
    SinhVienUpdate,
)
from backend.utils.hash import create_access_token, create_refresh_token, hash_password, verify_password


class AuthService:
    """Service for authentication operations."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def login(self, username: str, password: str) -> dict | None:
        """
        Authenticate user by username (TenDN for admin, Email for SV/GV) and password.
        Returns token data or None if authentication fails.
        """
        # Try admin first
        result = await self.session.execute(
            select(QuanTri).where(
                QuanTri.TenDN == username,
                QuanTri.is_active == True,  # noqa: E712
            )
        )
        admin = result.scalar_one_or_none()
        if admin and verify_password(password, admin.MatKhau):
            token = create_access_token({
                "user_id": admin.MaAdmin,
                "role": admin.VaiTro,
                "user_type": "admin",
            })
            refresh = create_refresh_token({"user_id": admin.MaAdmin, "role": admin.VaiTro})
            return {
                "access_token": token,
                "refresh_token": refresh,
                "token_type": "bearer",
                "user_id": admin.MaAdmin,
                "ho_ten": admin.HoTen,
                "role": admin.VaiTro,
            }

        # Try student
        result = await self.session.execute(
            select(SinhVien).where(
                SinhVien.Email == username,
                SinhVien.is_active == True,  # noqa: E712
            )
        )
        sv = result.scalar_one_or_none()
        if sv and verify_password(password, sv.MatKhau):
            token = create_access_token({
                "user_id": sv.MaSV,
                "role": "sinhvien",
                "user_type": "sinhvien",
            })
            refresh = create_refresh_token({"user_id": sv.MaSV, "role": "sinhvien"})
            return {
                "access_token": token,
                "refresh_token": refresh,
                "token_type": "bearer",
                "user_id": sv.MaSV,
                "ho_ten": sv.HoTen,
                "role": "sinhvien",
            }

        # Try lecturer
        result = await self.session.execute(
            select(GiangVien).where(
                GiangVien.Email == username,
                GiangVien.is_active == True,  # noqa: E712
            )
        )
        gv = result.scalar_one_or_none()
        if gv and verify_password(password, gv.MatKhau):
            token = create_access_token({
                "user_id": gv.MaGV,
                "role": "giangvien",
                "user_type": "giangvien",
            })
            refresh = create_refresh_token({"user_id": gv.MaGV, "role": "giangvien"})
            return {
                "access_token": token,
                "refresh_token": refresh,
                "token_type": "bearer",
                "user_id": gv.MaGV,
                "ho_ten": gv.HoTen,
                "role": "giangvien",
            }

        return None


class AdminService:
    """Service for admin user management."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: QuanTriCreate) -> QuanTri:
        """Create a new admin user."""
        admin = QuanTri(
            MaAdmin=data.MaAdmin,
            TenDN=data.TenDN,
            MatKhau=hash_password(data.MatKhau),
            HoTen=data.HoTen,
            Email=data.Email,
            SDT=data.SDT,
            VaiTro=data.VaiTro,
        )
        self.session.add(admin)
        await self.session.flush()
        await self.session.refresh(admin)
        return admin

    async def get_by_id(self, ma_admin: str) -> QuanTri | None:
        """Get admin by MaAdmin."""
        result = await self.session.execute(
            select(QuanTri).where(
                QuanTri.MaAdmin == ma_admin,
                QuanTri.is_active == True,  # noqa: E712
            )
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[QuanTri]:
        """Get all active admins."""
        result = await self.session.execute(
            select(QuanTri)
            .where(QuanTri.is_active == True)  # noqa: E712
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def update(self, ma_admin: str, data: QuanTriUpdate) -> QuanTri | None:
        """Update an admin."""
        admin = await self.get_by_id(ma_admin)
        if not admin:
            return None
        update_data = data.model_dump(exclude_unset=True)
        if "MatKhau" in update_data and update_data["MatKhau"]:
            update_data["MatKhau"] = hash_password(update_data["MatKhau"])
        for key, value in update_data.items():
            if hasattr(admin, key):
                setattr(admin, key, value)
        await self.session.flush()
        await self.session.refresh(admin)
        return admin

    async def delete(self, ma_admin: str) -> bool:
        """Soft delete an admin."""
        admin = await self.get_by_id(ma_admin)
        if not admin:
            return False
        admin.is_active = False
        await self.session.flush()
        return True


class SinhVienService:
    """Service for student management."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: SinhVienCreate) -> SinhVien:
        """Create a new student."""
        sv = SinhVien(
            MaSV=data.MaSV,
            HoTen=data.HoTen,
            NgaySinh=data.NgaySinh,
            GioiTinh=data.GioiTinh,
            Email=data.Email,
            MatKhau=hash_password(data.MatKhau),
            MaLop=data.MaLop,
            HeDaoTao=data.HeDaoTao,
            QueQuan=data.QueQuan,
            NoiSinh=data.NoiSinh,
            DanToc=data.DanToc,
            DiaChi=data.DiaChi,
            SDT=data.SDT,
            CCCD=data.CCCD,
        )
        self.session.add(sv)
        await self.session.flush()
        await self.session.refresh(sv)
        return sv

    async def get_by_id(self, ma_sv: str) -> SinhVien | None:
        """Get student by MaSV."""
        result = await self.session.execute(
            select(SinhVien).where(
                SinhVien.MaSV == ma_sv,
                SinhVien.is_active == True,  # noqa: E712
            )
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> SinhVien | None:
        """Get student by email."""
        result = await self.session.execute(
            select(SinhVien).where(
                SinhVien.Email == email,
                SinhVien.is_active == True,  # noqa: E712
            )
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[SinhVien]:
        """Get all active students."""
        result = await self.session.execute(
            select(SinhVien)
            .where(SinhVien.is_active == True)  # noqa: E712
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def update(self, ma_sv: str, data: SinhVienUpdate) -> SinhVien | None:
        """Update a student."""
        sv = await self.get_by_id(ma_sv)
        if not sv:
            return None
        update_data = data.model_dump(exclude_unset=True)
        if "MatKhau" in update_data and update_data["MatKhau"]:
            update_data["MatKhau"] = hash_password(update_data["MatKhau"])
        for key, value in update_data.items():
            if hasattr(sv, key):
                setattr(sv, key, value)
        await self.session.flush()
        await self.session.refresh(sv)
        return sv

    async def delete(self, ma_sv: str) -> bool:
        """Soft delete a student."""
        sv = await self.get_by_id(ma_sv)
        if not sv:
            return False
        sv.is_active = False
        await self.session.flush()
        return True


class GiangVienService:
    """Service for lecturer management."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, data: GiangVienCreate) -> GiangVien:
        """Create a new lecturer."""
        gv = GiangVien(
            MaGV=data.MaGV,
            HoTen=data.HoTen,
            Email=data.Email,
            SDT=data.SDT,
            HocVi=data.HocVi,
            HocHam=data.HocHam,
            ChuyenNganh=data.ChuyenNganh,
            DiaChi=data.DiaChi,
            MaKhoa=data.MaKhoa,
            MatKhau=hash_password(data.MatKhau),
        )
        self.session.add(gv)
        await self.session.flush()
        await self.session.refresh(gv)
        return gv

    async def get_by_id(self, ma_gv: str) -> GiangVien | None:
        """Get lecturer by MaGV."""
        result = await self.session.execute(
            select(GiangVien).where(
                GiangVien.MaGV == ma_gv,
                GiangVien.is_active == True,  # noqa: E712
            )
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> GiangVien | None:
        """Get lecturer by email."""
        result = await self.session.execute(
            select(GiangVien).where(
                GiangVien.Email == email,
                GiangVien.is_active == True,  # noqa: E712
            )
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[GiangVien]:
        """Get all active lecturers."""
        result = await self.session.execute(
            select(GiangVien)
            .where(GiangVien.is_active == True)  # noqa: E712
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())

    async def update(self, ma_gv: str, data: GiangVienUpdate) -> GiangVien | None:
        """Update a lecturer."""
        gv = await self.get_by_id(ma_gv)
        if not gv:
            return None
        update_data = data.model_dump(exclude_unset=True)
        if "MatKhau" in update_data and update_data["MatKhau"]:
            update_data["MatKhau"] = hash_password(update_data["MatKhau"])
        for key, value in update_data.items():
            if hasattr(gv, key):
                setattr(gv, key, value)
        await self.session.flush()
        await self.session.refresh(gv)
        return gv

    async def delete(self, ma_gv: str) -> bool:
        """Soft delete a lecturer."""
        gv = await self.get_by_id(ma_gv)
        if not gv:
            return False
        gv.is_active = False
        await self.session.flush()
        return True
