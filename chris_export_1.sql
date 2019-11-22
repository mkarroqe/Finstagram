-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Nov 22, 2019 at 10:33 PM
-- Server version: 5.7.25
-- PHP Version: 7.3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `finstagram`
--

-- --------------------------------------------------------

--
-- Table structure for table `BelongTo`
--

CREATE TABLE `BelongTo` (
  `member_username` varchar(20) NOT NULL,
  `owner_username` varchar(20) NOT NULL,
  `groupName` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `Follow`
--

CREATE TABLE `Follow` (
  `username_followed` varchar(20) NOT NULL,
  `username_follower` varchar(20) NOT NULL,
  `followstatus` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Follow`
--

INSERT INTO `Follow` (`username_followed`, `username_follower`, `followstatus`) VALUES
('test2', 'test', 1),
('test3', 'test', 0);

-- --------------------------------------------------------

--
-- Table structure for table `Friendgroup`
--

CREATE TABLE `Friendgroup` (
  `groupOwner` varchar(20) NOT NULL,
  `groupName` varchar(20) NOT NULL,
  `description` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `Likes`
--

CREATE TABLE `Likes` (
  `username` varchar(20) NOT NULL,
  `photoID` int(11) NOT NULL,
  `liketime` datetime DEFAULT NULL,
  `rating` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Likes`
--

INSERT INTO `Likes` (`username`, `photoID`, `liketime`, `rating`) VALUES
('test', 1, NULL, 5);

-- --------------------------------------------------------

--
-- Table structure for table `Person`
--

CREATE TABLE `Person` (
  `username` varchar(20) NOT NULL,
  `password` char(64) DEFAULT NULL,
  `firstName` varchar(20) DEFAULT NULL,
  `lastName` varchar(20) DEFAULT NULL,
  `bio` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Person`
--

INSERT INTO `Person` (`username`, `password`, `firstName`, `lastName`, `bio`) VALUES
('test', 'test', 'Christopher', 'Martinez', 'I am a man who likes to code'),
('test2', 'test', 'bobert', 'Robertson', 'I am the one who knocks'),
('test3', 'test', 'Micheal', 'Joe', 'Rubber band ball');

-- --------------------------------------------------------

--
-- Table structure for table `Photo`
--

CREATE TABLE `Photo` (
  `photoID` int(11) NOT NULL,
  `postingdate` datetime DEFAULT NULL,
  `filepath` varchar(10000) DEFAULT NULL,
  `allFollowers` tinyint(1) DEFAULT NULL,
  `caption` varchar(100) DEFAULT NULL,
  `photoPoster` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `Photo`
--

INSERT INTO `Photo` (`photoID`, `postingdate`, `filepath`, `allFollowers`, `caption`, `photoPoster`) VALUES
(1, '2019-11-22 15:25:14', 'https://www.nationalgeographic.com/content/dam/animals/thumbs/rights-exempt/mammals/d/domestic-dog_thumb.jpg', 1, 'Friendly doggo #blessed', 'test'),
(2, '2019-11-24 15:25:14', 'https://www.nationalgeographic.com/content/dam/animals/thumbs/rights-exempt/mammals/d/domestic-dog_thumb.jpg', 1, 'test', 'test2');

-- --------------------------------------------------------

--
-- Table structure for table `SharedWith`
--

CREATE TABLE `SharedWith` (
  `groupOwner` varchar(20) NOT NULL,
  `groupName` varchar(20) NOT NULL,
  `photoID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `Tagged`
--

CREATE TABLE `Tagged` (
  `username` varchar(20) NOT NULL,
  `photoID` int(11) NOT NULL,
  `tagstatus` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `BelongTo`
--
ALTER TABLE `BelongTo`
  ADD PRIMARY KEY (`member_username`,`owner_username`,`groupName`),
  ADD KEY `owner_username` (`owner_username`,`groupName`);

--
-- Indexes for table `Follow`
--
ALTER TABLE `Follow`
  ADD PRIMARY KEY (`username_followed`,`username_follower`),
  ADD KEY `username_follower` (`username_follower`);

--
-- Indexes for table `Friendgroup`
--
ALTER TABLE `Friendgroup`
  ADD PRIMARY KEY (`groupOwner`,`groupName`);

--
-- Indexes for table `Likes`
--
ALTER TABLE `Likes`
  ADD PRIMARY KEY (`username`,`photoID`),
  ADD KEY `photoID` (`photoID`);

--
-- Indexes for table `Person`
--
ALTER TABLE `Person`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `Photo`
--
ALTER TABLE `Photo`
  ADD PRIMARY KEY (`photoID`),
  ADD KEY `photoPoster` (`photoPoster`);

--
-- Indexes for table `SharedWith`
--
ALTER TABLE `SharedWith`
  ADD PRIMARY KEY (`groupOwner`,`groupName`,`photoID`),
  ADD KEY `photoID` (`photoID`);

--
-- Indexes for table `Tagged`
--
ALTER TABLE `Tagged`
  ADD PRIMARY KEY (`username`,`photoID`),
  ADD KEY `photoID` (`photoID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Photo`
--
ALTER TABLE `Photo`
  MODIFY `photoID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `BelongTo`
--
ALTER TABLE `BelongTo`
  ADD CONSTRAINT `belongto_ibfk_1` FOREIGN KEY (`member_username`) REFERENCES `Person` (`username`),
  ADD CONSTRAINT `belongto_ibfk_2` FOREIGN KEY (`owner_username`,`groupName`) REFERENCES `Friendgroup` (`groupOwner`, `groupName`);

--
-- Constraints for table `Follow`
--
ALTER TABLE `Follow`
  ADD CONSTRAINT `follow_ibfk_1` FOREIGN KEY (`username_followed`) REFERENCES `Person` (`username`),
  ADD CONSTRAINT `follow_ibfk_2` FOREIGN KEY (`username_follower`) REFERENCES `Person` (`username`);

--
-- Constraints for table `Friendgroup`
--
ALTER TABLE `Friendgroup`
  ADD CONSTRAINT `friendgroup_ibfk_1` FOREIGN KEY (`groupOwner`) REFERENCES `Person` (`username`);

--
-- Constraints for table `Likes`
--
ALTER TABLE `Likes`
  ADD CONSTRAINT `likes_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Person` (`username`),
  ADD CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`photoID`) REFERENCES `Photo` (`photoID`);

--
-- Constraints for table `Photo`
--
ALTER TABLE `Photo`
  ADD CONSTRAINT `photo_ibfk_1` FOREIGN KEY (`photoPoster`) REFERENCES `Person` (`username`);

--
-- Constraints for table `SharedWith`
--
ALTER TABLE `SharedWith`
  ADD CONSTRAINT `sharedwith_ibfk_1` FOREIGN KEY (`groupOwner`,`groupName`) REFERENCES `Friendgroup` (`groupOwner`, `groupName`),
  ADD CONSTRAINT `sharedwith_ibfk_2` FOREIGN KEY (`photoID`) REFERENCES `Photo` (`photoID`);

--
-- Constraints for table `Tagged`
--
ALTER TABLE `Tagged`
  ADD CONSTRAINT `tagged_ibfk_1` FOREIGN KEY (`username`) REFERENCES `Person` (`username`),
  ADD CONSTRAINT `tagged_ibfk_2` FOREIGN KEY (`photoID`) REFERENCES `Photo` (`photoID`);
