import asyncio
import websockets
import json
from asyncio import Queue

# Переменная для хранения кэшированных данных
cached_data = []
# Создайте очередь для сообщений
message_queue = Queue()

async def connect():
    uri = "ws://localhost:4002"
    try:
        async with websockets.connect(uri) as websocket:
            print("Підключено до WebSocket сервера")

            # Обрабатываем сообщения от сервера
            async for message in websocket:
                await message_queue.put(message)  # Добавляем сообщение в очередь
    except websockets.exceptions.ConnectionClosed as e:
        print(f"З'єднання закрито: {e.reason}")
    except Exception as e:
        print(f"Помилка WebSocket: {e}")

async def process_messages():
    while True:
        message = await message_queue.get()  # Получаем сообщение из очереди
        data = json.loads(message)
        cached_data.append(data)  # Добавляем данные в кэш
        print("Обработано сообщение:", data)

# Запускаем соединение и обработку сообщений
async def main():
    await asyncio.gather(connect(), process_messages())

if __name__ == "__main__":
    asyncio.run(main())
