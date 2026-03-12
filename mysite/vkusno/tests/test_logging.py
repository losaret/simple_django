import logging
from django.test import TestCase


class LoggingTestCase(TestCase):
    
    def test_logging_messages(self):
        """Тестирование логирования"""
        logger = logging.getLogger('django')
        
        with self.assertLogs('django', level='INFO') as cm:
            logger.info("Test info message")
            logger.warning("Test warning message")
            
        # Проверяем, что логи были записаны
        self.assertEqual(len(cm.output), 2)
        self.assertIn('Test info message', cm.output[0])
        self.assertIn('Test warning message', cm.output[1])