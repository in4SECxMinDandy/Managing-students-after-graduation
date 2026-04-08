"""
QLSVSDH Configuration
Cấu hình kết nối MySQL và JWT settings
"""
import os


class Config:
    """Cấu hình ứng dụng"""

    # MySQL Connection (XAMPP)
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "qlsvsdh")

    # JWT Settings
    JWT_SECRET = os.getenv("JWT_SECRET", "qlsvsdh-secret-key-change-in-production")
    JWT_ALGORITHM = "HS256"
    JWT_EXPIRY_HOURS = 24

    # API Settings
    API_PREFIX = "/api"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
