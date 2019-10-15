CREATE TABLE `User` (
  `id` int PRIMARY KEY NOT NULL,
  `first_name` varchar(30),
  `last_name` varchar(30),
  `email` varchar(30) NOT NULL,
  `pass_hash` varchar(50) NOT NULL
);

CREATE TABLE `Resume` (
  `id` int PRIMARY KEY NOT NULL,
  `uid` int NOT NULL,
  `title` varchar(30) NOT NULL,
  `description` varchar(10000) NOT NULL,
  `salary` int,
  `currency` ENUM ('usd', 'uah', 'eur')
);

CREATE TABLE `Vacancy` (
  `id` int PRIMARY KEY NOT NULL,
  `uid` int NOT NULL,
  `title` varchar(30) NOT NULL,
  `description` varchar(10000) NOT NULL,
  `salary` int,
  `currency` ENUM ('usd', 'uah', 'eur'),
  `experience` tinyint
);

CREATE TABLE `Connector` (
  `id` int PRIMARY KEY NOT NULL,
  `uid` int NOT NULL,
  `ad_t` ENUM ('resume', 'vacancy') NOT NULL,
  `ad_id` int NOT NULL
);

CREATE TABLE `PetProject` (
  `id` int PRIMARY KEY NOT NULL,
  `resume_id` int NOT NULL,
  `title` varchar(30) NOT NULL,
  `link` varchar(30) NOT NULL
);

CREATE TABLE `Skills` (
  `id` int PRIMARY KEY NOT NULL,
  `ad_t` ENUM ('resume', 'vacancy') NOT NULL,
  `ad_id` int NOT NULL,
  `skill` varchar(30) NOT NULL
);

CREATE TABLE `Responsibilities` (
  `id` int PRIMARY KEY NOT NULL,
  `vacancy_id` int NOT NULL,
  `responsibility` varchar(30) NOT NULL
);

ALTER TABLE `User` ADD FOREIGN KEY (`id`) REFERENCES `Connector` (`uid`);

ALTER TABLE `Vacancy` ADD FOREIGN KEY (`id`) REFERENCES `Connector` (`ad_id`);

ALTER TABLE `Resume` ADD FOREIGN KEY (`id`) REFERENCES `Connector` (`ad_id`);

ALTER TABLE `Resume` ADD FOREIGN KEY (`id`) REFERENCES `Skills` (`ad_id`);

ALTER TABLE `Vacancy` ADD FOREIGN KEY (`id`) REFERENCES `Skills` (`ad_id`);

ALTER TABLE `Vacancy` ADD FOREIGN KEY (`id`) REFERENCES `Responsibilities` (`vacancy_id`);

ALTER TABLE `PetProject` ADD FOREIGN KEY (`id`) REFERENCES `Resume` (`id`);
