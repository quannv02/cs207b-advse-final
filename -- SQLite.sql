-- SQLite
-- add status into reservation table
ALTER TABLE reservations
ADD COLUMN status INT NOT NULL DEFAULT 0;