import pymysql
import os

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'aaa1234512345',
    'database': 'transportation'
}

# 图片下载目录
DOWNLOAD_FOLDER = 'downloaded_images'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_image(image_id):
    # 连接到数据库
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    try:
        # 查询图片数据
        cursor.execute("SELECT file_type, image_data FROM images WHERE id = %s", (image_id,))
        result = cursor.fetchone()

        if result:
            file_type, image_data = result
            print(f"Image data length: {len(image_data)}")  # 打印数据长度
            file_extension = file_type.split('/')[-1]  # 获取文件扩展名
            file_path = os.path.join(DOWNLOAD_FOLDER, f"{image_id}.{file_extension}")

            # 将图片数据写入文件
            with open(file_path, 'wb') as file:
                file.write(image_data)

            print(f"图片已下载到: {file_path}")
        else:
            print("未找到指定ID的图片。")

    except Exception as e:
        print(f"下载图片时出错: {str(e)}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    image_id = input("请输入要下载图片在数据库中的ID: ")
    download_image(image_id)