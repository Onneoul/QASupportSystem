

SELECT * from game_information;
SELECT GAME_EXECUTION_PATH FROM GAME_INFORMATION WHERE GAME_TITLE = "Pikachu Ball" and GAME_VERSION = "1.0.0";
SELECT GAME_EXECUTION_PATH FROM GAME_INFORMATION WHERE GAME_TITLE = "Pikachu Ball" and GAME_VERSION = "2.0.0";

select * from user;
select * from bug_case;
select * from test_case;
select * from log;
select * from screenshot;
select * from test_macro;
select * from game_information;
select * from test_macro;


alter table bug_case change BUG_CASE_DATE CASE_DATE date;
alter table test_case change TEST_DATE CASE_DATE date;

update test_case set log_id = 3 where test_case_id = 'T20231101008';
SELECT SCREENSHOT_ID FROM SCREENSHOT WHERE SCREENSHOT_NAME = 'screenshot_20231030_185632.png' ORDER BY BUG_DATE DESC LIMIT 1;

alter table screenshot modify SCREENSHOT_PATH varchar(200) Not Null default 'static/Resource/Screenshot/';
alter table bug_case modify BUG_STATUS int Not Null default 0;
describe screenshot;
alter table LOG modify LOG_PATH  varchar(200) Not Null default 'static/Resource/Log/';
alter table PERFORMANCE modify PERFORMANCE_PATH  varchar(200) Not Null default 'static/Resource/Performance/';

GRANT ALL PRIVILEGES ON autoqa.* TO 'normal_user_test'@'%';