-- MySQL dump 10.13  Distrib 5.6.24, for Win32 (x86)
--
-- Host: localhost    Database: app_sharephotos
-- ------------------------------------------------------
-- Server version	5.6.24

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--


--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissi_permission_id_23962d04_fk_auth_permission_id` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--



--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`)
) ENGINE=MyISAM AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add tb_photo_info',7,'add_tb_photo_info'),(20,'Can change tb_photo_info',7,'change_tb_photo_info'),(21,'Can delete tb_photo_info',7,'delete_tb_photo_info'),(22,'Can add tb_tag',8,'add_tb_tag'),(23,'Can change tb_tag',8,'change_tb_tag'),(24,'Can delete tb_tag',8,'delete_tb_tag');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;


--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--



--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_30a071c9_fk_auth_group_id` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--


--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_perm_permission_id_3d7071f0_fk_auth_permission_id` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--



--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin__content_type_id_5151027a_fk_django_content_type_id` (`content_type_id`),
  KEY `django_admin_log_user_id_1c5f563_fk_auth_user_id` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--


--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_3ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'auth','permission'),(3,'auth','group'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(7,'sharephotos','tb_photo_info'),(8,'sharephotos','tb_tag');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;


--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2015-12-25 16:42:16'),(2,'auth','0001_initial','2015-12-25 16:42:16'),(3,'admin','0001_initial','2015-12-25 16:42:16'),(4,'contenttypes','0002_remove_content_type_name','2015-12-25 16:42:16'),(5,'auth','0002_alter_permission_name_max_length','2015-12-25 16:42:16'),(6,'auth','0003_alter_user_email_max_length','2015-12-25 16:42:16'),(7,'auth','0004_alter_user_username_opts','2015-12-25 16:42:16'),(8,'auth','0005_alter_user_last_login_null','2015-12-25 16:42:16'),(9,'auth','0006_require_contenttypes_0002','2015-12-25 16:42:16'),(10,'sessions','0001_initial','2015-12-25 16:42:16'),(11,'sharephotos','0001_initial','2015-12-26 07:33:42'),(12,'sharephotos','0002_auto_20151226_1611','2015-12-26 08:38:10'),(13,'sharephotos','0003_auto_20151226_1615','2015-12-26 08:38:10'),(14,'sharephotos','0004_auto_20151226_1615','2015-12-26 08:38:10'),(15,'sharephotos','0005_auto_20151226_1617','2015-12-26 08:38:10'),(16,'sharephotos','0006_auto_20151226_1619','2015-12-26 08:38:10'),(17,'sharephotos','0007_remove_tb_photo_info_store_url','2015-12-26 08:38:10'),(18,'sharephotos','0008_tb_photo_info_store_url','2015-12-26 08:38:10'),(19,'sharephotos','0009_auto_20151226_1640','2015-12-26 08:40:43'),(20,'sharephotos','0010_remove_tb_photo_info_store_url','2015-12-26 08:44:08'),(21,'sharephotos','0011_tb_photo_info_store_url','2015-12-26 08:45:06'),(22,'sharephotos','0012_auto_20151227_1538','2015-12-27 07:38:56');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;


--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--


--
-- Table structure for table `sharephotos_tb_photo_info`
--

DROP TABLE IF EXISTS `sharephotos_tb_photo_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sharephotos_tb_photo_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` longtext NOT NULL,
  `upload_time` datetime NOT NULL,
  `store_url` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sharephotos_tb_photo_info`
--

