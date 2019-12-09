--
-- ��SQLiteStudio v3.1.1 �������ļ� �ܶ� 8�� 13 14:35:08 2019
--
-- �ı����룺System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- ��known
DROP TABLE known;
CREATE TABLE known (id INTEGER PRIMARY KEY AUTOINCREMENT, word_id INTEGER REFERENCES word (id) NOT NULL, add_times INT (10) DEFAULT (0), create_date DATE);

-- ��today
DROP TABLE today;
CREATE TABLE today (id INTEGER PRIMARY KEY AUTOINCREMENT, word_id INTEGER REFERENCES word (id));

-- ��word
DROP TABLE word;
CREATE TABLE word (id INTEGER PRIMARY KEY AUTOINCREMENT, word VARCHAR (20) NOT NULL UNIQUE, explains VARCHAR (20) NOT NULL, phonetic VARCHAR (20) NOT NULL, examples_en VARCHAR (200), examples_cn VARCHAR (200), known_time DATETIME, add_times INT (2) DEFAULT (0), create_time DATETIME NOT NULL, is_delete BOOLEAN DEFAULT False NOT NULL);

DROP TABLE user;
CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR (20) UNIQUE NOT NULL DEFAULT C0C, word_num INT (4) DEFAULT (50), is_month VARCHAR (20) DEFAULT Month, head_image VARCHAR (200) NOT NULL, background_image VARCHAR (200) NOT NULL);
INSERT INTO user (id, name, word_num, is_month, head_image, background_image) VALUES (1, 'C0C', 50, 'Month', 'image/c0c.jpg', 'image/back.jpg');


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
