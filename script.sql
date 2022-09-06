-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema salud
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `salud` ;

-- -----------------------------------------------------
-- Schema salud
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `salud` DEFAULT CHARACTER SET utf8 ;
-- -----------------------------------------------------
-- Schema esquema_usuarios
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `esquema_usuarios` ;

-- -----------------------------------------------------
-- Schema esquema_usuarios
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `esquema_usuarios` DEFAULT CHARACTER SET utf8mb3 ;
USE `salud` ;

-- -----------------------------------------------------
-- Table `salud`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `salud`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombres` VARCHAR(150) NULL,
  `apellidos` VARCHAR(150) NULL,
  `email` VARCHAR(150) NULL,
  `password` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `salud`.`pendientes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `salud`.`pendientes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `clase` VARCHAR(45) NULL,
  `fecha` DATE NULL,
  `hora` TIME NULL,
  `lugar` VARCHAR(150) NULL,
  `detalles` TEXT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_pendientes_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_pendientes_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `salud`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `salud`.`examenes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `salud`.`examenes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE NULL,
  `descripcion` TEXT NULL,
  `documento` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_examenes_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_examenes_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `salud`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `salud`.`imagenes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `salud`.`imagenes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE NULL,
  `descripcion` TEXT NULL,
  `documento` VARCHAR(255) NULL,
  `link` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_imagenes_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_imagenes_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `salud`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `salud`.`historias`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `salud`.`historias` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE NULL,
  `origen` VARCHAR(255) NULL,
  `documento` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_historias_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_historias_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `salud`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `salud`.`ordenes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `salud`.`ordenes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `servicio` VARCHAR(255) NULL,
  `prestador` VARCHAR(255) NULL,
  `telefonos` VARCHAR(45) NULL,
  `direccion` VARCHAR(255) NULL,
  `documento` VARCHAR(255) NULL,
  `solicitada` VARCHAR(4) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_ordenes_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_ordenes_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `salud`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `esquema_usuarios` ;

-- -----------------------------------------------------
-- Table `esquema_usuarios`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_usuarios`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(255) NULL DEFAULT NULL,
  `last_name` VARCHAR(255) NULL DEFAULT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
