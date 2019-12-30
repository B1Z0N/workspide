BEGIN;
--
-- Create model User
--
CREATE TABLE `main_user` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `password` varchar(128) NOT NULL, `last_login` datetime(6) NULL, `email` varchar(50) NOT NULL UNIQUE, `first_name` varchar(30) NULL, `last_name` varchar(30) NULL, `not_read` integer UNSIGNED NOT NULL, `is_active` bool NOT NULL, `is_admin` bool NOT NULL);
--
-- Create model Ad
--
CREATE TABLE `main_ad` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `ad_type` varchar(7) NOT NULL, `city` varchar(30) NOT NULL, `title` varchar(50) NOT NULL, `text` longtext NULL, `salary_currency` varchar(3) NOT NULL, `salary` numeric(14, 2) NULL, `experience` integer UNSIGNED NULL, `experience_type` varchar(6) NOT NULL, `pub_dtime` datetime(6) NOT NULL, `is_archived` bool NOT NULL, `uid_id` integer NOT NULL);
--
-- Create model Skill
--
CREATE TABLE `main_skill` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `text` varchar(50) NOT NULL, `ad_id_id` integer NOT NULL);
--
-- Create model Responsibility
--
CREATE TABLE `main_responsibility` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `text` varchar(50) NOT NULL, `vacancy_id_id` integer NOT NULL);
--
-- Create model Pide
--
CREATE TABLE `main_pide` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `comment` longtext NULL, `state` varchar(8) NOT NULL, `pub_dtime` datetime(6) NOT NULL, `ad_from_id` integer NULL, `ad_to_id` integer NOT NULL, `uid_from_id` integer NOT NULL);
--
-- Create model PetProject
--
CREATE TABLE `main_petproject` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `text` varchar(50) NOT NULL, `link` varchar(50) NOT NULL, `resume_id_id` integer NOT NULL);
ALTER TABLE `main_ad` ADD CONSTRAINT `main_ad_uid_id_7e75c2c8_fk_main_user_id` FOREIGN KEY (`uid_id`) REFERENCES `main_user` (`id`);
ALTER TABLE `main_skill` ADD CONSTRAINT `main_skill_ad_id_id_b3f92a98_fk_main_ad_id` FOREIGN KEY (`ad_id_id`) REFERENCES `main_ad` (`id`);
ALTER TABLE `main_responsibility` ADD CONSTRAINT `main_responsibility_vacancy_id_id_cdefa442_fk_main_ad_id` FOREIGN KEY (`vacancy_id_id`) REFERENCES `main_ad` (`id`);
ALTER TABLE `main_pide` ADD CONSTRAINT `main_pide_ad_from_id_3de15236_fk_main_ad_id` FOREIGN KEY (`ad_from_id`) REFERENCES `main_ad` (`id`);
ALTER TABLE `main_pide` ADD CONSTRAINT `main_pide_ad_to_id_19107f51_fk_main_ad_id` FOREIGN KEY (`ad_to_id`) REFERENCES `main_ad` (`id`);
ALTER TABLE `main_pide` ADD CONSTRAINT `main_pide_uid_from_id_2c2aa502_fk_main_user_id` FOREIGN KEY (`uid_from_id`) REFERENCES `main_user` (`id`);
ALTER TABLE `main_petproject` ADD CONSTRAINT `main_petproject_resume_id_id_f937978f_fk_main_ad_id` FOREIGN KEY (`resume_id_id`) REFERENCES `main_ad` (`id`);
COMMIT;

