from google.oauth2 import service_account
from google.cloud import bigquery

# 修改这里，填写你下载的 service_account.json 文件路径
CREDENTIAL_PATH = "friendly-medley-434600-j5-75bc1871a459.json"

def main():
    # 1. 加载服务账号凭证
    credentials = service_account.Credentials.from_service_account_file(CREDENTIAL_PATH)

    # 2. 创建 BigQuery 客户端
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    # 3. 准备一个示例查询（查询美国德州的名字数据）
    sql_query = """
    SELECT name 
    FROM `bigquery-public-data.usa_names.usa_1910_2013` 
    WHERE state = "TX" 
    LIMIT 10
    """

    print("Running query...")
    query_job = client.query(sql_query)  # 执行查询
    rows = query_job.result()            # 等待结果返回

    # 4. 输出结果
    print("Query results:")
    for row in rows:
        print(row.name)

if __name__ == "__main__":
    main()