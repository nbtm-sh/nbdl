START TRANSACTION;
USE `nbdl`;
CREATE TABLE `urls` (
    id varchar(256) NOT NULL PRIMARY KEY,
    contentId TEXT NOT NULL,
    contentHost TEXT NOT NULL,
    dateCreated DATE NOT NULL,
    dateExpire DATE NOT NULL,
    contentFileName TEXT NOT NULL
);

COMMIT;