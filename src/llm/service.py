from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from ..logger import LoggerService

@dataclass
class LLMResponse:
    """Ответ от LLM модели"""
    text: str
    metadata: Dict[str, Any]

class LLMService(ABC, LoggerService):
    """Абстрактный класс для LLM сервисов"""
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        context: Optional[List[str]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> LLMResponse:
        """Генерирует ответ на основе промпта и контекста"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Проверяет доступность модели"""
        pass