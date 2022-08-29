CREATE DATABASE automatyka;

USE automatyka;

CREATE TABLE `configuration` (
	`id_config` INT(11) NOT NULL AUTO_INCREMENT,
	`temp_w` DECIMAL(10,3) NOT NULL DEFAULT '0.000',
	`temp_e` DECIMAL(10,3) NOT NULL DEFAULT '0.000',
	`dimension_x` INT(11) NOT NULL DEFAULT '0',
	`dimension_y` INT(11) NOT NULL DEFAULT '0',
	`dimension_z` INT(11) NOT NULL DEFAULT '0',
	PRIMARY KEY (`id_config`) USING BTREE
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


CREATE TABLE `measurement` (
	`id_measurement` INT NOT NULL AUTO_INCREMENT,
	`id_config` INT NOT NULL,
	`temp` DECIMAL(10,3) NOT NULL DEFAULT 0,
	`date_time` DATETIME NOT NULL DEFAULT 0,
	PRIMARY KEY (`id_measurement`),
	CONSTRAINT `CONFIG` FOREIGN KEY (`id_config`) REFERENCES `configuration` (`id_config`)
)
COLLATE='utf8_general_ci'
ENGINE=InnoDB
;


INSERT INTO configuration(temp_w,temp_e,dimension_x,dimension_y,dimension_z)
VALUES (24.0,18.0,50,50,50);

INSERT INTO measurement (id_config,temp,date_time)
VALUES (1, 25.000, "2021-01-21 12:00:00")