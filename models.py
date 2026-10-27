from psycopg import sql
# requests to init tables
#------------------------------------------------------------
CREATE_STATUS_ENUM = sql.SQL('''
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE pg_type.typname = 'note_status') THEN
        CREATE TYPE note_status AS ENUM ('draft', 'published', 'reviewed');
    END IF;
END$$;
''')

CREATE_USERS_TABLE = sql.SQL('''
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name Varchar(50) NOT NULL
);
''')

CREATE_NOTES_TABLE = sql.SQL('''
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    title Varchar(50) NOT NULL,
    content TEXT NOT NULL,
    status note_status DEFAULT 'draft' NOT NULL,
    time_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,
    
    CONSTRAINT fk_users 
    FOREIGN KEY (user_id) 
    REFERENCES users (id) 
    ON DELETE CASCADE
);    
''')

CREATE_NOTES_INDEX = sql.SQL('''CREATE INDEX IF NOT EXISTS notes_idx ON notes (time_created);''')

CREATE_USER_NOTES_INDEX = sql.SQL('''CREATE INDEX IF NOT EXISTS users_idx ON notes (user_id, time_created);''')
# CRUD for users
#-----------------------------------------------------------------------------------
POST_USER = sql.SQL('''INSERT INTO users (name) VALUES (%s) RETURNING id, name;''')

GET_USER = sql.SQL('''SELECT id, name FROM users WHERE id = %s;''')

TOTAL_USER_NOTES = sql.SQL('''SELECT COUNT(*) as total FROM notes WHERE user_id = %s;''')

SELECT_USER_NOTES = sql.SQL('''SELECT * FROM notes WHERE user_id = %s LIMIT %s OFFSET %s;''')

EXISTS_USER = sql.SQL('''SELECT 1 FROM users WHERE id = %s;''')

DELETE_USER = sql.SQL('''DELETE FROM users WHERE id = %s RETURNING id;''')

#CRUD for notes
#-----------------------------------------------------------------------------------

POST_NOTE = sql.SQL('''INSERT INTO notes (title, content, status, user_id) 
VALUES (%s, %s, %s, %s) RETURNING id, title, content, status, time_created, user_id;''')

TOTAL_NOTES = sql.SQL('''SELECT COUNT(*) as total FROM notes;''')

SELECT_ALL_NOTES = sql.SQL('SELECT * FROM notes ORDER BY time_created DESC LIMIT %s OFFSET %s;')

GET_NOTE = sql.SQL('SELECT * FROM notes WHERE id = %s;')

EXISTS_NOTE = sql.SQL('''SELECT 1 FROM notes WHERE id = %s;''')

DELETE_NOTE = sql.SQL('''DELETE FROM notes WHERE id = %s RETURNING id;''')

