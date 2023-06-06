DROP TABLE IF EXISTS `course`;
CREATE TABLE `course` (
  `Id` varchar(10) NOT NULL,
  `Name` varchar(20) NOT NULL,
  `TeacherID` varchar(20) NOT NULL,
  KEY `fk_teach` (`TeacherID`),
  CONSTRAINT `fk_teach` FOREIGN KEY (`TeacherID`) REFERENCES `teacher` (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

DROP TABLE IF EXISTS `student`;
CREATE TABLE `student` (
  `Id` varchar(20) NOT NULL,
  `Name` varchar(20) NOT NULL,
  `Grade` int(11) NOT NULL,
  `Department` varchar(20) NOT NULL,
  `Gender` varchar(20) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

DROP TABLE IF EXISTS `teacher`;
CREATE TABLE `teacher` (
  `Id` varchar(20) NOT NULL,
  `Name` varchar(10) NOT NULL,
  `Department` varchar(20) NOT NULL,
  `Gender` varchar(20) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

