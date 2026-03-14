-- Database backup from 2023-03-10
-- This is a sample backup file
-- Actual backups would contain SQL dump data

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Backup completed successfully
