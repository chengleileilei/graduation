CREATE TABLE  if not exists  `ipc_A`
-- 这是一个没有用的文件
(
    `ipc_index` int(11) not null AUTO_INCREMENT,
	`ipc_number` varchar(255) null,
	`ipc_info` varchar(5000)  null,
    PRIMARY KEY (`ipc_index`)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb3;