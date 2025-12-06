-- PostgreSQL schema for Grant Database
-- Compatible with render.com

DROP TABLE IF EXISTS questions CASCADE;
DROP TABLE IF EXISTS groups CASCADE;

CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    group_number INTEGER UNIQUE NOT NULL,
    group_name TEXT NOT NULL
);

CREATE TABLE questions (
    id SERIAL PRIMARY KEY,
    question_number VARCHAR(20) UNIQUE NOT NULL,
    group_id INTEGER NOT NULL REFERENCES groups(id),
    question_text TEXT NOT NULL,
    russian TEXT,
    muira TEXT,
    danish TEXT,
    nganasan TEXT,
    westcircassian TEXT,
    polish TEXT,
    bulgarian TEXT,
    nanai TEXT,
    nornakhichevan TEXT,
    udmurt TEXT,
    greben TEXT,
    mountmari TEXT,
    icari TEXT,
    macedonian TEXT,
    norwegian TEXT,
    kumyk TEXT,
    northernkhanty TEXT,
    ulch TEXT
);

CREATE INDEX idx_group_id ON questions(group_id);

-- Note: Data will be populated by the application using export_to_postgres.py
-- or by running create_database.py and then exporting the SQLite data

-- Example queries:
-- Get all questions in a group:
-- SELECT q.*, g.group_name FROM questions q JOIN groups g ON q.group_id = g.id WHERE g.group_number = 1;

-- Get random question from a group:
-- SELECT q.*, g.group_name FROM questions q JOIN groups g ON q.group_id = g.id WHERE g.group_number = 2 ORDER BY RANDOM() LIMIT 1;

-- Get statistics:
-- SELECT g.group_number, g.group_name, COUNT(q.id) as question_count 
-- FROM groups g LEFT JOIN questions q ON g.id = q.group_id 
-- GROUP BY g.id, g.group_number, g.group_name 
-- ORDER BY g.group_number;
