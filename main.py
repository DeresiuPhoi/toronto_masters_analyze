import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

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
    cursor = conn.cursor(dictionary=True)
except mysql.connector.Error as err:
    print(f"Ошибка подключения к базе данных: {err}")
    exit()

# === SQL-запросы ===
queries = {
    "avg_acs_per_team": """
        SELECT team, ROUND(AVG(acs), 2) AS avg_acs
        FROM player_stats
        GROUP BY team
        ORDER BY avg_acs DESC;
    """,
    "player_fk_fd_ratio": """
        SELECT
            player_name,
            ROUND(SUM(first_kills) / SUM(first_deaths), 2) AS fk_fd_ratio
        FROM player_stats
        GROUP BY player_name
        ORDER BY fk_fd_ratio DESC;
    """,
    "team_wins_per_map": """
        SELECT dm.map_name, dm.map_winner, COUNT(*) AS wins
        FROM detailed_matches_maps dm
        GROUP BY dm.map_name, dm.map_winner
        ORDER BY dm.map_name, wins DESC;
    """,
    "agent_usage_rating": """
        SELECT
            agent_name,
            COUNT(agent_name) AS num_pick,
            ROUND(AVG(rating), 2) AS avg_rating
        FROM detailed_matches_player_stats
        GROUP BY agent_name
        ORDER BY num_pick DESC;
    """,
    "player_clutches": """
        SELECT
            player_name,
            clutches
        FROM player_stats
        WHERE clutches IS NOT NULL AND clutches != ''
        ORDER BY CAST(SUBSTRING_INDEX(clutches, '/', 1) AS UNSIGNED) DESC;
    """,
    "team_pistol_wins": """
        SELECT team, SUM(pistol_won) AS pistol_wins
        FROM economy_data
        GROUP BY team
        ORDER BY pistol_wins DESC;
    """,
    "agent_effectiveness_by_map": """
        SELECT
            agent,
            map_name,
            COUNT(*) AS wins
        FROM detailed_matches_player_stats
        WHERE player_team = map_winner
        GROUP BY agent, map_name
        ORDER BY wins DESC
        LIMIT 10;
    """,
    "kast_per_player": """
        SELECT
            player_name,
            AVG(REPLACE(kast, '%', '')) AS avg_kast
        FROM player_stats
        GROUP BY player_name
        ORDER BY avg_kast DESC
        LIMIT 10;
    """,
    "pistol_vs_fullbuy_wins": """
        SELECT
            team,
            SUM(pistol_won) AS total_pistol_wins,
            SUM(CAST(SUBSTRING_INDEX(full_buywon, ' (', 1) AS UNSIGNED)) AS total_full_buy_wins
        FROM economy_data
        GROUP BY team
        ORDER BY total_pistol_wins DESC;
    """,
    "agent_most_wins": """
        SELECT agent, COUNT(*) AS wins
        FROM detailed_matches_player_stats
        WHERE player_team = map_winner
        GROUP BY agent
        ORDER BY wins DESC;
    """
}

# --- Настройка папки для графиков ---
output_folder = "charts"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
    print(f"Создана папка для графиков: '{output_folder}'")

# === Выполнение запросов и вывод ===
for name, query in queries.items():
    print(f"\n=== {name} ===")
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        
        if results:
            df = pd.DataFrame(results)
            print(df.head(10))
            # Сохранение в CSV
            df.to_csv(f"{name}.csv", index=False)
            
            # --- Визуализация данных ---
            plt.figure(figsize=(12, 8))
            
            if name == "avg_acs_per_team":
                sns.barplot(x='team', y='avg_acs', data=df.head(10))
                plt.title('Средний ACS по командам')
                plt.xlabel('Команда')
                plt.ylabel('Средний ACS')
            elif name == "player_fk_fd_ratio":
                sns.barplot(x='player_name', y='fk_fd_ratio', data=df.head(10))
                plt.title('Соотношение первой крови к первой смерти')
                plt.xlabel('Игрок')
                plt.ylabel('Соотношение FK/FD')
            elif name == "team_wins_per_map":
                # Улучшенная визуализация для этого отчёта
                df_filtered = df[df['map_winner'].notna()].head(10)
                sns.barplot(x='map_winner', y='wins', hue='map_name', data=df_filtered)
                plt.title('Победы команд по картам')
                plt.xlabel('Команда-победитель')
                plt.ylabel('Количество побед')
                plt.legend(title='Карта')
            elif name == "agent_usage_rating":
                sns.barplot(x='agent_name', y='avg_rating', data=df.head(10))
                plt.title('Средний рейтинг по агентам')
                plt.xlabel('Агент')
                plt.ylabel('Средний рейтинг')
            elif name == "player_clutches":
                df['clutches_won'] = df['clutches'].str.split('/').str[0].astype(int)
                sns.barplot(x='player_name', y='clutches_won', data=df.head(10))
                plt.title('Количество выигранных клатчей по игрокам')
                plt.xlabel('Игрок')
                plt.ylabel('Клатчи (выиграно)')
            elif name == "team_pistol_wins":
                sns.barplot(x='team', y='pistol_wins', data=df.head(10))
                plt.title('Количество выигранных пистолетных раундов')
                plt.xlabel('Команда')
                plt.ylabel('Выиграно пистолетных раундов')
            elif name == "agent_effectiveness_by_map":
                sns.barplot(x='agent', y='wins', hue='map_name', data=df.head(10))
                plt.title('Эффективность агентов на разных картах (победы)')
                plt.xlabel('Агент')
                plt.ylabel('Количество побед')
                plt.legend(title='Карта')
            elif name == "kast_per_player":
                sns.barplot(x='player_name', y='avg_kast', data=df.head(10))
                plt.title('Средний KAST по игрокам')
                plt.xlabel('Игрок')
                plt.ylabel('KAST (%)')
            elif name == "pistol_vs_fullbuy_wins":
                df_melted = df.head(10).melt('team', var_name='Round_Type', value_name='Wins')
                sns.barplot(x='team', y='Wins', hue='Round_Type', data=df_melted)
                plt.title('Сравнение побед в пистолетных и Full Buy раундах')
                plt.xlabel('Команда')
                plt.ylabel('Количество побед')
                plt.legend(title='Тип раунда', labels=['Пистолетные', 'Full Buy'])
            elif name == "agent_most_wins":
                sns.barplot(x='agent', y='wins', data=df.head(10))
                plt.title('Самые выигрышные агенты')
                plt.xlabel('Агент')
                plt.ylabel('Количество побед')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            plt.savefig(os.path.join(output_folder, f"{name}.png"))
            plt.close()
            
        else:
            print("Нет данных для отображения.")
            
    except mysql.connector.Error as err:
        print(f"Ошибка при выполнении запроса '{name}': {err}")

# Закрываем соединение
cursor.close()
conn.close()
print(f"\nВсе запросы выполнены, данные сохранены в CSV, а графики — в папке '{output_folder}'.")