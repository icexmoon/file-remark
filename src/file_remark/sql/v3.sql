ALTER TABLE files 
ADD COLUMN type INT(5);
UPDATE files SET type=1;
UPDATE config SET value='3' 
WHERE name = 'db_version';