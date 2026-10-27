CREATE TYPE note_status AS ENUM ('draft', 'published', 'reviewed');

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name Varchar(50) NOT NULL
);

CREATE TABLE notes (
    id SERIAL PRIMARY KEY,
    title Varchar(50) NOT NULL,
    content TEXT NOT NULL,
    status note_status DEFAULT "draft" NOT NULL,
    time_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP?
    user_id INTEGER NOT NULL,

    CONSTRAINT fk_users
    FOREIGN KEY (user_id)
    REFERENCES users (id)
    ON DELETE CASCADE
);

CREATE INDEX notes_idx ON notes (time_created);

CREATE INDEX IF NOT EXISTS users_idx ON notes (user_id, time_created);