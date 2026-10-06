import kagglehub
import pandas as pd
import os
import shutil
from datetime import datetime

class KaggleLoader:
    def __init__(self, config):
        self.config = config
        # Создаём папку для сырых данных Kaggle
        self.raw_dir = "storage/raw/kaggle"
        os.makedirs(self.raw_dir, exist_ok=True)
        
    def run(self):
        print("Загрузка данных из Kaggle....................")
        
        #cкачиваем датасет в кэш Kaggle
        path = kagglehub.dataset_download(
            self.config['data_sources']['kaggle']['dataset']
        )
        print(f"Датасет скачан в кэш: {path}")
        
        #находим папку с распакованными файлами
        versions_dir = os.path.join(path, "versions")
        if os.path.exists(versions_dir):
            #берём последнюю версию (папку с максимальным номером)
            version_folders = sorted(os.listdir(versions_dir))
            latest_version = os.path.join(versions_dir, version_folders[-1])
            source_dir = latest_version
        else:
            source_dir = path
        
        print(f"--------Источник файлов: {source_dir}")
        
        #копируем ВСЕ CSV файлы из папки
        copied_count = 0
        total_rows = 0
        
        for filename in os.listdir(source_dir):
            if filename.endswith(".csv"):
                source_path = os.path.join(source_dir, filename)
                target_path = os.path.join(self.raw_dir, filename)
                
                #копируем файл
                shutil.copy2(source_path, target_path)
                copied_count += 1
                
                #считаем строки для отчёта
                try:
                    df = pd.read_csv(target_path, nrows=0)  # Читаем только заголовки
                    row_count = sum(1 for _ in open(target_path, encoding='utf-8')) - 1
                    total_rows += row_count
                    print(f"--------------{filename}: {row_count} строк")
                except Exception as e:
                    print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!Не удалось прочитать {filename}: {e}")
        
        print(f"\nСкопировано файлов: {copied_count}")
        print(f"Всего строк данных: {total_rows}")
        print(f"Все сырые данные Kaggle сохранены в: {self.raw_dir}")