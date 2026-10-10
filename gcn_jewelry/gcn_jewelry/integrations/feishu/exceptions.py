class FeishuError(Exception):
    "Raised when a Feishu API request fails."


class FeishuConfigurationError(FeishuError):
    "Raised when site configuration is incomplete."
