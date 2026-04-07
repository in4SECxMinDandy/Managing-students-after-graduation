"""API Client for QLSVSDH Backend.

Reuses the authentication and request logic from the Streamlit frontend.
Token is stored in memory only (never in localStorage) for security.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any

import requests


API_BASE = os.environ.get("QLSVSDH_API_BASE", "http://localhost:8000")


@dataclass
class ApiResult:
    """Result of an API call.

    Attributes:
        data: The response data (list or dict) on success, None on failure.
        error: Error message string, or None on success.
    """
    data: dict | list | None = None
    error: str | None = None


class ApiClient:
    """HTTP client for the QLSVSDH backend API.

    All methods return ApiResult to keep error handling explicit and consistent.
    The token is stored in memory only — never written to disk or localStorage.
    """

    def __init__(self, base_url: str = API_BASE) -> None:
        self._base_url = base_url.rstrip("/")
        self._token: str | None = None

    @property
    def token(self) -> str | None:
        return self._token

    @token.setter
    def token(self, value: str | None) -> None:
        self._token = value

    def clear_token(self) -> None:
        self._token = None

    def _headers(self) -> dict[str, str]:
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    def login(self, username: str, password: str) -> ApiResult:
        """Authenticate user and store access token.

        Args:
            username: Login username or email.
            password: User password.

        Returns:
            ApiResult with user data dict on success, or error string on failure.
        """
        try:
            resp = requests.post(
                f"{self._base_url}/auth/login",
                json={"username": username, "password": password},
                timeout=10,
            )
            if resp.status_code == 200:
                payload = resp.json()
                self._token = payload.get("access_token")
                return ApiResult(data=payload, error=None)
            return ApiResult(data=None, error="Sai tên đăng nhập hoặc mật khẩu")
        except requests.exceptions.ConnectionError:
            return ApiResult(
                data=None,
                error=f"Không kết nối được API tại {self._base_url}. Hãy chắc chắn backend đang chạy.",
            )
        except requests.exceptions.Timeout:
            return ApiResult(data=None, error="API phản hồi quá lâu (timeout).")
        except Exception as exc:  # pragma: no-cover
            return ApiResult(data=None, error=str(exc))

    def get(self, path: str, params: dict | None = None) -> ApiResult:
        """Perform GET request.

        Args:
            path: API path (e.g. "/admissions/profiles").
            params: Optional query parameters.

        Returns:
            ApiResult with response data on 200, or error string otherwise.
        """
        try:
            resp = requests.get(
                f"{self._base_url}{path}",
                headers=self._headers(),
                params=params or {},
                timeout=10,
            )
            if resp.status_code == 200:
                return ApiResult(data=resp.json(), error=None)
            if resp.status_code == 401:
                self.clear_token()
                return ApiResult(data=None, error="Phiên đăng nhập hết hạn. Vui lòng đăng nh���p lại.")
            return ApiResult(data=None, error=f"Yêu cầu thất bại (HTTP {resp.status_code})")
        except Exception as exc:  # pragma: no-cover
            return ApiResult(data=None, error=str(exc))

    def post(self, path: str, data: dict) -> ApiResult:
        """Perform POST request.

        Args:
            path: API path (e.g. "/training/enrollments").
            data: JSON request body.

        Returns:
            ApiResult with response data on 200/201, or error string otherwise.
        """
        try:
            resp = requests.post(
                f"{self._base_url}{path}",
                headers=self._headers(),
                json=data,
                timeout=10,
            )
            if resp.status_code in (200, 201):
                return ApiResult(data=resp.json(), error=None)
            if resp.status_code == 401:
                self.clear_token()
                return ApiResult(data=None, error="Phiên đăng nhập hết hạn. Vui lòng đăng nhập lại.")
            return ApiResult(data=None, error=f"Yêu cầu thất bại (HTTP {resp.status_code})")
        except Exception as exc:  # pragma: no-cover
            return ApiResult(data=None, error=str(exc))

    def put(self, path: str, data: dict) -> ApiResult:
        """Perform PUT request.

        Args:
            path: API path.
            data: JSON request body.

        Returns:
            ApiResult with response data on 200, or error string otherwise.
        """
        try:
            resp = requests.put(
                f"{self._base_url}{path}",
                headers=self._headers(),
                json=data,
                timeout=10,
            )
            if resp.status_code == 200:
                return ApiResult(data=resp.json(), error=None)
            if resp.status_code == 401:
                self.clear_token()
                return ApiResult(data=None, error="Phiên đăng nhập hết hạn. Vui lòng đăng nhập lại.")
            return ApiResult(data=None, error=f"Yêu cầu thất bại (HTTP {resp.status_code})")
        except Exception as exc:  # pragma: no-cover
            return ApiResult(data=None, error=str(exc))

    def is_authenticated(self) -> bool:
        """Check if a valid token is held in memory."""
        return self._token is not None