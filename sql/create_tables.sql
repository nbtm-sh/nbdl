START TRANSACTION;
USE `nbdl`;
CREATE TABLE `urls` (
    id INT NOT NULL PRIMARY KEY,
    contentId TEXT NOT NULL UNIQUE,
    contentHost INT NOT NULL,
    dateCreated DATE NOT NULL,
    dateExpire DATE NOT NULL,
    contentFileName TEXT NOT NULL
);

COMMIT;