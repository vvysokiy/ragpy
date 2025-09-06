from .logger import logger

class LoggerService:
    def _logger_info(self, message: str):
        """
        Логирует информационное сообщение с указанием имени класса.

        Args:
            message (str): Сообщение для логирования.
        """
        name = self.__class__.__name__
        logger.info("[%s] %s", name, message)

    def _logger_error(self, message: str):
        """
        Логирует сообщение об ошибке с указанием имени класса.

        Args:
            message (str): Сообщение об ошибке для логирования.
        """
        name = self.__class__.__name__
        logger.error("[%s] %s", name, message)

    def _logger_warning(self, message: str):
        """
        Логирует сообщение о предупреждении с указанием имени класса.

        Args:
            message (str): Сообщение о предупреждении для логирования.
        """
        name = self.__class__.__name__
        logger.warning("[%s] %s", name, message)