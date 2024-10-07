"""Модуль с настройками OpenAI"""

import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

OPENAI_API_KEY = os.getenv('OpenAI_API_KEY')
OPENAI_ORGANIZATION = os.getenv('OpenAI_ORGANIZATION')
OPENAI_PROXY = os.getenv('OpenAI_PROXY')

OPENAI_MODEL = 'gpt-3.5-turbo'  # 'text-davinci-002' 'text-davinci-003'
OPENAI_TIMEOUT = 45

INVITATION = 'Напиши развёрнутый и обоснованный ответ на вопрос:'
ASSISTANT_PROMPT = "Отвечай честно, простым и понятным Русским языком"
DEFAULT_AI_ANSWER = 'При формировании ответа произошла ошибка'
