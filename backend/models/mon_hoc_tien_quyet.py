"""MonHocTienQuyet model."""
from sqlalchemy import ForeignKey, String, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class MonHocTienQuyet(Base):
    """Bảng Môn học Tiên quyết."""

    __tablename__ = "MonHocTienQuyet"

    MaMH: Mapped[str] = mapped_column(String(10), ForeignKey("MonHoc.MaMH", ondelete="CASCADE"), primary_key=True)
    MaMHTienQuyet: Mapped[str] = mapped_column(String(10), ForeignKey("MonHoc.MaMH", ondelete="CASCADE"), primary_key=True)
    MoTa: Mapped[str | None] = mapped_column(String, default=None)

    def __repr__(self) -> str:
        return f"<MonHocTienQuyet(MaMH={self.MaMH}, MaMHTienQuyet={self.MaMHTienQuyet})>"
