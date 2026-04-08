"""
QuanTri Model - Bảng quan_tri (Admin)
"""
import json
import os
from app.models.base import BaseModel

_QDBG = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "debug-722d3f.log")

def _qdbg(msg, data):
    try:
        with open(_QDBG, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "sessionId": "722d3f", "location": "models/quan_tri.py",
                "message": msg, "data": data, "runId": "run1", "hypothesisId": "H1;H3"
            }, ensure_ascii=False) + "\n")
    except Exception:
        pass


class QuanTri(BaseModel):
    table_name = "quan_tri"
    primary_key = "ma_qt"

    @classmethod
    def find_by_username(cls, ten_dn: str):
        """Tìm admin theo tên đăng nhập (email)"""
        _qdbg("find_by_username:QUERY", {"ten_dn": ten_dn, "table": cls.table_name})
        result = cls.raw_query(
            "SELECT * FROM quan_tri WHERE email = %s",
            (ten_dn,),
            fetch_one=True
        )
        _qdbg("find_by_username:RESULT",
              {"found": result is not None,
               "cols": list(result.keys()) if result else None,
               "db_row": {k: (v if k != "password_hash" else "***") for k, v in result.items()} if result else None})
        return result

    @classmethod
    def get_thong_bao_by_admin(cls, ma_admin: str):
        """Lấy thông báo do admin tạo"""
        return cls.raw_query(
            "SELECT * FROM thong_bao WHERE ma_admin = %s",
            (ma_admin,)
        )
