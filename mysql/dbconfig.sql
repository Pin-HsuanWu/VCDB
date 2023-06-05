-- create databases
CREATE DATABASE IF NOT EXISTS vcdb;
CREATE DATABASE IF NOT EXISTS userdb;


-- setup user privileges
CREATE USER if not exists myuser@0.0.0.0 IDENTIFIED BY 'mypassword';
CREATE USER if not exists root@0.0.0.0 IDENTIFIED BY 'mypassword2';

GRANT ALL PRIVILEGES ON vcdb.* TO myuser@0.0.0.0 with grant option;
GRANT ALL PRIVILEGES ON vcdb.* TO root@0.0.0.0 with grant option;

GRANT ALL PRIVILEGES ON userdb.* TO myuser@0.0.0.0 with grant option;
GRANT ALL PRIVILEGES ON userdb.* TO root@0.0.0.0 with grant option;
FLUSH PRIVILEGES;



use vcdb;
CREATE TABLE `branch`(
    `bid` int not null AUTO_INCREMENT,
    `name` varchar(125) NOT NULL,
    `tail` varchar(500) not null,
    PRIMARY KEY (`bid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


CREATE TABLE `commit`(
    `version` varchar(500) not null,
    `branch` varchar(500) not null,
    `last_version` varchar(500) ,
    `upgrade` varchar(5000) not null,
    `downgrade` varchar(5000) not null,
    `time` varchar(5000) not null,
    `uid` varchar(500) not null,
    `msg` varchar(500) ,
    PRIMARY KEY (`version`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


CREATE TABLE `merge`(
    `mid` int not null AUTO_INCREMENT,
    `version` varchar(500) not null,
    `merge_from` varchar(500) not null,
    PRIMARY KEY (`mid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;



CREATE TABLE `user`(
    `uid` varchar(500) not null,
    `name` varchar(125) not null,
    `email` varchar(125) not null,
    `current_version` varchar(500),
    `current_branch` varchar(500) not null,
    PRIMARY KEY (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


insert into user values ("testtt1", "elaine", "elaine.com", "", "main");
insert into user values ("testtt2", "calista", "calista.com", "", "main");
insert into user values ("testtt3", "leo", "leo.com", "", "main");
insert into user values ("testtt4", "yuu", "yuu.com", "", "main");

use userdb;