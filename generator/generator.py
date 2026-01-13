import os
import time
import random
import psycopg2
from datetime import datetime

# параметры подключения к бд из переменных окружения
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'fitness_db'),
    'user': os.getenv('DB_USER', 'fitness'),
    'password': os.getenv('DB_PASSWORD', 'fitness123')
}

# настройки генерации по типам активности
# каждый тип имеет свои характерные диапазоны показателей
ACTIVITY_PROFILES = {
    'sleeping': {
        'steps_range': (0, 0),
        'heart_rate_range': (50, 65),
        'calories_per_min': (0.8, 1.2),
        'weight': 0.15  # вероятность выбора
    },
    'resting': {
        'steps_range': (0, 5),
        'heart_rate_range': (60, 75),
        'calories_per_min': (1.0, 1.5),
        'weight': 0.20
    },
    'walking': {
        'steps_range': (80, 120),
        'heart_rate_range': (75, 100),
        'calories_per_min': (3.0, 5.0),
        'weight': 0.35
    },
    'running': {
        'steps_range': (140, 180),
        'heart_rate_range': (120, 160),
        'calories_per_min': (8.0, 12.0),
        'weight': 0.15
    },
    'cycling': {
        'steps_range': (0, 10),
        'heart_rate_range': (90, 130),
        'calories_per_min': (5.0, 9.0),
        'weight': 0.15
    }
}

# список пользователей
USER_IDS = [1, 2, 3, 4, 5]


def get_db_connection():
    """создает подключение к базе данных"""
    return psycopg2.connect(**DB_CONFIG)


def choose_activity():
    """выбирает тип активности на основе весов"""
    activities = list(ACTIVITY_PROFILES.keys())
    weights = [ACTIVITY_PROFILES[a]['weight'] for a in activities]
    return random.choices(activities, weights=weights)[0]


def generate_fitness_event(user_id):
    """генерирует одно событие фитнес-трекера для пользователя"""
    activity = choose_activity()
    profile = ACTIVITY_PROFILES[activity]

    # генерируем показатели в соответствии с профилем активности
    steps = random.randint(*profile['steps_range'])
    heart_rate = random.randint(*profile['heart_rate_range'])
    calories = round(random.uniform(*profile['calories_per_min']), 2)

    return {
        'user_id': user_id,
        'steps': steps,
        'heart_rate': heart_rate,
        'calories': calories,
        'activity_type': activity
    }


def insert_event(conn, event):
    """вставляет событие в базу данных"""
    query = """
        INSERT INTO fitness_events (user_id, steps, heart_rate, calories, activity_type)
        VALUES (%(user_id)s, %(steps)s, %(heart_rate)s, %(calories)s, %(activity_type)s)
    """
    with conn.cursor() as cur:
        cur.execute(query, event)
    conn.commit()


def main():
    """основной цикл генерации данных"""
    print("запуск генератора данных фитнес-трекера...")

    # ждем пока бд будет доступна
    conn = None
    while conn is None:
        try:
            conn = get_db_connection()
            print("подключение к базе данных установлено")
        except psycopg2.OperationalError as e:
            print(f"ожидание базы данных: {e}")
            time.sleep(2)

    print("генерация данных запущена (каждую секунду)")

    try:
        while True:
            # выбираем случайного пользователя
            user_id = random.choice(USER_IDS)

            # генерируем и вставляем событие
            event = generate_fitness_event(user_id)
            insert_event(conn, event)

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] user={event['user_id']}, "
                  f"activity={event['activity_type']}, "
                  f"steps={event['steps']}, "
                  f"hr={event['heart_rate']}, "
                  f"cal={event['calories']}")

            # пауза 1 секунда
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nгенератор остановлен")
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    main()
