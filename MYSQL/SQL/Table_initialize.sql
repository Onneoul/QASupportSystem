-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema AutoQA
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema AutoQA
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `AutoQA` DEFAULT CHARACTER SET utf8 ;
USE `AutoQA` ;

-- -----------------------------------------------------
-- Table `AutoQA`.`GAME_INFORMATION`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AutoQA`.`GAME_INFORMATION` (
  `GAME_ID` INT NOT NULL auto_increment,
  `GAME_TITLE` VARCHAR(45) NOT NULL,
  `GAME_VERSION` VARCHAR(45) NOT NULL,
  `GAME_EXECUTION_PATH` VARCHAR(100) NULL,
  `GAME_LOG_PATH` VARCHAR(45) NULL,
  PRIMARY KEY (`GAME_ID`),
  UNIQUE INDEX `GAME_VERSION_INDEX` (`GAME_VERSION` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AutoQA`.`TEST_MACRO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AutoQA`.`TEST_MACRO` (
  `TEST_MACRO_ID` INT NOT NULL auto_increment,
  `TEST_MACRO_NAME` VARCHAR(45) NOT NULL,
  `TEST_MACRO_PATH` VARCHAR(45) NULL,
  `GAME_VERSION` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`TEST_MACRO_ID`),
  INDEX `MACRO_GAME_VERSION_idx` (`GAME_VERSION` ASC) VISIBLE,
  CONSTRAINT `MACRO_GAME_VERSION`
    FOREIGN KEY (`GAME_VERSION`)
    REFERENCES `AutoQA`.`GAME_INFORMATION` (`GAME_VERSION`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AutoQA`.`USER`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AutoQA`.`USER` (
  `USER_CODE` INT NOT NULL,
  `USER_ID` VARCHAR(20) NOT NULL,
  `USER_PASSWORD` VARCHAR(45) NOT NULL,
  `USER_LEVEL` INT NOT NULL DEFAULT 1 COMMENT 'Level 1 = normal user\nLevel 2 = high level user\nLevel 3 = Administrator',
  PRIMARY KEY (`USER_CODE`),
  UNIQUE INDEX `USER_LEVEL_UNIQUE` (`USER_LEVEL` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AutoQA`.`TESTCASE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AutoQA`.`TESTCASE` (
  `TEST_CASE_ID` INT NOT NULL auto_increment,
  `TEST_DATE` DATE NOT NULL,
  `TEST_MACRO_ID` INT NULL,
  `GAME_VERSION` VARCHAR(45) NOT NULL,
  `USER_CODE` INT NOT NULL,
  PRIMARY KEY (`TEST_CASE_ID`),
  INDEX `TEST_MACRO_ID_idx` (`TEST_MACRO_ID` ASC) VISIBLE,
  INDEX `TEST_GAME_VERSION_idx` (`GAME_VERSION` ASC) VISIBLE,
  INDEX `TEST_CASE_USER_idx` (`USER_CODE` ASC) VISIBLE,
  UNIQUE INDEX `TEST_CASE_ID_UNIQUE` (`TEST_CASE_ID` ASC) VISIBLE,
  CONSTRAINT `TEST_MACRO_ID`
    FOREIGN KEY (`TEST_MACRO_ID`)
    REFERENCES `AutoQA`.`TEST_MACRO` (`TEST_MACRO_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `TEST_GAME_VERSION`
    FOREIGN KEY (`GAME_VERSION`)
    REFERENCES `AutoQA`.`GAME_INFORMATION` (`GAME_VERSION`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `TEST_CASE_USER`
    FOREIGN KEY (`USER_CODE`)
    REFERENCES `AutoQA`.`USER` (`USER_CODE`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 1
ROW_FORMAT = DEFAULT;


-- -----------------------------------------------------
-- Table `AutoQA`.`DISPOSITION`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AutoQA`.`DISPOSITION` (
  `DISPOSITION_ID` INT NOT NULL auto_increment,
  `DISPOSITION_NAME` VARCHAR(45) NOT NULL,
  `DISPOSITION_DESCRIPTION` VARCHAR(150) NULL,
  PRIMARY KEY (`DISPOSITION_ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AutoQA`.`TESTCASE_DISPOSITION`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AutoQA`.`TESTCASE_DISPOSITION` (
  `DISPOSITION_ID` INT NOT NULL,
  `TEST_CASE_ID` INT NOT NULL,
  INDEX `DISPOSITION_ID_idx` (`DISPOSITION_ID` ASC) VISIBLE,
  INDEX `TEST_CASE_ID_idx` (`TEST_CASE_ID` ASC) VISIBLE,
  CONSTRAINT `DISPOSITION_ID`
    FOREIGN KEY (`DISPOSITION_ID`)
    REFERENCES `AutoQA`.`DISPOSITION` (`DISPOSITION_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `TEST_CASE_ID`
    FOREIGN KEY (`TEST_CASE_ID`)
    REFERENCES `AutoQA`.`TESTCASE` (`TEST_CASE_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AutoQA`.`LOG`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AutoQA`.`LOG` (
  `LOG_ID` INT NOT NULL auto_increment,
  `LOG_NAME` VARCHAR(45) NOT NULL,
  `LOG_PATH` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`LOG_ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AutoQA`.`SCREENSHOT`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AutoQA`.`SCREENSHOT` (
  `SCREENSHOT_ID` INT NOT NULL AUTO_INCREMENT,
  `SCREENSHOT_NAME` VARCHAR(70) NOT NULL,
  `SCREENSHOT_PATH` VARCHAR(150) NOT NULL,
  `Description` VARCHAR(200) NULL,
  PRIMARY KEY (`SCREENSHOT_ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AutoQA`.`BUGCASE`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AutoQA`.`BUGCASE` (
  `TEST_CASE_ID` INT NOT NULL,
  `BUG_CASE_ID` INT NOT NULL,
  `BUG_DESCRIPTION` VARCHAR(45) NULL,
  `LOG_ID` INT NULL,
  `SCREENSHOT_ID` INT NULL,
  PRIMARY KEY (`BUG_CASE_ID`),
  INDEX `TEST_CASE_idx` (`TEST_CASE_ID` ASC) VISIBLE,
  INDEX `LOG_ID_idx` (`LOG_ID` ASC) VISIBLE,
  INDEX `SCREENSHOT_ID_idx` (`SCREENSHOT_ID` ASC) VISIBLE,
  CONSTRAINT `TEST_CASE`
    FOREIGN KEY (`TEST_CASE_ID`)
    REFERENCES `AutoQA`.`TESTCASE` (`TEST_CASE_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `LOG_ID`
    FOREIGN KEY (`LOG_ID`)
    REFERENCES `AutoQA`.`LOG` (`LOG_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `SCREENSHOT_ID`
    FOREIGN KEY (`SCREENSHOT_ID`)
    REFERENCES `AutoQA`.`SCREENSHOT` (`SCREENSHOT_ID`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AutoQA`.`CASE_RECOMMENDATION`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AutoQA`.`CASE_RECOMMENDATION` (
  `CASE_ID` INT NOT NULL,
  `RECOMMENDATION_CASE_ID` INT NOT NULL,
  INDEX `CASE_ID_idx` (`CASE_ID` ASC) VISIBLE,
  CONSTRAINT `CASE_ID`
    FOREIGN KEY (`CASE_ID`)
    REFERENCES `AutoQA`.`TESTCASE` (`TEST_CASE_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `RECOMMEND_CASE_ID`
    FOREIGN KEY (`CASE_ID`)
    REFERENCES `AutoQA`.`TESTCASE` (`TEST_CASE_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AutoQA`.`MANUFACTURE_DATA_INFO`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AutoQA`.`MANUFACTURE_DATA_INFO` (
  `MANUFACTURE_DATA_ID` INT NOT NULL,
  `MANUFACTURE_DATA_NAME` VARCHAR(45) NOT NULL,
  `MANUFACTURE_DATA_PATH` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`MANUFACTURE_DATA_ID`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `AutoQA`.`MANUFACTURE_DATA`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `AutoQA`.`MANUFACTURE_DATA` (
  `TEST_CASE_ID` INT NOT NULL,
  `MANUFACTURE_DATA_ID` INT NOT NULL,
  INDEX `MANUFACTURE_DATA_idx` (`MANUFACTURE_DATA_ID` ASC) VISIBLE,
  INDEX `CASE_ID_idx` (`TEST_CASE_ID` ASC) INVISIBLE,
  CONSTRAINT `CASE_ID`
    FOREIGN KEY (`TEST_CASE_ID`)
    REFERENCES `AutoQA`.`TESTCASE` (`TEST_CASE_ID`)
    ON DELETE NO ACTION
    ON UPDATE CASCADE,
  CONSTRAINT `MANUFACTURE_DATA`
    FOREIGN KEY (`MANUFACTURE_DATA_ID`)
    REFERENCES `AutoQA`.`MANUFACTURE_DATA_INFO` (`MANUFACTURE_DATA_ID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;