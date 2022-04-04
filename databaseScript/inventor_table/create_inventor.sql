create table if not exists `inventors` (
    `inventor_id` int  not null auto_increment primary key,
    `inventor_name` varchar(50) not null,
    `patents_ids` varchar(512) null,
    `inventor_patents_totalnum` int null,
    `inventor_companys` json null,
    `patents_ipcs` json null,
    `research_areas` json null,
    `collaborators` json null,
    `citations_num` int null,
    `h_index` int null,
    `g-index` int null
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


