START TRANSACTION;
USE `nbdl`;
CREATE TABLE `urls` (
    id INT NOT NULL PRIMARY KEY,
    contentId TEXT NOT NULL,
    contentHost INT NOT NULL,
    dateCreated DATE NOT NULL,
    dateExpire DATE NOT NULL
);

COMMIT;