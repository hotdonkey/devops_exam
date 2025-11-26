# В Colab ячейке для запуска
import subprocess
import time
import requests
import threading

def start_flask_app():
    """Запуск Flask приложения в отдельном процессе"""
    print("Запуск Flask приложения...")
    process = subprocess.Popen([
        "python", "app.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Даем время на запуск
    time.sleep(3)
    return process

def check_app_ready():
    """Проверка готовности приложения"""
    max_retries = 10
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:8080/health", timeout=2)
            if response.status_code == 200:
                print("Приложение запущено и готово!")
                return True
        except:
            print(f"Ожидание запуска приложения... ({i+1}/{max_retries})")
            time.sleep(2)
    return False

# Запускаем приложение
flask_process = start_flask_app()

# Проверяем готовность
if check_app_ready():
    print("\nТестируем основные эндпоинты:")
    
    # Тест корневого эндпоинта
    try:
        response = requests.get("http://localhost:8080/")
        print(f"GET / -> {response.status_code}")
        if response.status_code == 200:
            print(f"   Ответ: {response.json()}")
    except Exception as e:
        print(f"   Ошибка: {e}")
    
    # Тест health
    try:
        response = requests.get("http://localhost:8080/health")
        print(f"GET /health -> {response.status_code}")
    except Exception as e:
        print(f"   Ошибка: {e}")
    
    print(f"\nПриложение доступно по адресу: http://localhost:8080")
    print("   Попробуйте открыть эту ссылку в браузере!")
    
else:
    print("Не удалось запустить приложение")
    # Выводим логи ошибок
    stdout, stderr = flask_process.communicate()
    print("STDOUT:", stdout.decode())
    print("STDERR:", stderr.decode())
    flask_process.terminate()