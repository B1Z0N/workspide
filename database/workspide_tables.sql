CREATE TABLE `User` (
  `id` int PRIMARY KEY NOT NULL,
  `first_name` varchar(30),
  `last_name` varchar(30),
  `email` varchar(30) NOT NULL,
  `pass_hash` varchar(64) NOT NULL
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
  `experience_months` int
);

CREATE TABLE `SkillForResume` (
  `id` int PRIMARY KEY NOT NULL,
  `resume_id` int NOT NULL,
  `text` varchar(100) NOT NULL
);

CREATE TABLE `SkillForVacancy` (
  `id` int PRIMARY KEY NOT NULL,
  `vacancy_id` int NOT NULL,
  `text` varchar(100) NOT NULL
);

CREATE TABLE `PetProject` (
  `id` int PRIMARY KEY NOT NULL,
  `resume_id` int NOT NULL,
  `title` varchar(30) NOT NULL,
  `link` varchar(30) NOT NULL
);

CREATE TABLE `Responsibilities` (
  `id` int PRIMARY KEY NOT NULL,
  `vacancy_id` int NOT NULL,
  `responsibility` varchar(30) NOT NULL
);

ALTER TABLE `User` ADD FOREIGN KEY (`id`) REFERENCES `Resume` (`uid`);

ALTER TABLE `User` ADD FOREIGN KEY (`id`) REFERENCES `Vacancy` (`uid`);

ALTER TABLE `Resume` ADD FOREIGN KEY (`id`) REFERENCES `PetProject` (`resume_id`);

ALTER TABLE `Resume` ADD FOREIGN KEY (`id`) REFERENCES `SkillForResume` (`resume_id`);

ALTER TABLE `Vacancy` ADD FOREIGN KEY (`id`) REFERENCES `SkillForVacancy` (`vacancy_id`);

ALTER TABLE `Vacancy` ADD FOREIGN KEY (`id`) REFERENCES `Responsibilities` (`vacancy_id`);
