-- инициализация базы данных для фитнес-трекера

-- таблица событий фитнес-трекера
CREATE TABLE IF NOT EXISTS fitness_events (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    steps INTEGER NOT NULL,
    heart_rate INTEGER NOT NULL,
    calories DECIMAL(6,2) NOT NULL,
    activity_type VARCHAR(20) NOT NULL
);

-- индекс для быстрого поиска по времени
CREATE INDEX IF NOT EXISTS idx_fitness_events_timestamp ON fitness_events(timestamp);

-- индекс для поиска по пользователю
CREATE INDEX IF NOT EXISTS idx_fitness_events_user_id ON fitness_events(user_id);

-- индекс для поиска по типу активности
CREATE INDEX IF NOT EXISTS idx_fitness_events_activity_type ON fitness_events(activity_type);
