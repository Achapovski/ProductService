import os


class BaseSettingsConfigMixin:
    model_config = {
        "env_file": os.getenv("ENV_FILE", ".env")
    }
