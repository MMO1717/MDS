from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)


# 这是一个内部函数，用于安全地执行SQL
def run_sql_query(connection_info, sql_query):
    conn = None
    try:
        # 从连接信息中获取凭证
        host = connection_info.get('host')
        port = connection_info.get('port')
        user = connection_info.get('user')
        password = connection_info.get('password')
        database = connection_info.get('database')

        # 建立数据库连接
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            db=database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()

        # 执行 SQL 语句
        cursor.execute(sql_query)

        # 提交修改 (如果是INSERT/UPDATE/DELETE等)
        conn.commit()

        # 如果是查询语句，获取结果
        if sql_query.strip().lower().startswith('select'):
            result = cursor.fetchall()
            return {'status': 'success', 'data': result}
        else:
            # 否则，返回受影响的行数
            affected_rows = cursor.rowcount
            return {'status': 'success', 'message': f'SQL executed successfully. Affected rows: {affected_rows}'}

    except Exception as e:
        if conn:
            conn.rollback()
        return {'status': 'error', 'message': str(e)}
    finally:
        if conn and conn.open:
            conn.close()


# 定义一个接口，用于执行SQL
@app.route('/execute_sql', methods=['POST'])
def execute_sql_api():
    # 检查请求是否包含JSON数据
    if not request.is_json:
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

    data = request.get_json()
    sql_query = data.get('sql_query')
    connection_info = data.get('connection_info')

    if not sql_query or not connection_info:
        return jsonify({"status": "error", "message": "Missing 'sql_query' or 'connection_info' in request"}), 400

    # 调用内部函数执行SQL
    result = run_sql_query(connection_info, sql_query)

    return jsonify(result)


# Flask应用入口
if __name__ == '__main__':
    # 在实际部署中，你可能需要使用gunicorn或其他WSGI服务器
    app.run(debug=True, port=5000)