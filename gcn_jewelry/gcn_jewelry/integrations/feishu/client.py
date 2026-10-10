from __future__ import annotations

import requests

from .exceptions import FeishuConfigurationError, FeishuError

TOKEN_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
BITABLE_URL = "https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"


class FeishuClient:
    def __init__(self, app_id=None, app_secret=None, timeout=30):
        if not app_id or not app_secret:
            raise FeishuConfigurationError("Feishu app_id and app_secret are required")
        self.app_id = app_id
        self.app_secret = app_secret
        self.timeout = timeout
        self._token = None

    def tenant_access_token(self) -> str:
        if self._token:
            return self._token
        response = requests.post(
            TOKEN_URL,
            json={"app_id": self.app_id, "app_secret": self.app_secret},
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("code") not in (None, 0):
            raise FeishuError(payload.get("msg", "Feishu token request failed"))
        self._token = payload["tenant_access_token"]
        return self._token

    def list_records(self, app_token: str, table_id: str, page_token=None, page_size=500) -> dict:
        params = {"page_size": page_size}
        if page_token:
            params["page_token"] = page_token
        response = requests.get(
            BITABLE_URL.format(app_token=app_token, table_id=table_id),
            params=params,
            headers={"Authorization": f"Bearer {self.tenant_access_token()}"},
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("code") not in (None, 0):
            raise FeishuError(payload.get("msg", "Feishu records request failed"))
        return payload.get("data", {})
