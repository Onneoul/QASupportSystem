insert into user (user_id, user_password) values('normal_user_test', 'test1');
insert into user (user_id, user_password, user_level) values('high_user_test', 'test1', 2);
insert into user (user_id, user_password, user_level) values('administrator_test', 'test1', 3);
insert into user (user_id, user_password, user_level) values('kimminse', 'test2', 3);

insert into performance (performance_name, performance_path, performance_date, Test_CASE_ID) values ('FalsePerformance2.txt', 'static/Resource/Performance/', '2023-10-24 14:01:00', 'T20231023001');
insert into performance (performance_name, performance_path, performance_date, Test_CASE_ID) values ('FalsePerformance1.txt', 'static/Resource/Performance/', '2023-10-25 16:27:00', 'T20231024002');

insert into screenshot (SCREENSHOT_NAME, SCREENSHOT_PATH, SCREENSHOT_DESCRIPTION, SCREENSHOT_DATE) values ('TestScreenshot1.png', 'static/Resource/Screenshot/', '테스트용 Description입니다.' , '2023-10-24 15:25:00');
insert into screenshot (SCREENSHOT_NAME, SCREENSHOT_PATH, SCREENSHOT_DESCRIPTION, SCREENSHOT_DATE) values ('TestScreenshot2.png', 'static/Resource/Screenshot/', '테스트용 Description입니다.22' , '2023-10-25 16:26:00');

insert into log (log_name, log_path, log_date, Test_CASE_ID) values ('FalseLog1.txt', '/Resource/log/', '2023-10-24 14:01:00', 'T20231023001');
insert into log (log_name, log_path, log_date, Test_CASE_ID) values ('FalseLog2.txt', '/Resource/log/', '2023-10-25 16:27:00', 'T20231024002');

INSERT INTO GAME_INFORMATION (GAME_TITLE, GAME_VERSION, GAME_EXECUTION_PATH, GAME_LOG_PATH) VALUES ("Pikachu Ball", "1.0.0", "I:/AutomatedQA/MYSQL/GameInfoTest/Pikachu.EXE", "I:\AutomatedQA\MYSQL\LogTest");
INSERT INTO GAME_INFORMATION (GAME_TITLE, GAME_VERSION, GAME_EXECUTION_PATH, GAME_LOG_PATH) VALUES ("Pikachu Ball", "2.0.0", "I:/AutomatedQA/MYSQL/GameInfoTest/Pikachu_2.0.0.EXE", "I:\AutomatedQA\MYSQL\LogTest");
INSERT INTO GAME_INFORMATION (GAME_TITLE, GAME_VERSION, GAME_EXECUTION_PATH, GAME_LOG_PATH) VALUES ("Pikachu Ball", "3.0.0", "I:/AutomatedQA/MYSQL/GameInfoTest/Pikachu_3.0.0.EXE", "I:\AutomatedQA\MYSQL\LogTest");

insert into test_case (test_case_id, test_date, game_version, user_code, log_id) values ('T20231023001', '2023-10-23 00:00:00', '2.0.0', '1', 2);
insert into test_case (test_case_id, test_date, game_version, user_code, log_id) values ('T20231024001', '2023-10-24 14:00:00', '2.0.0', 1, 1);
insert into test_case (test_case_id, test_date, game_version, user_code) values ('T20231024002', '2023-10-24 15:10:00', '3.0.0', 2);
insert into test_case (test_case_id, test_date, game_version, user_code) values ('T20231025001', '2023-10-25 15:25:00', '3.0.0', 3);

insert into bug_case (TEST_CASE_ID, BUG_CASE_ID, BUG_DESCRIPTION, BUG_DATE, bug_status, game_version, screenshot_id) values ('T20231023001', 'B231023001001', '테스트용 버그 케이스', '2023-10-23 00:02:00', 2, '1.0.0', 1);
insert into bug_case (TEST_CASE_ID, BUG_CASE_ID, BUG_DESCRIPTION, BUG_DATE, bug_status, game_version) values ('T20231024001', 'B231024001001', 'Bug Case for Test', '2023-10-24 14:00:00', 1, '2.0.0');
insert into bug_case (TEST_CASE_ID, BUG_CASE_ID, BUG_DESCRIPTION, BUG_DATE, bug_status, game_version, screenshot_id) values ('T20231024001', 'B231024001002', 'Bug Case for Test 1', '2023-10-24 15:10:00', 0, '2.0.0', 2);
insert into bug_case (TEST_CASE_ID, BUG_CASE_ID, BUG_DESCRIPTION, BUG_DATE, bug_status, game_version) values ('T20231024002', 'B231024002001', '1111', '2023-10-24 15:25:00', 0, '3.0.0');
insert into bug_case (TEST_CASE_ID, BUG_CASE_ID, BUG_DESCRIPTION, BUG_DATE, bug_status, game_version) values ('T20231025001', 'B231025001001', '!$%^&)A:?ZXCP!$', '2023-10-25 16:26:00', 0, '3.0.0');


SELECT TEST_CASE_ID, TEST_DATE, GAME_VERSION FROM TEST_CASE WHERE TEST_CASE_ID = (SELECT TEST_CASE_ID FROM BUG_CASE WHERE BUG_CASE_ID = 'B231024001001');
SELECT TEST_CASE_ID, TEST_DATE,GAME_VERSION FROM TEST_CASE WHERE GAME_VERSION like (SELECT GAME_VERSION FROM TEST_CASE WHERE TEST_CASE_ID = 'T20231024001') AND TEST_CASE_ID <> 'T20231024001' limit 10;
SELECT BUG_CASE_ID, BUG_DATE, GAME_VERSION, BUG_STATUS FROM BUG_CASE WHERE TEST_CASE_ID = 'T20231023001' limit 10;
SELECT * FROM SCREENSHOT WHERE SCREENSHOT_ID = (SELECT SCREENSHOT_ID FROM BUG_CASE WHERE BUG_CASE_ID = 'B231023001001');

SELECT SCREENSHOT_ID FROM BUG_CASE WHERE BUG_CASE_ID = 'B231023001001';
select * from screenshot;
select * from bug_case where bug_case_id like 'B231024001001';

select * from performance where test_case_id = 'T20231023001';
select * from log;
select * from BUG_CASE;

select * from screenshot where screenshot_id = (select screenshot_id from bug_case where bug_case_id='B231023001001');