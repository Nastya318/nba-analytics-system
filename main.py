import os
import yaml
from dotenv import load_dotenv
from data_ingestion.kaggle_loader import KaggleLoader
from data_ingestion.balldontlie_api import BallDontLieLoader

def main():
    print("!!!!!!!Запуск NBA Predictive Analytics System!!!!!!!")
    
    #загрузка конфигурации
    load_dotenv()
    with open("config/settings.yaml", "r") as f:
        config = yaml.safe_load(f)
    
    #загрузка данных из Kaggle
    kaggle = KaggleLoader(config)
    kaggle.run()
    
    #загрузка данных из API
    api = BallDontLieLoader(config)
    api.run()
    
    print("---------- Пайплайн успешно завершен!")

if __name__ == "__main__":
    main()