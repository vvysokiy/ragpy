from langchain_ollama import OllamaLLM
from typing import List, Optional

from src.llm.service import LLMService, LLMResponse

class Qwen8BInstructLLM(LLMService):
    """LLM сервис на основе Qwen-8B-Instruct через Ollama"""

    _llm: Optional[OllamaLLM] = None
    
    def __init__(
        self,
        model: str,
        host: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ):
        """
        Инициализация Qwen LLM
        
        Args:
            model: Название модели (если None, берется из конфига)
            host: URL Ollama сервера (если None, берется из конфига)
            temperature: Температура генерации
            max_tokens: Максимальное количество токенов
        """
        self.model = model
        self.host = host
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        try:
            self._llm = OllamaLLM(
                model=self.model,
                base_url=self.host,
                temperature=self.temperature,
                num_ctx=self.max_tokens,
                # Дополнительные параметры, специфичные для Ollama
                # stop=["<|im_end|>"],  # Специальный токен для Qwen
                # top_k=40,
                # top_p=0.9,
                # repeat_penalty=1.1
            )

            self._logger_info(f"Qwen LLM инициализирован с моделью: {self.model}")
        except Exception as e:
            self._logger_error(f"Ошибка инициализации Qwen LLM: {e}")
            self._llm = None
    
    def is_available(self) -> bool:
        """Проверяет доступность модели"""
        return self._llm is not None
    
    def generate(
        self,
        prompt: str,
        context: Optional[List[str]] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> LLMResponse:
        """
        Генерирует ответ на основе промпта и контекста
        
        Args:
            prompt: Основной промпт
            context: Список контекстных фрагментов
            temperature: Переопределение температуры
            max_tokens: Переопределение максимального количества токенов
        """
        if not self.is_available():
            raise RuntimeError("LLM сервис недоступен")
        
        # Формируем полный промпт с контекстом
        full_prompt = prompt
        if context:
            context_text = "\n\n".join(context)
            full_prompt = f"Контекст:\n{context_text}\n\nВопрос:\n{prompt}\n\nОтвет:"
        
        try:
            # Генерируем ответ
            response = self._llm.invoke(
                full_prompt,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens
            )
            
            metadata = {
                "model": self.model,
                "temperature": temperature or self.temperature,
                "max_tokens": max_tokens or self.max_tokens,
                "context_chunks": len(context) if context else 0
            }
            
            return LLMResponse(
                text=response,
                metadata=metadata
            )
            
        except Exception as e:
            self._logger_error(f"Ошибка генерации ответа: {e}")
            raise
