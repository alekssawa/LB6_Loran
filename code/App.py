from quart import Quart, render_template, jsonify, websocket
import asyncio
import websockets
import json
import logging
from config import CONFIG
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Quart(__name__)

# Инициализация начальных точек
initial_points = [
    {'sourceId': 'source1', 'x': 0, 'y': 0, 'id': 'initial1', 'receivedAt': int(time.time() * 1000)},
    {'sourceId': 'source2', 'x': 0, 'y': 100, 'id': 'initial2', 'receivedAt': int(time.time() * 1000)},
    {'sourceId': 'source3', 'x': 100, 'y': 0, 'id': 'initial3', 'receivedAt': int(time.time() * 1000)}
]

cached_data = initial_points.copy()
clients = set()


def process_data(raw_data):
    # Обновляем только receivedAt для соответствующего sourceId
    for point in cached_data:
        if point['sourceId'] == raw_data.get('sourceId'):
            point['receivedAt'] = raw_data.get('receivedAt')
            point['id'] = raw_data.get('id')
            return point

    # Если sourceId не найден, создаем новую точку
    return {
        'x': raw_data.get('x', 0),
        'y': raw_data.get('y', 0),
        'sourceId': raw_data.get('sourceId'),
        'id': raw_data.get('id'),
        'receivedAt': raw_data.get('receivedAt', int(time.time() * 1000))
    }


async def connect_to_source():
    while True:
        try:
            async with websockets.connect(CONFIG['SOURCE_WEBSOCKET_URI']) as websocket:
                logger.info("Подключено к WebSocket серверу источника данных")
                async for message in websocket:
                    await handle_message(message)
        except websockets.exceptions.ConnectionClosed as e:
            logger.error(f"Соединение с источником данных закрыто: {e.reason}")
        except Exception as e:
            logger.error(f"Ошибка WebSocket при подключении к источнику: {e}")

        logger.info("Попытка переподключения к источнику через 5 секунд...")
        await asyncio.sleep(5)


async def handle_message(message):
    try:
        raw_data = json.loads(message)
        processed_data = process_data(raw_data)
        if processed_data not in cached_data:
            cached_data.append(processed_data)
        #logger.info(f"Обработано сообщение: {processed_data}")
        await notify_clients(processed_data)
    except json.JSONDecodeError:
        logger.error(f"Получено некорректное JSON сообщение: {message}")
    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")


async def notify_clients(data):
    if clients:
        disconnected_clients = set()
        for ws in clients:
            try:
                await ws.send(json.dumps(data))
            except Exception as e:
                logger.error(f"Ошибка при отправке данных клиенту: {e}")
                disconnected_clients.add(ws)

        clients.difference_update(disconnected_clients)


@app.before_serving
async def before_serving():
    app.add_background_task(connect_to_source)


@app.route('/')
async def index():
    return await render_template('index.html')


@app.websocket('/ws')
async def ws():
    client = websocket._get_current_object()
    clients.add(client)
    try:
        for data in cached_data:
            await client.send(json.dumps(data))

        while True:
            data = await client.receive()
            logger.info(f"Получено сообщение от клиента: {data}")
            await client.send(json.dumps({"status": "received", "message": "Сообщение получено!"}))
    except asyncio.CancelledError:
        pass
    except Exception as e:
        logger.error(f"Ошибка в WebSocket соединении с клиентом: {e}")
    finally:
        clients.remove(client)


@app.route('/get-data', methods=['GET'])
async def get_data():
    return jsonify(cached_data)


if __name__ == "__main__":
    app.run(host=CONFIG['HOST'], port=CONFIG['PORT'], debug=CONFIG['DEBUG'])