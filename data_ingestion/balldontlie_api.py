import requests
import time
import os
import json
from tenacity import retry, stop_after_attempt, wait_exponential

class BallDontLieLoader:
    def __init__(self, config):
        self.api_key = os.getenv("BALLDONTLIE_API_KEY")
        self.base_url = config['data_sources']['balldontlie']['base_url']
        self.headers = {"Authorization": self.api_key}
        self.delay = config['data_sources']['balldontlie']['rate_limit_delay']

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def fetch_data(self, endpoint, params=None):
        response = requests.get(
            f"{self.base_url}/{endpoint}",
            headers=self.headers,
            params=params,
            timeout=30
        )
        if response.status_code == 429:
            raise Exception("Rate limit exceeded")
        response.raise_for_status()
        return response.json()

    def run(self):
        print("Подключение к BALLDONTLIE API...")
        teams = self.fetch_data("teams")
        
        #выводим количество в консоль
        teams_list = teams.get('data', [])
        print(f"Получено команд: {len(teams_list)}")
        
        # сохраняем в файл, чтобы вы могли его открыть
        #создаем папку storage/raw, если её нет
        os.makedirs("storage/raw", exist_ok=True)
        
        #записываем данные в JSON файл
        with open("storage/raw/balldontlie_teams.json", "w", encoding="utf-8") as f:
            json.dump(teams, f, indent=4, ensure_ascii=False)
            
        print("-------Сырые данные API сохранены в файл: storage/raw/balldontlie_teams.json")
        
        time.sleep(self.delay)