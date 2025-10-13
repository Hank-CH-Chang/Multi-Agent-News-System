-- database/schema.sql
CREATE TABLE IF NOT EXISTS news (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT,
    summary TEXT,
    category TEXT,
    ranked TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_category ON news(category);
CREATE INDEX IF NOT EXISTS idx_created_at ON news(created_at);
