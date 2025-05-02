CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    comment TEXT,
    user_id INTEGER REFERENCES users
);