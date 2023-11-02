-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema autoqa
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema autoqa
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `autoqa` DEFAULT CHARACTER SET utf8mb3 ;
USE `autoqa` ;

-- -----------------------------------------------------
-- Table `autoqa`.`log`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `autoqa`.`log` (
  `LOG_ID` INT NOT NULL,
  `LOG_NAME` VARCHAR(45) NOT NULL,
  `LOG_PATH` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`LOG_ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `autoqa`.`screenshot`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `autoqa`.`screenshot` (
  `SCREENSHOT_ID` INT NOT NULL AUTO_INCREMENT,
  `SCREENSHOT_NAME` VARCHAR(70) NOT NULL,
  `SCREENSHOT_PATH` VARCHAR(150) NOT NULL,
  `Description` VARCHAR(200) NULL DEFAULT NULL,
  PRIMARY KEY (`SCREENSHOT_ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `autoqa`.`game_information`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `autoqa`.`game_information` (
  `GAME_ID` INT NOT NULL AUTO_INCREMENT,
  `GAME_TITLE` VARCHAR(45) NOT NULL,
  `GAME_VERSION` VARCHAR(45) NOT NULL,
  `GAME_EXECUTION_PATH` VARCHAR(100) NULL DEFAULT NULL,
  `GAME_LOG_PATH` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`GAME_ID`),
  UNIQUE INDEX `GAME_VERSION_INDEX` (`GAME_VERSION` ASC) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `autoqa`.`test_macro`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `autoqa`.`test_macro` (
  `TEST_MACRO_ID` INT NOT NULL,
  `TEST_MACRO_NAME` VARCHAR(45) NOT NULL,
  `TEST_MACRO_PATH` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`TEST_MACRO_ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `autoqa`.`testcase`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `autoqa`.`testcase` (
  `TEST_CASE_ID` INT NOT NULL,
  `TEST_DATE` DATE NOT NULL,
  `TEST_MACRO_ID` INT NOT NULL,
  `GAME_VERSION` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`TEST_CASE_ID`),
  INDEX `TEST_MACRO_ID_idx` (`TEST_MACRO_ID` ASC) VISIBLE,
  INDEX `TEST_GAME_VERSION_idx` (`GAME_VERSION` ASC) VISIBLE,
  CONSTRAINT `TEST_GAME_VERSION`
    FOREIGN KEY (`GAME_VERSION`)
    REFERENCES `autoqa`.`game_information` (`GAME_VERSION`),
  CONSTRAINT `TEST_MACRO_ID`
    FOREIGN KEY (`TEST_MACRO_ID`)
    REFERENCES `autoqa`.`test_macro` (`TEST_MACRO_ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `autoqa`.`bugcase`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `autoqa`.`bugcase` (
  `TEST_CASE_ID` INT NOT NULL,
  `BUG_CASE_ID` INT NOT NULL,
  `BUG_DESCRIPTION` VARCHAR(45) NULL DEFAULT NULL,
  `LOG_ID` INT NULL DEFAULT NULL,
  `SCREENSHOT_ID` INT NULL DEFAULT NULL,
  PRIMARY KEY (`BUG_CASE_ID`),
  INDEX `TEST_CASE_idx` (`TEST_CASE_ID` ASC) VISIBLE,
  INDEX `LOG_ID_idx` (`LOG_ID` ASC) VISIBLE,
  INDEX `SCREENSHOT_ID_idx` (`SCREENSHOT_ID` ASC) VISIBLE,
  CONSTRAINT `LOG_ID`
    FOREIGN KEY (`LOG_ID`)
    REFERENCES `autoqa`.`log` (`LOG_ID`),
  CONSTRAINT `SCREENSHOT_ID`
    FOREIGN KEY (`SCREENSHOT_ID`)
    REFERENCES `autoqa`.`screenshot` (`SCREENSHOT_ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `TEST_CASE`
    FOREIGN KEY (`TEST_CASE_ID`)
    REFERENCES `autoqa`.`testcase` (`TEST_CASE_ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `autoqa`.`case_recommendation`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `autoqa`.`case_recommendation` (
  `CASE_ID` INT NOT NULL,
  `RECOMMENDATION_CASE_ID` INT NOT NULL,
  INDEX `CASE_ID_idx` (`CASE_ID` ASC) VISIBLE,
  CONSTRAINT `CASE_ID`
    FOREIGN KEY (`CASE_ID`)
    REFERENCES `autoqa`.`testcase` (`TEST_CASE_ID`),
  CONSTRAINT `RECOMMEND_CASE_ID`
    FOREIGN KEY (`CASE_ID`)
    REFERENCES `autoqa`.`testcase` (`TEST_CASE_ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `autoqa`.`disposition`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `autoqa`.`disposition` (
  `DISPOSITION_ID` INT NOT NULL,
  `DISPOSITION_NAME` VARCHAR(45) NOT NULL,
  `DISPOSITION_DESCRIPTION` VARCHAR(150) NULL DEFAULT NULL,
  PRIMARY KEY (`DISPOSITION_ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `autoqa`.`manufacture_data_info`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `autoqa`.`manufacture_data_info` (
  `MANUFACTURE_DATA_ID` INT NOT NULL,
  `MANUFACTURE_DATA_NAME` VARCHAR(45) NOT NULL,
  `MANUFACTURE_DATA_PATH` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`MANUFACTURE_DATA_ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `autoqa`.`testcase_disposition`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `autoqa`.`testcase_disposition` (
  `DISPOSITION_ID` INT NOT NULL,
  `TEST_CASE_ID` INT NOT NULL,
  INDEX `DISPOSITION_ID_idx` (`DISPOSITION_ID` ASC) VISIBLE,
  INDEX `TEST_CASE_ID_idx` (`TEST_CASE_ID` ASC) VISIBLE,
  CONSTRAINT `DISPOSITION_ID`
    FOREIGN KEY (`DISPOSITION_ID`)
    REFERENCES `autoqa`.`disposition` (`DISPOSITION_ID`),
  CONSTRAINT `TEST_CASE_ID`
    FOREIGN KEY (`TEST_CASE_ID`)
    REFERENCES `autoqa`.`testcase` (`TEST_CASE_ID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `autoqa`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `autoqa`.`user` (
  `user_code` INT NOT NULL AUTO_INCREMENT,
  `USER_ID` VARCHAR(20) NOT NULL,
  `USER_PASSWORD` VARCHAR(45) NOT NULL,
  `USER_LEVEL` INT NOT NULL DEFAULT '1',
  PRIMARY KEY (`user_code`))
ENGINE = InnoDB
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8mb3;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
