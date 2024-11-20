SHOW COLUMNS FROM user LIKE 'password';
ALTER TABLE user MODIFY COLUMN password VARCHAR(255);
DESCRIBE chat_history;
ALTER TABLE chat_history MODIFY response LONGTEXT;
ALTER TABLE chat_history ADD COLUMN title VARCHAR(255);
