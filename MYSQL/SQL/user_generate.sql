insert into user (user_id, user_password) values('normal_user_test', 'test1');
insert into user (user_id, user_password, user_level) values('high_user_test', 'test1', 2);
insert into user (user_id, user_password, user_level) values('administrator_test', 'test1', 3);
insert into user (user_id, user_password, user_level) values('kimminse', 'test2', 3);

INSERT INTO GAME_INFORMATION (GAME_TITLE, GAME_VERSION, GAME_EXECUTION_PATH, GAME_LOG_PATH) VALUES ("Pikachu Ball", "1.0.0", "I:/AutomatedQA/MYSQL/GameInfoTest/Pikachu.EXE", "I:\AutomatedQA\MYSQL\LogTest");
INSERT INTO GAME_INFORMATION (GAME_TITLE, GAME_VERSION, GAME_EXECUTION_PATH, GAME_LOG_PATH) VALUES ("Pikachu Ball", "2.0.0", "I:/AutomatedQA/MYSQL/GameInfoTest/Pikachu_2.0.0.EXE", "I:\AutomatedQA\MYSQL\LogTest");
INSERT INTO GAME_INFORMATION (GAME_TITLE, GAME_VERSION, GAME_EXECUTION_PATH, GAME_LOG_PATH) VALUES ("Pikachu Ball", "3.0.0", "I:/AutomatedQA/MYSQL/GameInfoTest/Pikachu_3.0.0.EXE", "I:\AutomatedQA\MYSQL\LogTest");

insert into test_case (test_case_id, test_date, game_version, user_code) values ('T20231023001', '2023-10-23 00:00:00', '2.0.0', '1');
insert into test_case (test_case_id, test_date, game_version, user_code) values ('T20231024001', '2023-10-24 14:00:00', '2.0.0', 1);
insert into test_case (test_case_id, test_date, game_version, user_code) values ('T20231024002', '2023-10-24 15:10:00', '3.0.0', 2);
insert into test_case (test_case_id, test_date, game_version, user_code) values ('T20231025001', '2023-10-25 15:25:00', '3.0.0', 3);

insert into bug_case (TEST_CASE_ID, BUG_CASE_ID, BUG_DESCRIPTION, BUG_DATE, bug_status, game_version) values ('T20231023001', 'B231023001001', '테스트용 버그 케이스', '2023-10-23 00:02:00', 2, '1.0.0');
insert into bug_case (TEST_CASE_ID, BUG_CASE_ID, BUG_DESCRIPTION, BUG_DATE, bug_status, game_version) values ('T20231024001', 'B231024001001', 'Bug Case for Test', '2023-10-24 14:00:00', 1, '2.0.0');
insert into bug_case (TEST_CASE_ID, BUG_CASE_ID, BUG_DESCRIPTION, BUG_DATE, bug_status, game_version) values ('T20231024001', 'B231024001002', 'Bug Case for Test 1', '2023-10-24 15:10:00', 0, '2.0.0');
insert into bug_case (TEST_CASE_ID, BUG_CASE_ID, BUG_DESCRIPTION, BUG_DATE, bug_status, game_version) values ('T20231024002', 'B231024002001', '1111', '2023-10-24 15:25:00', 0, '3.0.0');
insert into bug_case (TEST_CASE_ID, BUG_CASE_ID, BUG_DESCRIPTION, BUG_DATE, bug_status, game_version) values ('T20231025001', 'B231025001001', '!$%^&)A:?ZXCP!$', '2023-10-25 16:26:00', 0, '3.0.0');



select * from test_case;
select * from bug_case;

SELECT bug_case_id AS case_id, bug_date as case_date, game_version, bug_status FROM bug_case WHERE case_date BETWEEN '' AND '';

alter table bug_case change bug_case_date BUG_DATE DATETIME;

SELECT bug_case_id AS case_id, bug_date AS case_date, game_version, bug_status FROM bug_case WHERE bug_date BETWEEN '2023-10-04 08:30:00' AND '2023-10-26 08:30:00' and GAME_VERSION = '2.0.0' and BUG_STATUS = 1;

SELECT bug_case_id AS case_id, bug_date AS case_date, game_version, bug_status FROM bug_case WHERE (bug_date BETWEEN '2023-10-04 08:30:00' AND '2023-10-26 08:30:00') AND (game_version = '2.0.0');

select BUG_CASE_ID, BUG_DATE, GAME_VERSION from bug_case order by BUG_DATE DESC limit 10;
select TEST_CASE_ID, TEST_DATE, GAME_VERSION from test_case order by TEST_DATE DESC limit 10;