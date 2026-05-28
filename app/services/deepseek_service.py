from openai import OpenAI

from app.core.config import settings


class DeepSeekService:
    def __init__(self) -> None:
        if not settings.deepseek_api_key:
            self.client = None
            return

        self.client = OpenAI(
            api_key=settings.deepseek_api_key,
            base_url=settings.deepseek_base_url,
        )

    def is_configured(self) -> bool:
        return self.client is not None


deepseek_service = DeepSeekService()
