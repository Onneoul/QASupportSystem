from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from functools import wraps
import hashlib  # 비밀번호 해싱을 위한 라이브러리
import requests
from datetime import datetime
import os
from flask_mysqldb import MySQL, MySQLdb
from waitress import serve

# mysql = MySQL()
app = Flask(__name__)

SCREENSHOT_FOLDER = 'static/Resource/Screenshot'
LOG_FOLDER = 'static/Resource/Log'
PERFORMANCE_FOLDER = 'static/Resource/Performance'
MACRO_FOLDER = 'static/Resource/Macro'

app.config['SECRET_KEY'] = '#aB354354'

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'kimminse'
# app.config['MYSQL_PASSWORD'] = '#aB354354'
# app.config['MYSQL_DB'] = 'autoqa'

app.config['MYSQL_HOST'] = '180.83.154.240'
app.config['MYSQL_USER'] = 'normal_user_test'
app.config['MYSQL_PASSWORD'] = '#aB354354@aB354354'
app.config['MYSQL_DB'] = 'autoqa'

# mysql.init_app(app)
mysql = MySQL(app)
# mysql = MySQLdb.connect(host="localhost", user="kimminse", passwd="#aB354354", db="autoqa")
# print(mysql.connect)

def login_check(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_function

@app.route("/")
@login_check
def index():
    try:
        print(mysql.connect)
        cur = mysql.connect.cursor()
        print("my sql connect is : {cur}")
    except AttributeError as e:
        print("Error: ", e)
        print("Check if MySQL is properly initialized and connected.")
        return "Database connect failed."
    
    # return render_template('main.html', template_name='dashboard.html') # login_check가 성공하면 이 항목을 실행
    return redirect(url_for('dashboard'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_id = request.form['ID']
        password = request.form['PASSWORD']
        

        try:
            cur = mysql.connect.cursor()
            cur.execute("SELECT * FROM user WHERE user_id = %s", [user_id])
            user = cur.fetchone()
        except AttributeError as e:
            print(f"Attribute Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            cur.close()

        if user and user[2] == password:  # user[2]는 'password' 필드
            session['user_id'] = user_id
            return redirect(url_for('dashboard')) # 로그인이 성공하면 dashboard로 리다이렉트
        else:
            flash("failed to login")
            return render_template('login.html')
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_check
def dashboard():
    try:
        cursor = mysql.connect.cursor()
        cursor.execute("select bug_case_id, bug_date, game_version, bug_status from bug_case order by bug_date DESC limit 10")
        bug_cases = cursor.fetchall()
        cursor.execute("select TEST_CASE_ID, TEST_DATE, GAME_VERSION from test_case order by TEST_DATE DESC limit 10")
        test_cases = cursor.fetchall()
        
        cursor.execute("select count(*) from bug_case")
        bug_total = cursor.fetchone()[0]
        cursor.execute("select count(*) from bug_case where bug_status = 0")
        bug_before = cursor.fetchone()[0]
        cursor.execute("select count(*) from bug_case where bug_status = 1")
        bug_do = cursor.fetchone()[0]
        cursor.execute("select count(*) from bug_case where bug_status = 2")
        bug_complete = cursor.fetchone()[0]
        
        cursor.execute("select count(*) from test_case")
        test_total = cursor.fetchone()[0]
        today_str = datetime.now().strftime("%Y%m%d")
        cursor.execute("select count(*) from test_case where DATE_FORMAT(test_date, '%%Y%%m%%d') = %s", (today_str,))
        test_today = cursor.fetchone()[0]
        
        
        bug_counts = (bug_total, bug_before, bug_do, bug_complete)
        test_counts = (test_total, test_today)
        
    except Exception as e:
        print(f"DB connect Error: {e}")
    finally:
        cursor.close()
    
    
    return render_template('main.html', template_name = 'dashboard.html', bug_cases=bug_cases, test_cases=test_cases, bug_counts=bug_counts, test_counts=test_counts)


@app.route('/search', methods=['GET', 'POST'])
@login_check
def search():
    error_message = request.args.get('error_message')
    results = None
    game_versions = []
    selected_tables = []
    cursor = None
    start_date = None
    end_date = None
    bug_status = 3
    
    
    try:
        cursor = mysql.connect.cursor()
        cursor.execute("SELECT game_version FROM game_information")
        game_versions = [item[0] for item in cursor.fetchall()]
        print(game_versions[0])
        cursor.close()
    except Exception as e:
        print(f"DB connect Error: {e}")
        error_message = f"DB connect Error: {e}"
    # Error가 발생하면 return
    
    # Search 쿼리
    if request.method == 'POST':
        try:
            cursor = mysql.connect.cursor()
            
            selected_tables = request.form.getlist('tables')
            
            if request.form['start_date']:
                date_start_tmp = datetime.strptime(request.form['start_date'], '%Y-%m-%dT%H:%M')
                start_date = date_start_tmp.strftime('%Y-%m-%d %H:%M:%S')
            else:
                start_date = None

            # end_date 처리
            if request.form['end_date']:
                date_end_tmp = datetime.strptime(request.form['end_date'], '%Y-%m-%dT%H:%M')
                end_date = date_end_tmp.strftime('%Y-%m-%d %H:%M:%S')
            else:
                end_date = None
                
            game_version = request.form.get('game_version')
            if game_version == 'None':
                game_version = None
            bug_status = request.form['bug_status']
            
            #테스트용 print
            print('bug_status = ' + bug_status)
            
            queries = []
            if start_date is None:
                if game_version is None:
                    if 'test_case' in selected_tables:
                        queries.append(f"SELECT test_case_id AS case_id, test_date AS case_date, game_version, NULL AS bug_status FROM test_case WHERE test_date <= '{end_date}'")
                    if 'bug_case' in selected_tables:
                        if bug_status == '3':
                            queries.append(f"SELECT bug_case_id AS case_id, bug_date AS case_date, game_version, bug_status FROM bug_case WHERE (bug_date <= '{end_date}')")
                        else:
                            queries.append(f"SELECT bug_case_id AS case_id, bug_date AS case_date, game_version, bug_status FROM bug_case WHERE bug_date <= '{end_date}' AND bug_status = {bug_status}")
                else:
                    if 'test_case' in selected_tables:
                        queries.append(f"SELECT test_case_id AS case_id, test_date AS case_date, game_version, NULL AS bug_status FROM test_case WHERE test_date <= '{end_date}' AND (game_version = '{game_version}')")
                    if 'bug_case' in selected_tables:
                        if bug_status == '3':
                            queries.append(f"SELECT bug_case_id AS case_id, bug_date AS case_date, game_version, bug_status FROM bug_case WHERE (bug_date <= '{end_date}') AND (game_version = '{game_version}')")
                        else:
                            queries.append(f"SELECT bug_case_id AS case_id, bug_date AS case_date, game_version, bug_status FROM bug_case WHERE (bug_date <= '{end_date}') AND (game_version = '{game_version}') AND bug_status = {bug_status}")
            elif end_date is None:
                if game_version is None:
                    if 'test_case' in selected_tables:
                        queries.append(f"SELECT test_case_id AS case_id, test_date AS case_date, game_version, NULL AS bug_status FROM test_case WHERE test_date >= '{start_date}'")
                    if 'bug_case' in selected_tables:
                        if bug_status == '3':
                            queries.append(f"SELECT bug_case_id AS case_id, bug_date AS case_date, game_version, bug_status FROM bug_case WHERE (bug_date >= '{start_date}')")
                        else:
                            queries.append(f"SELECT bug_case_id AS case_id, bug_date AS case_date, game_version, bug_status FROM bug_case WHERE bug_date >= '{start_date}' AND bug_status = {bug_status}")
                else:
                    if 'test_case' in selected_tables:
                        queries.append(f"SELECT test_case_id AS case_id, test_date AS case_date, game_version, NULL AS bug_status FROM test_case WHERE test_date >= '{start_date}' AND (game_version = '{game_version}')")
                    if 'bug_case' in selected_tables:
                        if bug_status == '3':
                            queries.append(f"SELECT bug_case_id AS case_id, bug_date AS case_date, game_version, bug_status FROM bug_case WHERE (bug_date >= '{start_date}') AND (game_version = '{game_version}')")
                        else:
                            queries.append(f"SELECT bug_case_id AS case_id, bug_date AS case_date, game_version, bug_status FROM bug_case WHERE (bug_date >= '{start_date}') AND (game_version = '{game_version}') AND bug_status = {bug_status}")
            else :
                if game_version is None:
                    if 'test_case' in selected_tables:
                        queries.append(f"SELECT test_case_id AS case_id, test_date AS case_date, game_version, NULL AS bug_status FROM test_case")
                    if 'bug_case' in selected_tables:
                        if bug_status == '3':
                            queries.append(f"SELECT bug_case_id AS case_id, bug_date AS case_date, game_version, bug_status FROM bug_case")
                        else:
                            queries.append(f"SELECT bug_case_id AS case_id, bug_date AS case_date, game_version, bug_status FROM bug_case WHERE bug_status = {bug_status}")
                else:
                    if 'test_case' in selected_tables:
                        queries.append(f"SELECT test_case_id AS case_id, test_date AS case_date, game_version, NULL AS bug_status FROM test_case WHERE (game_version = '{game_version}')")
                    if 'bug_case' in selected_tables:
                        if bug_status == '3':
                            queries.append(f"SELECT bug_case_id AS case_id, bug_date AS case_date, game_version, bug_status FROM bug_case WHERE (game_version = '{game_version}')")
                        else:
                            queries.append(f"SELECT bug_case_id AS case_id, bug_date AS case_date, game_version, bug_status FROM bug_case WHERE (game_version = '{game_version}') AND bug_status = {bug_status}")

                
             
            # if game_version is None:
            #     if 'test_case' in selected_tables:
            #         queries.append(f"SELECT test_case_id AS case_id, test_date AS case_date, game_version, NULL AS bug_status FROM test_case WHERE test_date BETWEEN '{start_date}' AND '{end_date}'")
            #     if 'bug_case' in selected_tables:
            #         if bug_status == 3:
            #             queries.append(f"SELECT bug_case_id AS case_id, bug_date AS case_date, game_version, bug_status FROM bug_case WHERE bug_date BETWEEN '{start_date}' AND '{end_date}' AND bug_status = {bug_status}")
            #         else:
            #             queries.append(f"SELECT bug_case_id AS case_id, bug_date AS case_date, game_version, bug_status FROM bug_case WHERE (bug_date BETWEEN '{start_date}' AND '{end_date}')")
            # else:
            #     if 'test_case' in selected_tables:
            #         queries.append(f"SELECT test_case_id AS case_id, test_date AS case_date, game_version, NULL AS bug_status FROM test_case WHERE test_date BETWEEN '{start_date}' AND '{end_date}' AND (game_version = '{game_version}')")
            #     if 'bug_case' in selected_tables:
            #         if bug_status == 3:
            #             queries.append(f"SELECT bug_case_id AS case_id, bug_date AS case_date, game_version, bug_status FROM bug_case WHERE (bug_date BETWEEN '{start_date}' AND '{end_date}') AND (game_version = '{game_version}') AND bug_status = {bug_status}")
            #         else:
            #             queries.append(f"SELECT bug_case_id AS case_id, bug_date AS case_date, game_version, bug_status FROM bug_case WHERE (bug_date BETWEEN '{start_date}' AND '{end_date}') AND (game_version = '{game_version}')")
            
            
                
            
            
            print(queries)
            final_query = ' UNION '.join(queries)
            final_query += " ORDER BY case_date DESC"
            cursor.execute(final_query)
            results = cursor.fetchall()
            cursor.close()
        except Exception as e:
            print( f"Search Query Error: {e}")
            error_message = f"Search Query Error: {e}"
            cursor.close()
   
    return render_template('main.html', template_name='search/SearchMain.html', game_versions=game_versions, results=results, error_message=error_message, start_date=start_date, end_date=end_date, selected_tables=selected_tables, bug_status=bug_status)

@app.route('/searchDetail', methods=['GET'])
@login_check
def get_search_detail():
    recommend_cases = [];
    bug_cases = [];
    log_contents = [];
    performance_contents = [];
    
    case_id = request.args.get('case_id') # searchDetail 페이지에서 case_id 받아오기
    print(case_id)
    if case_id is None:
        flash("Case ID가 유효하지 않습니다.")
        return redirect(url_for('search')) # Case_code가 없는데 searchDetail 페이지로 왔으면 search로 돌려보냄
    
    try:
        cur = mysql.connect.cursor()
    except AttributeError as e:
        print(f"Attribute Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    # case_code 앞자리에 따라 detail 페이지에 표시될 내용을 구분함(Bug Case, Test Case 등)
    case_code = case_id[0]
    if case_code == 'T': # Test Case면
        print("Test Case Test") # 테스트용 
        try:
            cur.execute("SELECT * FROM TEST_CASE WHERE TEST_CASE_ID = %s", [case_id])
            test_case = cur.fetchone()    
            cur.execute("SELECT Performance_ID, Performance_PATH, PERFORMANCE_NAME FROM PERFORMANCE WHERE PERFORMANCE_ID = (SELECT PERFORMANCE_ID from TEST_CASE WHERE TEST_CASE_ID = %s)", [case_id])
            performances = cur.fetchall()
            cur.execute("SELECT LOG_ID, LOG_PATH, LOG_NAME FROM LOG WHERE LOG_ID = (SELECT LOG_ID from TEST_CASE WHERE TEST_CASE_ID = %s)", [case_id])
            logs = cur.fetchall()
            cur.execute("SELECT BUG_CASE_ID, BUG_DATE, GAME_VERSION, BUG_STATUS FROM BUG_CASE WHERE TEST_CASE_ID = %s limit 10", [case_id])
            bug_cases = cur.fetchall()
            cur.execute("SELECT TEST_CASE_ID, TEST_DATE,GAME_VERSION FROM TEST_CASE WHERE GAME_VERSION like (SELECT GAME_VERSION FROM TEST_CASE WHERE TEST_CASE_ID = %s) AND TEST_CASE_ID <> %s limit 10", [case_id, case_id])
            recommend_cases = cur.fetchall()
            
            performance_contents = []
            for performance in performances:
                performance_id, performance_path, performance_name = performance
                performance_full_path = os.path.join(performance_path, performance_name)
                print('performance full path = ' + performance_full_path) # 테스트용
                with open(performance_full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                performance_contents.append({
                    'performance_id': performance_id,
                    'content': content.replace('\n', '<br>'),
                    'performance_path': performance_full_path
                })
            log_contents = []
            for log in logs:
                log_id, log_path, log_name = log
                log_full_path = os.path.join(log_path, log_name)
                print('log full path = ' + log_full_path) # 테스트용
                with open(log_full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                log_contents.append({
                    'log_id': log_id,
                    'content': content.replace('\n', '<br>'),
                    'log_path': log_full_path
                })
        except AttributeError as e:
            print(f"Attribute Error: {e}") # 테스트용
        except Exception as e:
            print(f"An error occurred: {e}") # 테스트용
        finally:
            cur.close()
        return render_template('main.html', template_name='search/SearchDetail.html', search_detail_content='search/TestDetail.html', test_case=test_case, case_id=case_id, log_contents=log_contents, performance_contents=performance_contents, bug_cases=bug_cases, recommend_cases=recommend_cases)

            
    elif case_code == 'B': # Bug Case면
        print("Bug Case Test") # 테스트용
        try:
            screenshot_full_path = None
            test_case = None
            bug_case = None
            screenshot_info = None
            
            cur = mysql.connect.cursor()
            cur.execute("SELECT * FROM BUG_CASE WHERE BUG_CASE_ID = %s", [case_id])
            bug_case = cur.fetchone()
            
            cur.execute("SELECT * FROM SCREENSHOT WHERE SCREENSHOT_ID = (SELECT SCREENSHOT_ID FROM BUG_CASE WHERE BUG_CASE_ID = %s)", [case_id])
            screenshot_info = cur.fetchone()
            print(f"Querying for BUG_CASE_ID: {case_id}, got SCREENSHOT_ID: {screenshot_info[0]}")
            if (screenshot_info != None):
                screenshot_full_path = os.path.join(screenshot_info[2], screenshot_info[1])
                print('screenshot path = {screenshot_full_path}')
            else:
                print("screenshot_info is None")    
                
            cur.execute("SELECT TEST_CASE_ID, TEST_DATE, GAME_VERSION FROM TEST_CASE WHERE TEST_CASE_ID = (SELECT TEST_CASE_ID FROM BUG_CASE WHERE BUG_CASE_ID = %s)", [case_id])
            test_case = cur.fetchone()
            cur.execute("SELECT BUG_CASE_ID, BUG_DATE, GAME_VERSION, BUG_STATUS FROM BUG_CASE WHERE GAME_VERSION like (SELECT GAME_VERSION FROM BUG_CASE WHERE BUG_CASE_ID = %s) AND BUG_CASE_ID <> %s limit 10", [case_id, case_id])
            recommend_cases = cur.fetchall()
            print(screenshot_full_path)
            
        except AttributeError as e:
            print(f"Attribute Error: {e}") # 테스트용
        except Exception as e:
            print(f"An error occurred: {e}") # 테스트용
        finally:
            cur.close()
            
        return render_template('main.html', template_name='search/SearchDetail.html', search_detail_content='search/BugDetail.html', bug_case=bug_case, case_id=case_id, screenshot_info=screenshot_info, screenshot_full_path=screenshot_full_path, test_case=test_case, recommend_cases=recommend_cases)
    
    else:
        flash('case_code가 올바르지 않습니다.')
        return render_template('main.html', template_name='search/searchMain.html')



















# File Upload Section
@app.route('/upload/screenshot', methods=['POST'])
def upload_screenshot():
    file = request.files['file']
    if file:
        filename = os.path.join(SCREENSHOT_FOLDER.replace('/', os.sep), file.filename)
        file.save(filename)
        return {'path': filename}, 200
    # 경로를 받았다고 가정하고, 이를 'path' 변수에 저장
    else:
        return "File save failed"
    # 이제 이 'path'를 MySQL DB에 저장

@app.route('/upload/log', methods=['POST'])
def upload_log():
    if not os.path.exists('/static/Resource/Log'):
        os.makedirs('/static/Resource/Log')
    cur = mysql.connect.cursor()
    try:
        file = request.files['file']
        test_case_id = request.form.get('test_case_id')
        print('test_case_id is: ' + test_case_id)

        if file and test_case_id:
            # 파일 저장
            filename = os.path.join(LOG_FOLDER, file.filename).replace("\\", "/")
            file.save(filename)

            # 현재 날짜와 시간
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 데이터베이스에 로그 정보 삽입
            cur.execute(
                "INSERT INTO log (LOG_NAME, LOG_DATE) VALUES (%s, %s)",
                (file.filename, current_time)
            )
            # 생성된 log_id 가져오기
            log_id = cur.lastrowid
            cur.execute("update test_case set log_id = %s where test_case_id = %s", (log_id, test_case_id))
            # 모든 쿼리가 성공적으로 완료되면 커밋
            mysql.connect.commit()
            cur.execute("COMMIT")

            return f'File and log_id {log_id} uploaded successfully', 200

        else:
            mysql.connect.rollback()  # 문제가 있을 경우 롤백
            return 'Missing file or test_case_id', 400

    except Exception as e:
        print(f"Error: {e}")
        mysql.connect.rollback()  # 문제가 있을 경우 롤백
        return f"File upload failed: {e}", 500

    finally:
        cur.close()
    
@app.route('/upload/performance', methods=['POST'])
def upload_performance():
    if not os.path.exists('/static/Resource/Performance'):
        os.makedirs('/static/Resource/Performance')
    cur = mysql.connect.cursor()
    try:
        file = request.files['file']
        test_case_id = request.form.get('test_case_id')
        print('test_case_id is: ' + test_case_id)

        if file and test_case_id:
            # 파일 저장
            filename = os.path.join(PERFORMANCE_FOLDER, file.filename).replace("\\", "/")
            file.save(filename)

            # 현재 날짜와 시간
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 데이터베이스에 로그 정보 삽입
            cur.execute(
                "INSERT INTO PERFORMANCE (Performance_NAME, Performance_DATE) VALUES (%s, %s)",
                (file.filename, current_time)
            )
            # 생성된 performance_id 가져오기
            Performance_id = cur.lastrowid
            cur.execute("update test_case set Performance_id = %s where test_case_id = %s", (Performance_id, test_case_id))
            # 모든 쿼리가 성공적으로 완료되면 커밋
            mysql.connect.commit()
            cur.execute("COMMIT")

            return f'File and Performance {Performance_id} uploaded successfully', 200

        else:
            mysql.connect.rollback()  # 문제가 있을 경우 롤백
            return 'Missing file or test_case_id', 400

    except Exception as e:
        print(f"Error: {e}")
        mysql.connect.rollback()  # 문제가 있을 경우 롤백
        return f"File upload failed: {e}", 500

    finally:
        cur.close()
    
    
@app.route('/upload/playthrough_macro', methods=['POST'])
def upload_playthroughMacro():
    if not os.path.exists('/static/Resource/Macro'):
        os.makedirs('/static/Resource/Macro')
    cur = mysql.connect.cursor()
    try:
        file = request.files['file']
        test_case_id = request.form.get('test_case_id')
        print('test_case_id is: ' + test_case_id)

        if file and test_case_id:
            # 파일 저장
            filename = os.path.join(MACRO_FOLDER, file.filename).replace("\\", "/")
            file.save(filename)

            # 현재 날짜와 시간
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 데이터베이스에 로그 정보 삽입
            cur.execute(
                "INSERT INTO TEST_MACRO (TEST_MACRO_NAME, TEST_MACRO_PATH, TEST_MACRO_DATE, GAME_VERSION) VALUES (%s, %s, %s, %s)",
                (file.filename, filename, current_time, "3.0.0")
            )
            # 생성된 Macro_id 가져오기
            TEST_MACRO_id = cur.lastrowid
            cur.execute("update test_case set TEST_MACRO_ID = %s where test_case_id = %s", (TEST_MACRO_id, test_case_id))
            
            # 모든 쿼리가 성공적으로 완료되면 커밋
            mysql.connect.commit()
            cur.execute("COMMIT")

            return f'File and TEST_MACRO_id {TEST_MACRO_id} uploaded successfully', 200

        else:
            mysql.connect.rollback()  # 문제가 있을 경우 롤백
            return 'Missing file or test_case_id', 400

    except Exception as e:
        print(f"Error: {e}")
        mysql.connect.rollback()  # 문제가 있을 경우 롤백
        return f"File upload failed: {e}", 500

    finally:
        cur.close()
    
@app.route('/upload/macros', methods=['POST'])
def upload_macros():
    return "macros upload success"

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
    # serve(app, host='0.0.0.0', port=5000)