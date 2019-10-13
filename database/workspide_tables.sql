CREATE TABLE `User` (
  `id` int PRIMARY KEY,
  `first_name` varchar(30),
  `last_name` varchar(30),
  `email` varchar(30),
  `pass_hash` varchar(50)
);

CREATE TABLE `Resume` (
  `id` int PRIMARY KEY,
  `uid` int,
  `title` varchar(30),
  `description` varchar(10000),
  `salary` int,
  `currency` ENUM ('usd', 'uah', 'eur')
);

CREATE TABLE `Vacancy` (
  `id` int PRIMARY KEY,
  `uid` int,
  `title` varchar(30),
  `description` varchar(10000),
  `salary` int,
  `currency` ENUM ('usd', 'uah', 'eur'),
  `experience` tinyint
);

CREATE TABLE `Connector` (
  `id` int PRIMARY KEY,
  `uid` int,
  `ad_t` ENUM ('resume', 'vacancy'),
  `ad_id` int
);

CREATE TABLE `PetProject` (
  `id` int PRIMARY KEY,
  `resume_id` int,
  `title` varchar(30),
  `link` varchar(30)
);

CREATE TABLE `Skills` (
  `id` int PRIMARY KEY,
  `ad_t` ENUM ('resume', 'vacancy'),
  `ad_id` int,
  `skill` varchar(30)
);

CREATE TABLE `Responsibilities` (
  `id` int PRIMARY KEY,
  `vacancy_id` int,
  `responsibility` varchar(30)
);

ALTER TABLE `User` ADD FOREIGN KEY (`id`) REFERENCES `Connector` (`uid`);

ALTER TABLE `Vacancy` ADD FOREIGN KEY (`id`) REFERENCES `Connector` (`ad_id`);

ALTER TABLE `Resume` ADD FOREIGN KEY (`id`) REFERENCES `Connector` (`ad_id`);

ALTER TABLE `Resume` ADD FOREIGN KEY (`id`) REFERENCES `Skills` (`ad_id`);

ALTER TABLE `Vacancy` ADD FOREIGN KEY (`id`) REFERENCES `Skills` (`ad_id`);

ALTER TABLE `Vacancy` ADD FOREIGN KEY (`id`) REFERENCES `Responsibilities` (`vacancy_id`);

ALTER TABLE `PetProject` ADD FOREIGN KEY (`id`) REFERENCES `Resume` (`id`);
