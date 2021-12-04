-- phpMyAdmin SQL Dump
-- version 4.4.15.9
-- https://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 04, 2021 at 02:53 AM
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
  `password` varchar(250) NOT NULL,
  `admin` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `account`
--

INSERT INTO `account` (`account_id`, `first_name`, `last_name`, `phone`, `address`, `email`, `password`, `admin`) VALUES
(1, 'Testfirst', 'Testlast', '1112223344', 'test# testrd teststate 00000', 'testaccount@test.com', 'testpass1234', 0),
(2, 'admin', 'admin', '0123456789', '123 admin address', 'admin@aol.com', 'admin', 1);

-- --------------------------------------------------------

--
-- Table structure for table `item_for_order`
--

CREATE TABLE IF NOT EXISTS `item_for_order` (
  `itemorder_id` int(12) NOT NULL,
  `order_id` int(12) NOT NULL,
  `menu_id` int(12) NOT NULL,
  `quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `menu`
--

CREATE TABLE IF NOT EXISTS `menu` (
  `menu_id` int(12) NOT NULL,
  `dish_name` varchar(100) DEFAULT NULL,
  `price` float NOT NULL,
  `description` varchar(250) DEFAULT ''
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `menu`
--

INSERT INTO `menu` (`menu_id`, `dish_name`, `price`, `description`) VALUES
(2, 'Vegetable Springs Rolls (2pcs)', 2.95, NULL),
(3, 'Wonton Soup', 2.75, NULL),
(4, 'Wonton Soup', 4.95, NULL),
(5, 'Fish Ball Noodle Soup', 9.95, NULL),
(6, 'Vegetable Fried Rice', 5.95, NULL),
(7, 'Vegetable Fried Rice', 8.95, NULL),
(8, 'Vegetable Chow Mein', 5.95, 'Served w/ white rice & fried noodle'),
(9, 'Vegetable Chow Mein', 8.95, 'Served w/ white rice & fried noodle');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE IF NOT EXISTS `orders` (
  `order_id` int(12) NOT NULL,
  `itemorder_id` int(12) NOT NULL,
  `account_id` int(12) NOT NULL,
  `time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `payment`
--

CREATE TABLE IF NOT EXISTS `payment` (
  `card_number` int(20) NOT NULL,
  `account_id` int(12) NOT NULL,
  `card_code` int(4) NOT NULL,
  `card_expdate` date NOT NULL,
  `cardholder_name` varchar(100) NOT NULL,
  `cardholder_zip` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`account_id`);

--
-- Indexes for table `item_for_order`
--
ALTER TABLE `item_for_order`
  ADD PRIMARY KEY (`itemorder_id`),
  ADD KEY `ifo_FK1` (`menu_id`),
  ADD KEY `ifo_FK2` (`order_id`);

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`menu_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `orders_FK1` (`itemorder_id`),
  ADD KEY `orders_FK2` (`account_id`);

--
-- Indexes for table `payment`
--
ALTER TABLE `payment`
  ADD PRIMARY KEY (`card_number`,`account_id`),
  ADD KEY `payment_FK1` (`account_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `account`
--
ALTER TABLE `account`
  MODIFY `account_id` int(12) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `item_for_order`
--
ALTER TABLE `item_for_order`
  MODIFY `itemorder_id` int(12) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `menu`
--
ALTER TABLE `menu`
  MODIFY `menu_id` int(12) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=10;
--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(12) NOT NULL AUTO_INCREMENT;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `item_for_order`
--
ALTER TABLE `item_for_order`
  ADD CONSTRAINT `ifo_FK1` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`menu_id`),
  ADD CONSTRAINT `ifo_FK2` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`);

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_FK1` FOREIGN KEY (`itemorder_id`) REFERENCES `item_for_order` (`itemorder_id`),
  ADD CONSTRAINT `orders_FK2` FOREIGN KEY (`account_id`) REFERENCES `account` (`account_id`);

--
-- Constraints for table `payment`
--
ALTER TABLE `payment`
  ADD CONSTRAINT `payment_FK1` FOREIGN KEY (`account_id`) REFERENCES `account` (`account_id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
