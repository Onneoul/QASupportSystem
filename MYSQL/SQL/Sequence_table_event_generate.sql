CREATE TABLE sequence (
    id INT AUTO_INCREMENT PRIMARY KEY
);

INSERT INTO sequence (id) VALUES ();
SELECT LAST_INSERT_ID();

SET GLOBAL event_scheduler = ON;

DELIMITER //
CREATE EVENT reset_sequence
ON SCHEDULE EVERY 1 DAY STARTS TIMESTAMP(CURDATE(), '00:00:00')
DO 
BEGIN
    TRUNCATE TABLE sequence_table;
END;
//
DELIMITER ;

select * from sequence;