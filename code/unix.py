import datetime

# Ваша временная метка Unix в миллисекундах
unix_timestamp_ms = 1727634385901.3098

# Преобразуем временную метку в секунды
unix_timestamp = unix_timestamp_ms / 1000.0

# Преобразуем временную метку в объект datetime с учетом часового пояса
dt_object = datetime.datetime.fromtimestamp(unix_timestamp, datetime.timezone.utc)

# Выводим дату и время
print("Дата и время:", dt_object)
