USE testdb;

DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS exercise;

CREATE TABLE user(
	id VARCHAR(20) NOT NULL,
    pw VARCHAR(100) NOT NULL,
    first_name VARCHAR(10),
    last_name VARCHAR(10),
	PRIMARY KEY(id)
);

CREATE TABLE exercise(
    e_id INT NOT NULL,
    e_name VARCHAR(20) NOT NULL,
    e_repeat INT,
    PRIMARY KEY(e_id)
);

CREATE TABLE Bookmark(
    id varchar(20) NOT NULL,
    e_id INT,
    PRIMARY KEY (id, e_id),
    FOREIGN KEY(id) REFERENCES user(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY(e_id) REFERENCES exercise(e_id) ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO user VALUES("root", "root", "root", "root");

INSERT INTO exercise VALUES(1, "SQUAT", 10);
INSERT INTO exercise VALUES(2, "SQUAT", 20);
INSERT INTO exercise VALUES(3, "SQUAT", 30);
INSERT INTO exercise VALUES(4, "LUNGE", 10);
INSERT INTO exercise VALUES(5, "LUNGE", 20);
INSERT INTO exercise VALUES(6, "LUNGE", 30);
INSERT INTO exercise VALUES(7, "PUSH UP", 10);
INSERT INTO exercise VALUES(8, "PUSH UP", 20);
INSERT INTO exercise VALUES(9, "PUSH UP", 30); 