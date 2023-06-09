
CREATE TABLE `teacher` (
  `Id` varchar(20) NOT NULL,
  `Name` varchar(10) NOT NULL,
  `Department` varchar(20) NOT NULL,
  `Gender` varchar(20) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `test` (
  `test` varchar(45) DEFAULT NULL,
  `Grade` int NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Department` varchar(20) NOT NULL,
  `Id` varchar(20) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `test222` (
  `Id` varchar(20) NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Grade` int NOT NULL,
  `Department` varchar(20) NOT NULL,
  `t` varchar(20) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

