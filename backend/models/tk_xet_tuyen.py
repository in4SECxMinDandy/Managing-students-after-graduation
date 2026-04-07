"""TK_XetTuyen model - Tài khoản xét tuyển."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class TKXetTuyen(BaseTable):
    """Bảng Tài khoản Xét tuyển."""

    __tablename__ = "TK_XetTuyen"

    MaTK: Mapped[str] = mapped_column(String(10), primary_key=True)
    Email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    MatKhau: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationships
    hso: Mapped["HSOXetTuyen"] = relationship("HSOXetTuyen", back_populates="tai_khoan", uselist=False)

    def __repr__(self) -> str:
        return f"<TKXetTuyen(MaTK={self.MaTK}, Email={self.Email})>"


from backend.models.hso_xet_tuyen import HSOXetTuyen
