-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-10-2025 a las 16:37:59
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `crud_flask_python`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carros`
--

CREATE TABLE `carros` (
  `id` int(11) NOT NULL,
  `marca` varchar(45) NOT NULL,
  `modelo` varchar(45) NOT NULL,
  `year` varchar(45) NOT NULL,
  `color` varchar(45) NOT NULL,
  `puertas` varchar(45) NOT NULL,
  `favorito` varchar(45) NOT NULL,
  `foto` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `carros`
--

INSERT INTO `carros` (`id`, `marca`, `modelo`, `year`, `color`, `puertas`, `favorito`, `foto`) VALUES
(1, 'BMW', 'BMW X7', '2022', 'Gris', '4', 'Si', 'R5Q2IZSTU6BVDWL3CA9H.png'),
(2, 'Ford', 'CAMIONETA', '2022', 'Blanco', '4', 'Si', 'ZHKTJE319UCDIB6F7A_5.png'),
(3, 'Chevrolet', 'Onix Turbo', '2013', 'Blanco', '2', 'No', 'IMWSBJD4O1UCA97N_R0P.jpg'),
(7, 'Toyota', 'Avalon', '2018', 'Gris', '2', 'No', '4IQKOW_31NFYL7BU9TPM.png'),
(8, 'Chevrolet', 'Joy HB', '2015', 'Rojo', '4', 'Si', 'Z1UR8IQMVSE3JWDLFNOT.jpg'),
(10, 'Mercedes-Benz', 'CLA Coupé', '2022', 'Blanco', '4', 'Si', 'SM_A2NQ13GZKOW0JIDP9.jpg'),
(14, 'hilux', 'senati', '2010', 'Rojo', '2', 'Si', 'ZSIWXRGUV6AO0TYN_K5L.jpg');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `carros`
--
ALTER TABLE `carros`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `carros`
--
ALTER TABLE `carros`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
