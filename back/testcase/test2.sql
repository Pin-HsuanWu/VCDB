CREATE TABLE `Persons_Test` (
  `ID` varchar(40) NOT NULL,
  `LastName` varchar(40) NOT NULL,
  `Address` varchar(40) NOT NULL,
  UNIQUE KEY `UC_Person` (`ID`,`LastName`),
  UNIQUE KEY `UC_Address` (`Address`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `comments` (
  `Course` varchar(40) NOT NULL,
  `Year` int(11) DEFAULT NULL,
  `Comments` varchar(255) NOT NULL,
  PRIMARY KEY (`Course`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


CREATE TABLE `getid1` (
  `StuId` varchar(10) DEFAULT NULL,
  `TeacherId` varchar(10) DEFAULT '987654321',
  KEY `StuId` (`StuId`),
  KEY `userDefined` (`TeacherId`),
  CONSTRAINT `getid1_ibfk_1` FOREIGN KEY (`StuId`) REFERENCES `student` (`Id`) ON DELETE CASCADE ON UPDATE SET NULL,
  CONSTRAINT `userDefined` FOREIGN KEY (`TeacherId`) REFERENCES `teacher` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


CREATE TABLE `getid2` (
  `RowId` int(11) NOT NULL,
  `StuId` varchar(10) DEFAULT NULL,
  `TeacherId` varchar(10) DEFAULT NULL,
  `TodayDate` date DEFAULT curdate(),
  PRIMARY KEY (`RowId`),
  KEY `userStu` (`StuId`),
  CONSTRAINT `userStu` FOREIGN KEY (`StuId`) REFERENCES `teacher` (`Id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


CREATE TABLE `student` (
  `Id` varchar(20) NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Grade` int(11) NOT NULL,
  `Department` varchar(20) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;


CREATE TABLE `teacher` (
  `Id` varchar(20) NOT NULL,
  `Name` varchar(10) NOT NULL,
  `Department` varchar(20) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE `department` (
  `Id` varchar(20) NOT NULL,
  `Name` varchar(10) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

CREATE TABLE `Employee` (
  `EmployeeID` varchar(40) NOT NULL,
  `EmployeeName` varchar(40) NOT NULL,
  `Birthday` date DEFAULT NULL,
  `IsPartTime` tinyint(1) DEFAULT NULL,
  `IsFullTime` tinyint(1) DEFAULT NULL,
  `IsManager` tinyint(1) DEFAULT '0',
  `WorkingHour` int DEFAULT '0',
  `BaseSalary` int DEFAULT '0',
  PRIMARY KEY (`EmployeeID`),
  CONSTRAINT `employee_chk_1` CHECK (((`WorkingHour` >= 5) and (`WorkingHour` <= 46) and (`BaseSalary` >= 0)))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