/*!40000 ALTER TABLE `sharephotos_tb_photo_info` DISABLE KEYS */;
INSERT INTO `sharephotos_tb_photo_info` VALUES (1,'描述','2015-12-26 08:45:24','http://sinacloud.net/sharephotos/Sat%20Dec%2026%2016%3A45%3A23%202015?Expires=1451119824&ssig=FbWUuLfwmg&KID=sina%2C1cjfyo5kQPdnsI3cUc6W'),(2,'P站表情','2015-12-26 08:52:33','http://sinacloud.net/sharephotos/Sat%20Dec%2026%2016%3A52%3A32%202015?Expires=1451120253&ssig=Vf8dF%2F9p20&KID=sina%2C1cjfyo5kQPdnsI3cUc6W'),(3,'描述1','2015-12-26 09:14:22','http://sinacloud.net/sharephotos/Sat%20Dec%2026%2017%3A14%3A21%202015?Expires=1451121562&ssig=72vGD67Os9&KID=sina%2C1cjfyo5kQPdnsI3cUc6W'),(4,'阿狸表情','2015-12-26 10:05:41','http://sinacloud.net/sharephotos/Sat%20Dec%2026%2018%3A05%3A38%202015?Expires=1451124641&ssig=FYp8iTxotD&KID=sina%2C1cjfyo5kQPdnsI3cUc6W'),(5,'楪祈壁纸','2015-12-26 10:07:52','http://sinacloud.net/sharephotos/Sat%20Dec%2026%2018%3A07%3A51%202015?Expires=1451124772&ssig=u1j38%2B1oBQ&KID=sina%2C1cjfyo5kQPdnsI3cUc6W'),(6,'一只小猫','2015-12-26 11:03:44','http://sinacloud.net/sharephotos/Sat%20Dec%2026%2019%3A03%3A43%202015.jpg?Expires=1451128124&ssig=u0CrOAxp%2FS&KID=sina%2C1cjfyo5kQPdnsI3cUc6W'),(7,'白花','2015-12-26 11:45:21','http://sinacloud.net/sharephotos/Sat%20Dec%2026%2019%3A45%3A17%202015.jpg?formatter=json'),(8,'海边风景','2015-12-26 13:37:12','http://sinacloud.net/sharephotos/Sat%20Dec%2026%2021%3A37%3A09%202015.jpg?Expires=1451137332&ssig=VE131D52Mn&KID=sina%2C1cjfyo5kQPdnsI3cUc6W'),(9,'晚上的风景','2015-12-26 13:37:31','http://sinacloud.net/sharephotos/Sat%20Dec%2026%2021%3A37%3A30%202015.jpg?Expires=1451137351&ssig=%2BFMpc4k69E&KID=sina%2C1cjfyo5kQPdnsI3cUc6W'),(10,'一艘小船','2015-12-26 15:38:30','http://sinacloud.net/sharephotos/Sat%20Dec%2026%2023%3A38%3A25%202015.jpg?formatter=json'),(11,'晚上的山峰','2015-12-26 16:49:09','http://sinacloud.net/sharephotos/Sun%20Dec%2027%2000%3A49%3A05%202015.jpg?formatter=json'),(12,'兔斯基','2015-12-27 07:09:27','http://sinacloud.net/sharephotos/Sun%20Dec%2027%2015%3A09%3A25%202015.jpg?formatter=json'),(13,'初音','2015-12-27 07:10:20','http://sinacloud.net/sharephotos/Sun%20Dec%2027%2015%3A10%3A18%202015.jpg?formatter=json'),(14,'楪祈  小提琴','2015-12-27 07:46:51','http://sinacloud.net/sharephotos/Sun%20Dec%2027%2015%3A46%3A41%202015.jpg?formatter=json'),(15,'楪祈  小提琴','2015-12-27 07:48:21','http://sinacloud.net/sharephotos/Sun%20Dec%2027%2015%3A48%3A07%202015.jpg?formatter=json'),(16,'兔斯基','2015-12-27 07:51:12','http://sinacloud.net/sharephotos/Sun%20Dec%2027%2015%3A51%3A07%202015.jpg?formatter=json'),(17,'迪路兽1','2015-12-27 09:05:23','http://sinacloud.net/sharephotos/Sun%20Dec%2027%2017%3A05%3A18%202015.jpg?formatter=json'),(18,'迪路兽2','2015-12-27 09:05:45','http://sinacloud.net/sharephotos/Sun%20Dec%2027%2017%3A05%3A44%202015.jpg?formatter=json'),(19,'向日葵','2015-12-27 09:06:56','http://sinacloud.net/sharephotos/Sun%20Dec%2027%2017%3A06%3A55%202015.jpg?formatter=json'),(20,'向日葵2','2015-12-27 09:07:28','http://sinacloud.net/sharephotos/Sun%20Dec%2027%2017%3A07%3A27%202015.jpg?formatter=json'),(21,'树上一只小鸟','2015-12-27 09:16:29','http://sinacloud.net/sharephotos/%E5%B0%8F%E9%B8%9FSun%20Dec%2027%2017%3A16%3A22%202015.jpg?formatter=json'),(22,'没有找到图片','2015-12-27 09:42:41','http://sinacloud.net/sharephotos/%E6%B2%A1%E6%9C%89%E6%89%BE%E5%88%B0%E5%9B%BE%E7%89%87Sun%20Dec%2027%2017%3A42%3A40%202015.jpg?formatter=json'),(23,'栀子花','2015-12-27 09:56:47','http://sinacloud.net/sharephotos/%E6%A0%80%E5%AD%90%E8%8A%B1Sun%20Dec%2027%2017%3A56%3A45%202015.jpg?formatter=json'),(24,'栀子花','2015-12-27 09:57:16','http://sinacloud.net/sharephotos/%E8%8A%B1Sun%20Dec%2027%2017%3A57%3A15%202015.jpg?formatter=json'),(25,'桃花','2015-12-27 09:57:47','http://sinacloud.net/sharephotos/%E8%8A%B1Sun%20Dec%2027%2017%3A57%3A46%202015.jpg?formatter=json'),(26,'杜鹃花','2015-12-27 09:58:17','http://sinacloud.net/sharephotos/%E8%8A%B1Sun%20Dec%2027%2017%3A58%3A16%202015.jpg?formatter=json'),(27,'栀子花','2015-12-27 10:01:39','http://sinacloud.net/sharephotos/%E6%A0%80%E5%AD%90%E8%8A%B1_Sun%20Dec%2027%2018%3A01%3A37%202015.jpg?formatter=json');
/*!40000 ALTER TABLE `sharephotos_tb_photo_info` ENABLE KEYS */;


