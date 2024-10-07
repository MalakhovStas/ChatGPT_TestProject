"""Модуль инструментов для взаимодействия с библиотекой и сервисом OpenAI"""
import asyncio
from typing import Optional, List

from httpx import AsyncClient
from openai import AsyncOpenAI, APIError
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice

import config


class OpenAIManager:
    """ Класс для работы с API ChatGPT """

    def __init__(self):
        self.openai = AsyncOpenAI(
            api_key=config.OPENAI_API_KEY,
            organization=config.OPENAI_ORGANIZATION,
            http_client=AsyncClient(proxy=config.OPENAI_PROXY)
        )

    async def some_question(
            self,
            prompt: str,
            messages_data: Optional[List] = None,
    ) -> Optional[str]:
        """Основной метод осуществления запросов к ChatGPT"""
        answer = None
        if await self._check_type_str(prompt):
            if config.OPENAI_MODEL == 'gpt-3.5-turbo':
                answer = await self.answer_gpt_3_5_turbo(
                    prompt=prompt,
                    correct=False,
                    messages_data=messages_data,
                )
        return answer

    @staticmethod
    async def _check_type_str(*args) -> bool:
        return all((isinstance(arg, str) for arg in args))

    @staticmethod
    async def prompt_correct(text: str) -> str:
        """Для корректировки входящего запроса, в конце обязательно должна стоять точка,
        иначе модель ИИ пытается продолжить текст, а не ответить на него"""
        text = text.strip()
        if not text.endswith('.'):
            text += '.'
        return f'{config.INVITATION} {text}'

    async def answer_gpt_3_5_turbo(
            self,
            prompt: str,
            correct: bool = True,
            messages_data: Optional[List] = None,
    ) -> str:
        """ Запрос к ChatGPT модель: gpt-3.5-turbo"""

        prompt = await self.prompt_correct(text=prompt) if correct else prompt

        messages_data = list() if not isinstance(messages_data, list) else messages_data
        if not messages_data:
            messages_data.append(
                {"role": "assistant", "content": config.ASSISTANT_PROMPT})
        messages_data.append({"role": "user", "content": prompt})

        try:
            response = await asyncio.wait_for(self.openai.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=messages_data,
                timeout=config.OPENAI_TIMEOUT
            ), timeout=config.OPENAI_TIMEOUT + 3)

            if (response
                    and isinstance(response, ChatCompletion)
                    and isinstance(response.choices[0], Choice)
                    and isinstance(response.choices[0].message, ChatCompletionMessage)
            ):
                answer = response.choices[0].message.content.strip('\n')
                messages_data.append({"role": "assistant", "content": answer})
            else:
                messages_data.pop(-1)
                answer = config.DEFAULT_AI_ANSWER
        except APIError as exc:
            answer = config.DEFAULT_AI_ANSWER
            print(
                f'\nОшибка: {exc.message=}\n\t{exc.request=}\n\t{exc.body=}'
                f'\n\t{exc.code=}\n\t{exc.param=}\n\t{exc.type=}\n'
            )
        except Exception as exc:
            answer = config.DEFAULT_AI_ANSWER
            print(f'Ошибка: {exc.__class__.__name__} {exc}')

        return answer
