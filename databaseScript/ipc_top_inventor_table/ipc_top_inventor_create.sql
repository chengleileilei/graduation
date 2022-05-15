CREATE TABLE `ipc_top_inventor` (
    `ipc_category` char(1) NOT NULL,
    `top_inventors` json DEFAULT NULL,
    PRIMARY KEY (`ipc_category`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
