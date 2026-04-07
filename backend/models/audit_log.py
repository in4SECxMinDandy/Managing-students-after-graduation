"""AuditLog model."""
from sqlalchemy import BigInteger, DateTime, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class AuditLog(Base):
    """Bảng Audit Log."""

    __tablename__ = "AuditLog"

    MaAudit: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    UserId: Mapped[str | None] = mapped_column(String(15), default=None)
    UserType: Mapped[str | None] = mapped_column(String(20), default=None)
    Action: Mapped[str] = mapped_column(String(10), nullable=False)
    TableName: Mapped[str] = mapped_column(String(50), nullable=False)
    RecordId: Mapped[str | None] = mapped_column(String(15), default=None)
    OldData: Mapped[dict | None] = mapped_column(JSON, default=None)
    NewData: Mapped[dict | None] = mapped_column(JSON, default=None)
    IpAddress: Mapped[str | None] = mapped_column(String(45), default=None)
    UserAgent: Mapped[str | None] = mapped_column(String(500), default=None)
    created_at: Mapped[dict] = mapped_column(DateTime, default=lambda: None)

    def __repr__(self) -> str:
        return f"<AuditLog(MaAudit={self.MaAudit}, Action={self.Action}, TableName={self.TableName})>"