--
-- Table structure for table `sharephotos_tb_tag`
--

DROP TABLE IF EXISTS `sharephotos_tb_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sharephotos_tb_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(20) NOT NULL,
  `is_face` tinyint(1) NOT NULL,
  `add_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag` (`tag`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sharephotos_tb_tag`
--

/*!40000 ALTER TABLE `sharephotos_tb_tag` DISABLE KEYS */;
INSERT INTO `sharephotos_tb_tag` VALUES (1,'标签',0,'2015-12-26 08:45:24'),(2,'表情',0,'2015-12-26 08:52:33'),(3,'标签1',0,'2015-12-26 09:14:22'),(4,'阿狸',0,'2015-12-26 10:05:41'),(5,'楪祈',0,'2015-12-26 10:07:52'),(6,'小猫',0,'2015-12-26 11:03:44'),(7,'花',0,'2015-12-27 09:58:17'),(8,'风景',0,'2015-12-26 13:37:12'),(9,'船',0,'2015-12-26 15:38:30'),(10,'山峰',0,'2015-12-26 16:49:09'),(11,'兔斯基',0,'2015-12-27 07:51:12'),(12,'初音',0,'2015-12-27 07:10:20'),(13,'迪路兽',0,'2015-12-27 09:05:45'),(14,'小鸟',0,'2015-12-27 09:16:29'),(15,'没有找到图片',0,'2015-12-27 09:42:41'),(16,'栀子花',0,'2015-12-27 10:01:39');
/*!40000 ALTER TABLE `sharephotos_tb_tag` ENABLE KEYS */;


--
-- Table structure for table `sharephotos_tb_tag_photo`
--

DROP TABLE IF EXISTS `sharephotos_tb_tag_photo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sharephotos_tb_tag_photo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tb_tag_id` int(11) NOT NULL,
  `tb_photo_info_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tb_tag_id` (`tb_tag_id`,`tb_photo_info_id`),
  KEY `sharephotos_tb_tag_photo_177256b0` (`tb_tag_id`),
  KEY `sharephotos_tb_tag_photo_a815d01c` (`tb_photo_info_id`)
) ENGINE=MyISAM AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sharephotos_tb_tag_photo`
--

/*!40000 ALTER TABLE `sharephotos_tb_tag_photo` DISABLE KEYS */;
INSERT INTO `sharephotos_tb_tag_photo` VALUES (1,3,3),(2,4,4),(3,5,5),(4,6,6),(5,7,7),(6,8,8),(7,9,10),(8,10,11),(9,11,12),(10,12,13),(11,11,16),(12,13,17),(13,13,18),(14,7,19),(15,7,20),(16,14,21),(17,15,22),(18,16,23),(19,7,24),(20,7,25),(21,7,26),(22,16,27);
/*!40000 ALTER TABLE `sharephotos_tb_tag_photo` ENABLE KEYS */;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-12-27 19:53:08
