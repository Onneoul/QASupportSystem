# BUGCASE ID 생성 트리거

DELIMITER //
CREATE TRIGGER generate_bug_case_id
BEFORE INSERT ON BUG_CASE
FOR EACH ROW
BEGIN
  DECLARE last_sequence INT;
  DECLARE new_bug_case_id VARCHAR(15);
  
  -- 해당 TEST_CASE_ID를 가지는 가장 최근의 BUG_CASE_ID를 찾음
  SELECT MAX(SUBSTRING(BUG_CASE_ID, -3))
  INTO last_sequence
  FROM BUG_CASE
  WHERE SUBSTRING(BUG_CASE_ID, 2, 9) = SUBSTRING(NEW.TEST_CASE_ID, 2, 9);
  
  -- 시퀀스 번호 증가 또는 초기화
  IF last_sequence IS NULL THEN
    SET last_sequence = 1;
  ELSE
    SET last_sequence = last_sequence + 1;
  END IF;
  
  -- 새로운 BUG_CASE_ID 생성
  SET new_bug_case_id = CONCAT('B', SUBSTRING(NEW.TEST_CASE_ID, 2, 9), LPAD(last_sequence, 3, '0'));
  
  -- 삽입될 행의 BUG_CASE_ID 설정
  SET NEW.BUG_CASE_ID = new_bug_case_id;
END;
//
DELIMITER ;