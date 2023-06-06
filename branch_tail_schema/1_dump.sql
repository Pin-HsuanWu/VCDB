
CREATE TABLE `development_team` (
  `Name` varchar(40) NOT NULL,
  PRIMARY KEY (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;


CREATE TABLE `game` (
  `Title` varchar(40) NOT NULL,
  `Year` int(11) DEFAULT NULL CHECK (`Year` > 1800 and `Year` < 2100),
  `Price` int(11) DEFAULT NULL,
  `Development_team` varchar(40) NOT NULL,
  PRIMARY KEY (`Title`),
  KEY `Development_team` (`Development_team`),
  CONSTRAINT `game_ibfk_1` FOREIGN KEY (`Development_team`) REFERENCES `development_team` (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;


CREATE TABLE `student` (
  `Id` varchar(20) NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Grade` int(11) DEFAULT NULL,
  `Department` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

