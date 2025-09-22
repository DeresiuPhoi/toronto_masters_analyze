import mysql.connector
import pandas as pd
import glob
import numpy as np

# === Настройки подключения ===
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'valorant_masters_2025'
}

# Подключение к базе
try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
except mysql.connector.Error as err:
    print(f"Ошибка подключения к базе данных: {err}")
    exit()

# === Список таблиц и соответствующих CSV ===
tables_csv = {
    "event_info": "csv/event_info.csv",
    "matches": "csv/matches.csv",
    "player_stats": "csv/player_stats.csv",
    "maps_stats": "csv/maps_stats.csv",
    "agents_stats": "csv/agents_stats.csv",
    "economy_data": "csv/economy_data.csv",
    "performance_data": "csv/performance_data.csv",
    "detailed_matches_player_stats": "csv/detailed_matches_player_stats.csv",
    "detailed_matches_overview": "csv/detailed_matches_overview.csv",
    "detailed_matches_maps": "csv/detailed_matches_maps.csv"
}

# === Очистка таблиц ===
for table in tables_csv.keys():
    print(f"Очищаем таблицу {table}...")
    try:
        cursor.execute(f"DELETE FROM {table};")
    except mysql.connector.Error as err:
        print(f"Ошибка при очистке таблицы {table}: {err}")
        conn.rollback()
conn.commit()

# === Загрузка CSV ===
for table, csv_file in tables_csv.items():
    print(f"Загружаем {csv_file} в таблицу {table}...")
    try:
        df = pd.read_csv(csv_file)

        # Обработка имен колонок для совместимости с MySQL
        df.columns = [c.replace(" ", "_").replace("(", "").replace(")", "").replace("-", "_").lower() for c in df.columns]

        # Замена пустых значений NaN на None
        df = df.replace({np.nan: None})

        # Загрузка данных
        cols = ",".join([f"`{col}`" for col in df.columns]) # Оборачиваем имена колонок в обратные кавычки
        vals = ",".join(["%s"] * len(df.columns))
        sql = f"INSERT INTO {table} ({cols}) VALUES ({vals})"

        for _, row in df.iterrows():
            try:
                cursor.execute(sql, tuple(row))
            except mysql.connector.Error as err:
                print(f"Ошибка при вставке строки в таблицу {table}: {err}")
                print(f"Строка с ошибкой: {row.values}")
                # Продолжаем работу, чтобы обработать остальные строки
    except FileNotFoundError:
        print(f"Ошибка: Файл {csv_file} не найден. Проверьте путь.")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка при обработке файла {csv_file}: {e}")
    
conn.commit()

cursor.close()
conn.close()
print("Все CSV загружены в базу данных успешно!")