"""Основной модуль запускающий чат с OpenAI"""
import asyncio

from openai_manager import OpenAIManager

messages_data = []


async def chat():
    """Функция запускающая чат для общения с OpenAI"""
    openai = OpenAIManager()
    while True:
        request = input('Введите ваш вопрос: ')
        print(
            'Ответ:',
            await openai.answer_gpt_3_5_turbo(prompt=request, messages_data=messages_data)
        )

if __name__ == '__main__':
    asyncio.run(chat())

