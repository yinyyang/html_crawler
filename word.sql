/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50724
 Source Host           : localhost:3306
 Source Schema         : word

 Target Server Type    : MySQL
 Target Server Version : 50724
 File Encoding         : 65001

 Date: 22/08/2019 17:30:28
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for word
-- ----------------------------
DROP TABLE IF EXISTS `word`;
CREATE TABLE `word`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `word_idx` int(11) NULL DEFAULT NULL,
  `english` varchar(500) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_bin ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for word_ext
-- ----------------------------
DROP TABLE IF EXISTS `word_ext`;
CREATE TABLE `word_ext`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `word_idx` int(11) NULL DEFAULT NULL,
  `chinese` longtext CHARACTER SET utf8 COLLATE utf8_bin NULL,
  `lodoce` longtext CHARACTER SET utf8 COLLATE utf8_bin NULL,
  `formation` text CHARACTER SET utf8 COLLATE utf8_bin NULL,
  `soundmark` text CHARACTER SET utf8 COLLATE utf8_bin NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_bin ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
