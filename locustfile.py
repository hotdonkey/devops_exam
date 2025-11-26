from locust import HttpUser, task, between
import random
import json

class IrisAPIUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Вызывается при создании каждого пользователя"""
        self.client.headers = {
            "Content-Type": "application/json",
            "User-Agent": "LocustLoadTest/1.0"
        }
    
    @task(3)
    def health_check(self):
        """Проверка здоровья сервиса"""
        with self.client.get("/health", catch_response=True, name="/health") as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Health check failed: {response.status_code}")
    
    @task(2)
    def healthcheck_endpoint(self):
        """Альтернативный health check"""
        with self.client.get("/healthcheck", catch_response=True, name="/healthcheck") as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Healthcheck failed: {response.status_code}")
    
    @task(5)
    def make_prediction(self):
        """Основная задача - предсказание"""
        # Генерация реалистичных данных ириса
        features = [
            round(random.uniform(4.5, 7.5), 2),  # sepal_length
            round(random.uniform(2.0, 4.0), 2),  # sepal_width
            round(random.uniform(1.0, 6.5), 2),  # petal_length
            round(random.uniform(0.1, 2.5), 2)   # petal_width
        ]
        
        payload = {"features": features}
        
        with self.client.post("/predict", 
                            json=payload,
                            catch_response=True,
                            name="/predict") as response:
            if response.status_code == 200:
                data = response.json()
                if "prediction" in data and "species" in data:
                    response.success()
                else:
                    response.failure("Invalid prediction response format")
            else:
                response.failure(f"Prediction failed: {response.status_code} - {response.text}")
    
    @task(2)
    def get_model_info(self):
        """Получение информации о модели"""
        with self.client.get("/model/info", catch_response=True, name="/model/info") as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Model info failed: {response.status_code}")
    
    @task(1)
    def get_metrics(self):
        """Получение метрик"""
        with self.client.get("/metrics", catch_response=True, name="/metrics") as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Metrics failed: {response.status_code}")
    
    @task(1)
    def get_root(self):
        """Получение корневой страницы"""
        with self.client.get("/", catch_response=True, name="/") as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Root endpoint failed: {response.status_code}")