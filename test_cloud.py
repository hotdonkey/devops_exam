import requests
import time
import json
import sys

def test_service():
    print("=== ТЕСТИРОВАНИЕ СЕРВИСА ===")
    
    #base_url = "https://bbav7reetq7c84fe177c.containers.yandexcloud.net:8080"
    base_url = "https://bbav7reetq7c84fe177c.containers.yandexcloud.net"
    
    # Тест корневого эндпоинта
    try:
        print("\n1. Тестируем корневой эндпоинт /")
        resp = requests.get(f"{base_url}/", timeout=5)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"Service: {data.get('service')}")
            print(f"Status: {data.get('status')}")
        else:
            print(f"Error: {resp.text}")
    except Exception as e:
        print(f"Ошибка: {e}")
        return False
    
    # Тест здоровья
    try:
        print("\n2. Тестируем /health")
        resp = requests.get(f"{base_url}/health", timeout=5)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            print(f"Health: {resp.json().get('status')}")
        else:
            print(f"Error: {resp.text}")
    except Exception as e:
        print(f"Ошибка: {e}")
        return False
    
    # Тест healthcheck
    try:
        print("\n3. Тестируем /healthcheck")
        resp = requests.get(f"{base_url}/healthcheck", timeout=5)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            print("Healthcheck: OK")
        else:
            print(f"Error: {resp.text}")
    except Exception as e:
        print(f"Ошибка: {e}")
        return False
    
    # Тест информации о модели
    try:
        print("\n4. Тестируем /model/info")
        resp = requests.get(f"{base_url}/model/info", timeout=5)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            info = resp.json()
            print(f"Model: {info.get('model_type')}")
            print(f"Accuracy: {info.get('accuracy')}")
        else:
            print(f"Error: {resp.text}")
    except Exception as e:
        print(f"Ошибка: {e}")
        return False
    
    # Тест предсказания
    try:
        print("\n5. Тестируем /predict")
        test_data = {
            "features": [5.1, 3.5, 1.4, 0.2]  # setosa
        }
        
        resp = requests.post(f"{base_url}/predict", json=test_data, timeout=5)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            result = resp.json()
            print(f"Prediction: {result['species']}")
            print(f"Confidence: {result['confidence']:.2f}")
        else:
            print(f"Error: {resp.text}")
    except Exception as e:
        print(f"Ошибка: {e}")
        return False
    
    # Тест метрик
    try:
        print("\n6. Тестируем /metrics")
        resp = requests.get(f"{base_url}/metrics", timeout=5)
        print(f"Status: {resp.status_code}")
        if resp.status_code == 200:
            metrics = resp.json()
            print(f"Dataset size: {metrics.get('dataset_size')}")
        else:
            print(f"Error: {resp.text}")
    except Exception as e:
        print(f"Ошибка: {e}")
        return False
    
    print("\nВсе тесты пройдены успешно!")
    return True

if __name__ == "__main__":
    success = test_service()
    sys.exit(0 if success else 1)