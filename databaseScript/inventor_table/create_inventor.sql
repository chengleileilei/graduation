CREATE TABLE  if not exists  `inventors`
(
    `inventor_id`               int         NOT NULL AUTO_INCREMENT,
    `inventor_name`             varchar(50) NOT NULL,
    `patents_ids`               longtext,
    `inventor_patents_totalnum` int   DEFAULT NULL,
    `inventor_companys`         json  DEFAULT NULL,
    `patents_ipcs`              json  DEFAULT NULL,
    `research_areas`            json  DEFAULT NULL,
    `collaborators`             json  DEFAULT NULL,
    `num_with_score`            int   DEFAULT NULL,
    `average_score`             float DEFAULT NULL,
    `inventor_categories`       json  DEFAULT NULL,
    PRIMARY KEY (`inventor_id`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb3;



--   create table if not exists `inventors` (
--     `inventor_id` int  not null auto_increment primary key,
--     `inventor_name` varchar(50) not null,
--     `patents_ids` LONGTEXT null,
--     `inventor_patents_totalnum` int null,
--     `inventor_companys` json null,
--     `patents_ipcs` json null,
--     `research_areas` json null,
--     `collaborators` json null,
--     `citations_num` int null,
--     `h_index` int null,
--     `g-index` int null
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
