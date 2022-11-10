PRAGMA foreign_keys = ON;
CREATE TABLE users(
  username VARCHAR(20) NOT NULL,
  fullname VARCHAR(40) NOT NULL,
  email VARCHAR(40) NOT NULL,
  password VARCHAR(256) NOT NULL,
  created datetime default CURRENT_TIMESTAMP,
  PRIMARY KEY(username)
);

CREATE TABLE files(
  fileid INTEGER PRIMARY KEY AUTOINCREMENT,
  filename VARCHAR(64) NOT NULL,
  owner VARCHAR(20) NOT NULL,
  duration FLOAT,
  bitrate FLOAT,
  size INTEGER,
  created datetime default CURRENT_TIMESTAMP,
  FOREIGN KEY(owner) REFERENCES users(username) ON DELETE CASCADE
);
