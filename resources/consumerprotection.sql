-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 11, 2021 at 04:44 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `consumerprotection`
--

-- --------------------------------------------------------

--
-- Table structure for table `organization`
--

CREATE TABLE `organization` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `logo` varchar(255) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `shop_type_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `organization`
--

INSERT INTO `organization` (`id`, `name`, `logo`, `description`, `is_active`, `created_at`, `updated_at`, `user_id`, `category_id`, `shop_type_id`) VALUES
(13, 'Name', '40_org_PXL_20210420_120555753.jpg', 'test feedback on this one is so much', 1, 1, 1, 40, 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `report`
--

CREATE TABLE `report` (
  `id` int(255) NOT NULL,
  `uid` int(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  `is_active` tinyint(4) NOT NULL,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `report`
--

INSERT INTO `report` (`id`, `uid`, `name`, `email`, `title`, `description`, `url`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 40, 'Charitha', 'eyepaxapps@gmail.com', 'Test', 'tested positive for the test results and test it out and test it out and test it out and test it out and test it tttttt', '', 1, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `shop`
--

CREATE TABLE `shop` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phonenumber` varchar(255) DEFAULT NULL,
  `organization_id` int(11) NOT NULL,
  `location` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `shop`
--

INSERT INTO `shop` (`id`, `name`, `address`, `phonenumber`, `organization_id`, `location`, `is_active`, `created_at`, `updated_at`) VALUES
(15, 'Pizza Hut - Malabe', 'WX32+R4Q, Malabe, Sri Lanka.', '0771119961', 13, '{\"lat\":6.9045917,\"lon\":79.9503526}', 1, 1, 1),
(16, 'Pizza Hut - Battaramulla', '17 Battaramulla - Pannipitiya Road, Battaramulla, Sri Lanka.[10120]', '0771119962', 13, '{\"lat\":6.9020335,\"lon\":79.9201666}', 1, 1, 1),
(17, 'Ggg', 'Malabe, Malabe, Sri Lanka.[10115]', '0771119961', 13, '{\"lat\":6.9078482999999995,\"lon\":79.94740870000001}', 1, 1, 1),
(18, 'Ddd', 'Salmal Uyana Bus Stop, Sri Lanka.', '0771119963', 13, '{\"lat\":6.9210612,\"lon\":79.9481266}', 1, 1, 1),
(19, 'Ttt', '86 Robert Gunawardena Mawatha, Susitha Pura, Sri Lanka.', '0778881125', 13, '{\"lat\":6.9047624999999995,\"lon\":79.9568955}', 1, 1, 1),
(20, 'Pizza Hut- Rajagiriya', '157 Kotte - Bope Road, Sri Jayawardenepura Kotte, Sri Lanka.[10120]', '0771119965', 13, '{\"lat\":6.9023506999999995,\"lon\":79.9140299}', 1, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `shop_type`
--

CREATE TABLE `shop_type` (
  `id` int(11) NOT NULL,
  `type` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `shop_type`
--

INSERT INTO `shop_type` (`id`, `type`, `is_active`) VALUES
(0, 'Type 1', 1),
(1, 'Type 2', 1);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `uid` varchar(255) NOT NULL,
  `user_type` int(11) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone_number` varchar(45) NOT NULL,
  `birth_day` int(11) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `gender` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `uid`, `user_type`, `full_name`, `email`, `password`, `phone_number`, `birth_day`, `address`, `gender`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 'dc5c5cde1a323dcbbad73c524e436e86', 0, 'Charitha Ratnayake', 'jachratnayake@gmail.com', '3dbe00a167653a1aaee01d93e77e730e', '0771119961', 672192000, 'Thlahena Malabe', 0, 1, 1591440397, 1591440397),
(2, '22fb9e79a87411ff17e263cb1429c554', 1, 'Charitha Seller', 'jach@gmail.com', '3dbe00a167653a1aaee01d93e77e730e', '0771119962', 672192000, 'Thlahena Malabe', 0, 1, 1591440624, 1591440624),
(28, '7ba9b512de6a7e41f37b93bddc22925d', 0, 'Charitha Ratnayake', 'jq2awe@gmail.com', 'e10adc3949ba59abbe56e057f20f883e', '0727118291', 0, '0771119961', 0, 1, 1, 1),
(40, 'd10ca8d11301c2f4993ac2279ce4b930', 0, '', 'a@a.com', '3dbe00a167653a1aaee01d93e77e730e', '0771119963', 0, '0', 0, 1, 1, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `organization`
--
ALTER TABLE `organization`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `fk_organization_user1_idx` (`user_id`),
  ADD KEY `fk_organization_shop_type1_idx` (`shop_type_id`);

--
-- Indexes for table `report`
--
ALTER TABLE `report`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `shop`
--
ALTER TABLE `shop`
  ADD PRIMARY KEY (`id`),
  ADD KEY `shop_org` (`organization_id`);

--
-- Indexes for table `shop_type`
--
ALTER TABLE `shop_type`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id_UNIQUE` (`id`),
  ADD UNIQUE KEY `email_UNIQUE` (`email`),
  ADD UNIQUE KEY `phone_number_UNIQUE` (`phone_number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `organization`
--
ALTER TABLE `organization`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `report`
--
ALTER TABLE `report`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `shop`
--
ALTER TABLE `shop`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `organization`
--
ALTER TABLE `organization`
  ADD CONSTRAINT `organization_ibfk_2` FOREIGN KEY (`shop_type_id`) REFERENCES `shop_type` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `shop`
--
ALTER TABLE `shop`
  ADD CONSTRAINT `shop_org` FOREIGN KEY (`organization_id`) REFERENCES `organization` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
