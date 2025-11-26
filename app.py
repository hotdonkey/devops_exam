from flask import Flask, jsonify, request
import joblib
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import time
import os
import socket

app = Flask(__name__)

# Загрузка/обучение модели при старте
def load_model():
    model_path = 'iris_model.joblib'
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        iris = load_iris()
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(iris.data, iris.target)
        joblib.dump(model, model_path)
        return model

model = load_model()
iris_data = load_iris()
feature_names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
target_names = ['setosa', 'versicolor', 'virginica']

# Модуль 1: Здоровье и информация
@app.route('/')
def home():
    return jsonify({
        "service": "Iris Classification API",
        "version": "1.0",
        "status": "running",
        "hostname": socket.gethostname(),
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "model_info": "/model/info",
            "metrics": "/metrics"
        },
        "example_request": {
            "url": "/predict",
            "method": "POST",
            "body": {"features": [5.1, 3.5, 1.4, 0.2]}
        }
    })

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy", 
        "timestamp": time.time(),
        "service": "Iris API"
    })

@app.route('/healthcheck')
def healthcheck():
    """Альтернативный эндпоинт для health checks"""
    return jsonify({"status": "OK"}), 200

# Модуль 2: Предсказания
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        if not data or 'features' not in data:
            return jsonify({"error": "No features provided"}), 400
            
        features = data.get('features', [])
        
        if len(features) != 4:
            return jsonify({"error": "Need exactly 4 features"}), 400
        
        # Проверка типов данных
        try:
            features_array = np.array(features, dtype=float).reshape(1, -1)
        except ValueError:
            return jsonify({"error": "All features must be numbers"}), 400
        
        # Предсказание
        prediction = model.predict(features_array)[0]
        probabilities = model.predict_proba(features_array)[0]
        
        return jsonify({
            "prediction": int(prediction),
            "species": target_names[prediction],
            "confidence": float(max(probabilities)),
            "probabilities": {
                target_names[i]: float(prob) for i, prob in enumerate(probabilities)
            },
            "features_received": features
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Модуль 3: Информация о модели
@app.route('/model/info')
def model_info():
    accuracy = model.score(iris_data.data, iris_data.target)
    return jsonify({
        "model_type": "RandomForest",
        "accuracy": round(accuracy, 3),
        "n_estimators": 100,
        "features": feature_names,
        "classes": target_names,
        "dataset_size": len(iris_data.data)
    })

# Модуль 4: Мониторинг и метрики
@app.route('/metrics')
def metrics():
    feature_means = np.mean(iris_data.data, axis=0)
    feature_stds = np.std(iris_data.data, axis=0)
    
    return jsonify({
        "dataset_size": len(iris_data.data),
        "feature_statistics": {
            feature_names[i]: {
                "mean": float(feature_means[i]),
                "std": float(feature_stds[i])
            } for i in range(len(feature_names))
        },
        "model_accuracy": round(model.score(iris_data.data, iris_data.target), 3)
    })

if __name__ == '__main__':
    # Используем порт из переменной окружения или 5025 по умолчанию
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)