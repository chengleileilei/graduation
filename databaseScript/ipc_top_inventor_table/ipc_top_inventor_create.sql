CREATE TABLE `ipc_top_inventor` (
    `ipc_category` char(1) NOT NULL,
    `top_inventors` json DEFAULT NULL,
    `ipc_category_info` varchar(500) DEFAULT NULL,
    `ipc_image_name` varchar(100) DEFAULT NULL,
    PRIMARY KEY (`ipc_category`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;