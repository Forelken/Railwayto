import os
import datetime
import subprocess
from flask import current_app as app
from dotenv import load_dotenv
import yadisk

load_dotenv()

def create_backup():
    # Настройки Яндекс.Диска
    YANDEX_DISK_TOKEN = os.getenv('YANDEX_DISK_TOKEN')
    # Имя файла резервной копии
    backup_filename = f"backup_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql"
    backup_path = os.path.join(os.getcwd(), backup_filename)

    # Создание резервной копии с помощью pg_dump
    pg_dump_path = r'C:\Program Files\PostgreSQL\17\bin\pg_dump.exe'
    try:
        result = subprocess.run(
            [pg_dump_path, '-U', os.getenv('DB_USER'), '-h', '127.0.0.1', os.getenv('DB_NAME'), '-f', backup_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            print(f"pg_dump stdout: {result.stdout.decode()}")
            print(f"pg_dump stderr: {result.stderr.decode()}")
            raise Exception(result.stderr.decode())
    except Exception as e:
        print(f"Error creating backup: {e}")
        return

    # Загрузка на Яндекс.Диск
    y = yadisk.YaDisk(token=YANDEX_DISK_TOKEN)
    try:
        y.upload(backup_path, f"/dump_sql/{backup_filename}")
    except Exception as e:
        print(f"Error uploading backup: {e}")
        return

    # Удаление локального файла резервной копии
    try:
        os.remove(backup_path)
    except Exception as e:
        print(f"Error deleting backup file: {e}")
        return

    print('Backup successfully created and uploaded to Yandex.Disk')

if __name__ == '__main__':
    create_backup()
