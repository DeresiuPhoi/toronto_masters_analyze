CREATE TABLE `player_stats` (
  `player_id` VARCHAR(255) NOT NULL,
  `player_name` VARCHAR(255),
  `team` VARCHAR(255),
  `rounds` INT,
  `rating` FLOAT,
  `acs` FLOAT,
  `kd_ratio` FLOAT,
  PRIMARY KEY (`player_id`)
);

CREATE TABLE `agents_stats` (
  `agent_name` VARCHAR(255) NOT NULL,
  `total_utilization` FLOAT,
  `map_utilizations` TEXT,
  PRIMARY KEY (`agent_name`)
);

CREATE TABLE `economy_data` (
  `team` VARCHAR(255) NOT NULL,
  `pistol_won` INT,
  `full_buywon` VARCHAR(255),
  PRIMARY KEY (`team`)
);

CREATE TABLE `detailed_matches_player_stats` (
  `match_id` VARCHAR(255) NOT NULL,
  `map_name` VARCHAR(255) NOT NULL,
  `player_id` VARCHAR(255),
  `player_team` VARCHAR(255),
  `agent` VARCHAR(255),
  `k` INT,
  `kills` INT,
  `deaths` INT,
  `assists` INT,
  `rating` FLOAT,
  `event_stage` VARCHAR(255),
  `map_winner` VARCHAR(255),
  PRIMARY KEY (`match_id`, `map_name`, `player_id`),
  FOREIGN KEY (`player_id`) REFERENCES `player_stats`(`player_id`),
  FOREIGN KEY (`match_id`, `map_name`) REFERENCES `detailed_matches_maps`(`match_id`, `map_name`)
);

CREATE TABLE `detailed_matches_maps` (
  `match_id` VARCHAR(255) NOT NULL,
  `map_name` VARCHAR(255) NOT NULL,
  `map_winner` VARCHAR(255),
  `map_loser` VARCHAR(255),
  PRIMARY KEY (`match_id`, `map_name`)
);

CREATE TABLE `event_info` (
  `event_id` INT NOT NULL,
  `event_name` VARCHAR(255),
  PRIMARY KEY (`event_id`)
);

CREATE TABLE `matches` (
  `match_id` VARCHAR(255) NOT NULL,
  `team1` VARCHAR(255),
  `team2` VARCHAR(255),
  PRIMARY KEY (`match_id`)
);