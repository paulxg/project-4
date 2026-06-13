-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 13, 2026 at 10:56 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `projekt_4_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `tickets`
--

CREATE TABLE `tickets` (
  `ticket_number` int(11) NOT NULL,
  `user_id_ref` int(10) UNSIGNED NOT NULL,
  `factor` decimal(10,0) DEFAULT NULL,
  `date_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `category` varchar(45) NOT NULL,
  `short_description` varchar(100) NOT NULL,
  `long_description` varchar(255) NOT NULL,
  `comment` text NOT NULL,
  `status` text NOT NULL,
  `handled_by` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tickets`
--

INSERT INTO `tickets` (`ticket_number`, `user_id_ref`, `factor`, `date_time`, `category`, `short_description`, `long_description`, `comment`, `status`, `handled_by`) VALUES
(37, 3, 5, '2026-06-12 12:20:59', 'Installation or Updates', 'Test', 'akdwbaid awdda', '', 'in progress', 'Paul'),
(38, 3, 5, '2026-06-12 12:22:25', 'Installation or Updates', 'Test 2', '', '', 'in progress', 'Lorena');

-- --------------------------------------------------------

--
-- Table structure for table `ticket_messages`
--

CREATE TABLE `ticket_messages` (
  `id` int(11) NOT NULL,
  `ticket_id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ticket_messages`
--

INSERT INTO `ticket_messages` (`id`, `ticket_id`, `sender_id`, `message`, `timestamp`) VALUES
(1, 17, 2, 'Anton?', '2026-05-30 23:25:19'),
(2, 20, 2, 'rwaddawdad', '2026-05-30 23:26:36'),
(3, 20, 3, 'PAULLLLL', '2026-05-30 23:27:06'),
(4, 19, 2, 'test', '2026-05-31 00:09:26'),
(5, 19, 2, 'ja passt wa', '2026-05-31 00:36:53'),
(6, 23, 2, 'jop', '2026-05-31 11:32:23'),
(7, 24, 2, 'Lorena ist cool', '2026-05-31 12:20:08'),
(8, 24, 2, 'aiwfuhaoifuahfiawhf', '2026-05-31 12:20:29'),
(9, 25, 3, 'Mir fällt ein, dass ......', '2026-05-31 12:22:21'),
(10, 25, 2, 'ja tolle idee!', '2026-05-31 12:22:38'),
(11, 25, 2, 'Final erledigt!', '2026-05-31 12:22:54'),
(12, 35, 2, 'awdawd', '2026-05-31 14:40:05'),
(13, 36, 2, 'Info Anfrage', '2026-06-12 14:17:49'),
(14, 36, 2, 'adawdwda', '2026-06-12 14:53:15');

-- --------------------------------------------------------

--
-- Table structure for table `userdata`
--

CREATE TABLE `userdata` (
  `id` int(10) UNSIGNED NOT NULL,
  `username` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `rank` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `userdata`
--

INSERT INTO `userdata` (`id`, `username`, `password`, `rank`, `status`) VALUES
(1, 'Lorena', '1234', 'admin', 'company'),
(2, 'Paul', '1234', 'admin', 'private'),
(3, 'Anton', '1234', 'user', 'private'),
(23, 'company', '1', 'user', 'company'),
(24, 'private', '1', 'user', 'private');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tickets`
--
ALTER TABLE `tickets`
  ADD PRIMARY KEY (`ticket_number`),
  ADD KEY `user_id_ref_idx` (`user_id_ref`);

--
-- Indexes for table `ticket_messages`
--
ALTER TABLE `ticket_messages`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `userdata`
--
ALTER TABLE `userdata`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tickets`
--
ALTER TABLE `tickets`
  MODIFY `ticket_number` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

--
-- AUTO_INCREMENT for table `ticket_messages`
--
ALTER TABLE `ticket_messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `userdata`
--
ALTER TABLE `userdata`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tickets`
--
ALTER TABLE `tickets`
  ADD CONSTRAINT `user_id_ref` FOREIGN KEY (`user_id_ref`) REFERENCES `userdata` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
