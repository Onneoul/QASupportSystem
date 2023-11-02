select * from bug_case;
select * from test_case;
select * from test_macro;
select * from user;
select * from log;
select * from performance;
select * from game_information;
select * from screenshot;
select * from sequence;

DESCRIBE TEST_CASE;
select Count(*) from bug_case;
select Count(*) from bug_case where bug_status = 0;
select Count(*) from bug_case where bug_status = 1;
select Count(*) from bug_case where bug_status = 2;

select auto_increment from information_schema.tables where table_name = 'log' and table_schema = 'autoqa';

update test_case set log_id = 2 where test_case_id = 'T20231101003';