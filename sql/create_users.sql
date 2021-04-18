START TRANSACTION;
USE `nbdl`;
CREATE USER IF NOT EXISTS 'nbdl'@'localhost' IDENTIFIED BY 'default_JNMt$523FmeMJE^S'; 
CREATE USER IF NOT EXISTS 'nbdlexpire'@'localhost' IDENTIFIED BY 'default_S5#cj&QfH8~S5xkr';
USE `nbdl`;
GRANT INSERT, SELECT ON `urls` TO 'nbdl'@'localhost';
GRANT INSERT, UPDATE, DELETE, SELECT ON `urls` TO 'nbdlexpire'@'localhost';
FLUSH PRIVILEGES;
COMMIT;