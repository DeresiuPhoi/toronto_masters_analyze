-- 1. Средний ACS игроков по командам
SELECT team, ROUND(AVG(acs), 2) AS avg_acs
FROM player_stats
GROUP BY team
ORDER BY avg_acs DESC;

-- 2. Средний K/D ratio по игрокам
SELECT player_name, ROUND(AVG(kd_ratio), 2) AS avg_kd
FROM player_stats
GROUP BY player_name
ORDER BY avg_kd DESC;

-- 3. Победы команд по картам
SELECT dm.map_name, dm.map_winner, COUNT(*) AS wins
FROM detailed_matches_player_stats dm
GROUP BY dm.map_name, dm.map_winner
ORDER BY dm.map_name, wins DESC;

-- 4. Использование агентов и их эффективность (средний рейтинг)
SELECT p.agent, COUNT(*) AS pick_count, ROUND(AVG(p.rating),2) AS avg_rating
FROM performance_data p
GROUP BY p.agent
ORDER BY pick_count DESC;

-- 5. Количество клатчей 1vX по игрокам
SELECT Player, 
       SUM(clutch_1v1 + clutch_1v2 + clutch_1v3 + clutch_1v4 + clutch_1v5) AS total_clutches
FROM performance_data
GROUP BY Player
ORDER BY total_clutches DESC;

-- 6. Победы команд после пистолетного раунда
SELECT Team, SUM(Pistol_Won) AS pistol_wins
FROM economy_data
GROUP BY Team
ORDER BY pistol_wins DESC;

-- 7. Средний рейтинг игроков по стадиям турнира
SELECT event_stage, ROUND(AVG(rating),2) AS avg_rating
FROM detailed_matches_player_stats
GROUP BY event_stage
ORDER BY avg_rating DESC;

-- 8. Победы команд по экономическим раундам (Full buy wins)
SELECT Team, SUM(CAST(SUBSTRING_INDEX(full_buy_won,'(',1) AS UNSIGNED)) AS full_buy_wins
FROM economy_data
GROUP BY Team
ORDER BY full_buy_wins DESC;

-- 9. Самые результативные карты (по среднему количеству убийств на карте)
SELECT map_name, ROUND(AVG(k),2) AS avg_kills
FROM detailed_matches_player_stats
GROUP BY map_name
ORDER BY avg_kills DESC;

-- 10. Агент с наибольшим процентом побед на картах
SELECT dm.agent, COUNT(*) AS wins
FROM detailed_matches_player_stats dm
WHERE dm.player_team = dm.map_winner
GROUP BY dm.agent
ORDER BY wins DESC;
