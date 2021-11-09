-- phpMyAdmin SQL Dump
-- version 4.4.15.9
-- https://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 09, 2021 at 02:33 AM
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
-- Table structure for table `menu`
--

CREATE TABLE IF NOT EXISTS `menu` (
  `menu_id` int(12) NOT NULL,
  `dish_name` varchar(100) DEFAULT NULL,
  `price` float NOT NULL,
  `size` varchar(10) DEFAULT NULL,
  `description` varchar(250) DEFAULT '',
  `category` varchar(100) DEFAULT NULL
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `menu`
--

INSERT INTO `menu` (`menu_id`, `dish_name`, `price`, `size`, `description`, `category`) VALUES
(2, 'Vegetable Springs Rolls (2pcs)', 2.95, NULL, NULL, 'APPETIZERS'),
(3, 'Wonton Soup', 2.75, 'Small', NULL, 'SOUPS'),
(4, 'Wonton Soup', 4.95, 'Large', NULL, 'SOUPS'),
(5, 'Fish Ball Noodle Soup', 9.95, NULL, NULL, 'NOODLE SOUPS'),
(6, 'Vegetable Fried Rice', 5.95, 'Pt.', NULL, 'FRIED RICE'),
(7, 'Vegetable Fried Rice', 8.95, 'Qt.', NULL, 'FRIED RICE'),
(8, 'Vegetable Chow Mein', 5.95, 'Pt.', 'Served w/ white rice & fried noodle', 'CHOW MEIN'),
(9, 'Vegetable Chow Mein', 8.95, 'Qt.', 'Served w/ white rice & fried noodle', 'CHOW MEIN');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`menu_id`),
  ADD KEY `size` (`size`),
  ADD KEY `category` (`category`);

--
-- AUTO_INCREMENT for dumped tables
--

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
