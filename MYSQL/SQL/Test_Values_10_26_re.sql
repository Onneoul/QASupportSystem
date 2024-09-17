insert into user (user_id, user_password) values('normal_user_test', 'test1');
insert into user (user_id, user_password, user_level) values('high_user_test', 'test1', 2);
insert into user (user_id, user_password, user_level) values('administrator_test', 'test1', 3);
insert into user (user_id, user_password, user_level) values('kimminse', 'test2', 3);

INSERT INTO GAME_INFORMATION (GAME_TITLE, GAME_VERSION, GAME_EXECUTION_PATH) VALUES ("Pikachu Ball", "1.0.0", "I:/AutomatedQA/MYSQL/GameInfoTest/Pikachu.EXE");
INSERT INTO GAME_INFORMATION (GAME_TITLE, GAME_VERSION, GAME_EXECUTION_PATH) VALUES ("Pikachu Ball", "2.0.0", "I:/AutomatedQA/MYSQL/GameInfoTest/Pikachu_2.0.0.EXE");
INSERT INTO GAME_INFORMATION (GAME_TITLE, GAME_VERSION, GAME_EXECUTION_PATH) VALUES ("Pikachu Ball", "3.0.0", "I:/AutomatedQA/MYSQL/GameInfoTest/Pikachu_3.0.0.EXE");


insert into performance (performance_name, performance_path, performance_date) values ('FalsePerformance2.txt', 'static/Resource/Performance/', '2023-10-24 14:01:00');
insert into performance (performance_name, performance_path, performance_date) values ('FalsePerformance1.txt', 'static/Resource/Performance/', '2023-10-25 16:27:00');

insert into screenshot (SCREENSHOT_NAME, SCREENSHOT_PATH, SCREENSHOT_DESCRIPTION, SCREENSHOT_DATE) values ('TestScreenshot1.png', 'static/Resource/Screenshot/', '테스트용 Description입니다.' , '2023-10-24 15:25:00');
insert into screenshot (SCREENSHOT_NAME, SCREENSHOT_PATH, SCREENSHOT_DESCRIPTION, SCREENSHOT_DATE) values ('TestScreenshot2.png', 'static/Resource/Screenshot/', '테스트용 Description입니다.22' , '2023-10-25 16:26:00');
insert into screenshot (SCREENSHOT_NAME, SCREENSHOT_PATH, SCREENSHOT_DESCRIPTION, SCREENSHOT_DATE) values ('screenshot_20231031_185632.png', 'static/Resource/Screenshot/', '무한 로딩.' , '2023-10-31 18:56:32');


insert into log (log_name, log_path, log_date) values ('FalseLog1.txt', '/Resource/log/', '2023-10-24 14:01:00');
insert into log (log_name, log_path, log_date) values ('FalseLog2.txt', '/Resource/log/', '2023-10-25 16:27:00');

insert into test_case (test_case_id, test_date, game_version, user_code, log_id) values ('T20231023001', '2023-10-23 00:00:00', '2.0.0', '1', 2);
insert into test_case (test_case_id, test_date, game_version, user_code, log_id) values ('T20231024001', '2023-10-24 14:00:00', '2.0.0', 1, 1);
insert into test_case (test_case_id, test_date, game_version, user_code) values ('T20231024002', '2023-10-24 15:10:00', '3.0.0', 2);
insert into test_case (test_case_id, test_date, game_version, user_code) values ('T20231025001', '2023-10-25 15:25:00', '3.0.0', 3);
insert into test_case (test_case_id, test_date, game_version, user_code) values ('T20231031001', '2023-10-31 18:56:11', '3.0.0', 1);




insert into bug_case (TEST_CASE_ID, BUG_CASE_ID, BUG_DATE, bug_status, game_version, screenshot_id) values ('T20231023001', 'B231023001001', '2023-10-23 00:02:00', 2, '1.0.0', 1);
insert into bug_case (TEST_CASE_ID, BUG_CASE_ID, BUG_DATE, bug_status, game_version) values ('T20231024001', 'B231024001001', '2023-10-24 14:00:00', 1, '2.0.0');
insert into bug_case (TEST_CASE_ID, BUG_CASE_ID, BUG_DATE, bug_status, game_version, screenshot_id) values ('T20231024001', 'B231024001002', '2023-10-24 15:10:00', 0, '2.0.0', 2);
insert into bug_case (TEST_CASE_ID, BUG_CASE_ID, BUG_DATE, bug_status, game_version) values ('T20231024002', 'B231024002001', '2023-10-24 15:25:00', 0, '3.0.0');
insert into bug_case (TEST_CASE_ID, BUG_CASE_ID, BUG_DATE, bug_status, game_version) values ('T20231025001', 'B231025001001', '2023-10-25 16:26:00', 0, '3.0.0');
insert into bug_case (TEST_CASE_ID, BUG_CASE_ID, BUG_DATE, bug_status, game_version, screenshot_id) values ('T20231031001', 'B231031001001', '2023-10-31 16:26:00', 0, '3.0.0', 3);
insert into bug_case (TEST_CASE_ID, BUG_DATE, game_version) values ('T20231031001', '2023-10-31 17:26:00', '3.0.0');

SHOW CREATE TABLE SEQUENCE;
select * from screenshot;
select * from bug_case;
select * from test_case;
select * from sequence;
select * from screenshot where screenshot_id = (select screenshot_id from bug_case where bug_case_id = 'B231031001001');
drop database autoqa;