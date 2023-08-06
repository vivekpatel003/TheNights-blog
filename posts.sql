-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 06, 2023 at 02:34 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `thenights`
--

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE `posts` (
  `serialNo` int(11) NOT NULL,
  `title` text NOT NULL,
  `slug` varchar(25) NOT NULL,
  `content` text NOT NULL,
  `img_url` varchar(50) NOT NULL,
  `subtitle` varchar(50) NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `posts`
--

INSERT INTO `posts` (`serialNo`, `title`, `slug`, `content`, `img_url`, `subtitle`, `date`) VALUES
(1, 'Naruto once said..', 'blog-one', 'IF YOU DON’T LIKE THE HAND THAT FATE’S DEALT YOU WITH, FIGHT FOR A NEW ONE.', 'img/post-sample-image.jpg', 'Anime Po', '2023-08-01 13:44:06'),
(3, 'Are certain fruits healthier than others?', 'blog-three', 'Most people have heard the nutritional recommendation to eat five servings of fruit per day. But are some fruits better for you than others? Is it okay to eat dried or frozen fruit, or to drink fruit juice? Does it have to be organic?', 'img/fruits.jpg', 'Nutrition', '2023-07-26 13:36:01'),
(4, 'Creating communities that help support neurodiverse children', 'blog-four', 'For neurodiverse children and their families, the landscape of friendships and social spaces can feel unwelcoming. Being more inclusive is a positive step, yet it takes more to create communities where everyone feels they belong.', 'img/child-health.jpg', 'Child & Teen Health', '2023-07-17 13:37:01');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `posts`
--
ALTER TABLE `posts`
  ADD PRIMARY KEY (`serialNo`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `posts`
--
ALTER TABLE `posts`
  MODIFY `serialNo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
