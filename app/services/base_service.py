"""
BaseService - Base class cho tất cả Services
Chứa business logic và gọi Model operations
"""
from typing import List, Dict, Any, Optional, Type

from app.models.base import BaseModel


class BaseService:
    """Base Service với business logic helpers"""

    model: Type[BaseModel] = None

    @classmethod
    def get_all(cls, order_by: str = None) -> List[Dict[str, Any]]:
        """Lấy tất cả records"""
        return cls.model.all(order_by=order_by)

    @classmethod
    def get_by_id(cls, pk_value: Any) -> Optional[Dict[str, Any]]:
        """Lấy record theo ID"""
        return cls.model.find(pk_value)

    @classmethod
    def get_where(cls, conditions: Dict[str, Any], order_by: str = None) -> List[Dict[str, Any]]:
        """Lấy records theo điều kiện"""
        return cls.model.where(conditions, order_by=order_by)

    @classmethod
    def create(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Tạo record mới"""
        return cls.model.create(data)

    @classmethod
    def update(cls, pk_value: Any, data: Dict[str, Any]) -> Dict[str, Any]:
        """Cập nhật record"""
        return cls.model.update(pk_value, data)

    @classmethod
    def delete(cls, pk_value: Any) -> bool:
        """Xóa record"""
        return cls.model.delete(pk_value)

    @classmethod
    def exists(cls, pk_value: Any) -> bool:
        """Kiểm tra tồn tại"""
        return cls.model.exists(pk_value)

    @classmethod
    def count(cls, conditions: Dict[str, Any] = None) -> int:
        """Đếm records"""
        return cls.model.count(conditions)

    @classmethod
    def paginate(cls, page: int = 1, per_page: int = 20, order_by: str = None) -> Dict[str, Any]:
        """Phân trang"""
        offset = (page - 1) * per_page
        records = cls.model.raw_query(
            f"SELECT * FROM {cls.model.table_name} ORDER BY {order_by or cls.model.primary_key} LIMIT %s OFFSET %s",
            (per_page, offset)
        )
        total = cls.count()
        return {
            "data": records,
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page
        }
