create table `tb1` (
    `id` int unsigned auto_increment,
    primary key (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

create table `tb2` (
    `id` int not null auto_increment none primary key
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



CREATE TABLE `mytest` (
    `update_time` timestamp  NULL  default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

//如果想设置一个具体的默认时间可以这样：
CREATE TABLE `mytest2` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `comments` varchar(255) DEFAULT '' COMMENT '内容',
  `create_time` timestamp DEFAULT '2020-12-12 12:12:12' COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


create table `company_patent` ( 
`id` int(11) NOT NULL PRIMARY KEY  auto_increment,
`company_id` int(11) NULL   ,
`name` varchar(512) NULL   ,
`status` varchar(50) NULL   ,
`patent_type` varchar(50) NULL   ,
`num` varchar(50) NOT NULL   ,
`patenter` varchar(255) NULL   ,
`patenter_now` varchar(255) NULL   ,
`inventor` varchar(512) NULL   ,
`designer` varchar(255) NULL   ,
`ipc` text NULL   ,
`cpc` text NULL   ,
`info` longtext NULL   ,
`public_date` varchar(25) NULL   ,
`application_date` varchar(25) NULL   ,
`company_guogao_id` int(11) NULL   ,
`industry` varchar(50) NULL   ,
`tags` varchar(5000) NULL   ,
`tags_ltp` varchar(5000) NULL   ,
`node_id` int(11) NULL   ,
`node_score` float NULL   ,
`claims` mediumtext NULL   ,
`instructions` mediumtext NULL   ,
`url` varchar(1000) NULL   ,
`application_num` varchar(64) NULL   ,
`main_classification_num` varchar(64) NULL   ,
`province_code` varchar(64) NULL   ,
`pages` varchar(10) NULL   ,
`agency` varchar(128) NULL   ,
`agent` varchar(64) NULL   ,
`address` varchar(255) NULL   ,
`sovereignty_item` mediumtext NULL   ,
`crawl_time` datetime NULL  DEFAULT CURRENT_TIMESTAMP ,
`update_time` datetime NULL  DEFAULT CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
`structure_node` longtext NULL   ,
`structure_link` longtext NULL   ,
`claims_mongo` tinyint(4) NULL   ,
`instructions_mongo` tinyint(4) NULL   ,
`domain_id_list` varchar(1000) NULL   ,
`focus_node` text NULL   ,
`focus_link` text NULL   ,
`applicant` varchar(255) NULL   ,
`is_online` tinyint(4) NULL   ,
`industry_is_right` tinyint(4) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;