-- phpMyAdmin SQL Dump
-- version 4.4.15.9
-- https://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 13, 2021 at 05:09 AM
-- Server version: 5.6.37
-- PHP Version: 5.6.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `restaurant`
--

-- --------------------------------------------------------

--
-- Table structure for table `account`
--

CREATE TABLE IF NOT EXISTS `account` (
  `account_id` int(12) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `phone` varchar(14) NOT NULL,
  `address` varchar(250) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(250) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`account_id`, `first_name`, `last_name`, `phone`, `address`, `email`, `password`) VALUES
(1, 'Testfirst', 'Testlast', '1112223344', 'test# testrd teststate 00000', 'testaccount@test.com', 'testpass1234');

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE IF NOT EXISTS `categories` (
  `category` varchar(100) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`category`) VALUES
('APPETIZERS'),
('BEEF'),
('CHICKEN'),
('CHOW MEIN'),
('DIET MENU SPECIAL'),
('EGG FOO YOUNG'),
('FRIED RICE'),
('HO FUN OR MEI FUN'),
('KY LIN CHEF SUGGESTIONS'),
('LO MEIN'),
('NOODLE SOUPS'),
('PAN FRIED EGG NOODLE'),
('PORK'),
('SEAFOOD'),
('SIDE ORDERS & DRINKS'),
('SOUPS'),
('SPECIAL PLATTER'),
('SWEET & SOUR'),
('VEGETABLES & BEAN CURD');

-- --------------------------------------------------------

--
-- Table structure for table `menu`
--

CREATE TABLE IF NOT EXISTS `menu` (
  `menu_id` int(12) NOT NULL,
  `dish_name` varchar(100) DEFAULT NULL,
  `price` float NOT NULL,
  `size` varchar(10) DEFAULT NULL,
  `options` int(11) DEFAULT NULL,
  `description` varchar(250) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `menu`
--

INSERT INTO `menu` (`menu_id`, `dish_name`, `price`, `size`, `options`, `description`, `category`) VALUES
(2, 'Vegetable Springs Rolls (2pcs)', 2.95, NULL, NULL, NULL, 'APPETIZERS'),
(3, 'Wonton Soup', 2.75, 'Small', NULL, NULL, 'SOUPS'),
(4, 'Wonton Soup', 4.95, 'Large', NULL, NULL, 'SOUPS'),
(5, 'Fish Ball Noodle Soup', 9.95, NULL, NULL, NULL, 'NOODLE SOUPS'),
(6, 'Vegetable Fried Rice', 5.95, 'Pt.', NULL, NULL, 'FRIED RICE'),
(7, 'Vegetable Fried Rice', 8.95, 'Qt.', NULL, NULL, 'FRIED RICE'),
(8, 'Vegetable Chow Mein', 5.95, 'Pt.', NULL, 'Served w/ white rice & fried noodle', 'CHOW MEIN'),
(9, 'Vegetable Chow Mein', 8.95, 'Qt.', NULL, 'Served w/ white rice & fried noodle', 'CHOW MEIN');

-- --------------------------------------------------------

--
-- Table structure for table `sizes`
--

CREATE TABLE IF NOT EXISTS `sizes` (
  `size` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `sizes`
--

INSERT INTO `sizes` (`size`) VALUES
('Large'),
('Pt.'),
('Qt.'),
('Small');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`account_id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`category`);

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`menu_id`),
  ADD KEY `size` (`size`),
  ADD KEY `category` (`category`);

--
-- Indexes for table `sizes`
--
ALTER TABLE `sizes`
  ADD PRIMARY KEY (`size`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account`
--
ALTER TABLE `account`
  MODIFY `account_id` int(12) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `menu`
--
ALTER TABLE `menu`
  MODIFY `menu_id` int(12) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=10;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `menu`
--
ALTER TABLE `menu`
  ADD CONSTRAINT `menu_ibfk_1` FOREIGN KEY (`size`) REFERENCES `sizes` (`size`),
  ADD CONSTRAINT `menu_ibfk_2` FOREIGN KEY (`category`) REFERENCES `categories` (`category`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
