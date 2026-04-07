"""Seed script to create initial admin user and sample data."""
import asyncio

from backend.database.engine import async_session_factory
from backend.models.all_models import QuanTri
from backend.utils.hash import hash_password


async def seed_admin():
    """Create default admin user."""
    async with async_session_factory() as session:
        # Check if admin already exists
        from sqlalchemy import select
        result = await session.execute(select(QuanTri).where(QuanTri.TenDN == "admin"))
        existing = result.scalar_one_or_none()
        if existing:
            print("Admin already exists, skipping.")
            return

        admin = QuanTri(
            MaAdmin="ADMIN001",
            TenDN="admin",
            MatKhau=hash_password("admin123"),
            HoTen="Quản trị viên",
            Email="admin@qlsvsdh.edu.vn",
            VaiTro="admin",
        )
        session.add(admin)
        await session.commit()
        print("Admin created: admin / admin123")


if __name__ == "__main__":
    asyncio.run(seed_admin())
