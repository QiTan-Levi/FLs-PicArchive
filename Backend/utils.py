import pymysql as ysq
from configparser import ConfigParser
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import pymongo
from gridfs import GridFS

verification_codes = {}
mysql = None
mongodb = None
fs = None

def init_db_connections():
    global mysql, mongodb, fs
    config = ConfigParser()
    config.read('config.ini')
    data_host = config.get('Database', 'Host')
    data_username = config.get('Database', 'User')
    data_password = config.get('Database', 'Password')
    data_databasename = config.get('Database', 'Database')
    
    mysql = ysq.connect(
        host=data_host,
        user=data_username,
        password=data_password,
        database=data_databasename
    )
    
    mongodb = pymongo.MongoClient("mongodb://localhost:27017/")["transportation"]
    fs = GridFS(mongodb)

    return mysql, mongodb, fs

def send_verification_email(email, code):
    with open('verifycode_email_template.html', 'r', encoding='utf-8') as f:
        html_content = f.read().replace('{{verification_code}}', code)
    
    msg = MIMEText(html_content, 'html', 'utf-8')
    msg['From'] = Header("ByInfo Service", 'utf-8')
    msg['To'] = email
    msg['Subject'] = Header('ByInfo Service Picture Archive 验证码', 'utf-8')
    
    try:
        smtp = smtplib.SMTP_SSL("smtp.163.com", 465)
        smtp.login("byinfosvc@163.com", "BMSvkGwzrVE8fijz")
        smtp.sendmail("byinfosvc@163.com", [email], msg.as_string())
        smtp.quit()
        print(f"验证码已发送到 {email}")
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")