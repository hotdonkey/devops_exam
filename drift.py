import pandas as pd
import numpy as np
from sklearn.datasets import load_iris
from evidently.report import Report
from evidently.metric_preset import DataQualityPreset, DataDriftPreset

def check_drift():
    print("Проверяем дрейф данных...")
    
    # Референсные данные
    iris = load_iris()
    reference_data = pd.DataFrame(iris.data, columns=iris.feature_names)
    
    # Текущие данные (с небольшим дрейфом)
    current_data = pd.DataFrame(iris.data, columns=iris.feature_names)
    current_data['petal length (cm)'] *= 1.1
    current_data['sepal width (cm)'] += 0.1
    
    # Создаем отчет
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_data, current_data=current_data)
    
    # Сохраняем отчет
    report.save_html('drift_report_simple.html')
    
    # Простой анализ
    result = report.as_dict()
    drift_detected = result['metrics'][0]['result']['dataset_drift']
    drifted_features = result['metrics'][0]['result']['number_of_drifted_columns']
    
    print(f"Дрейф обнаружен: {drift_detected}")
    print(f"Дрейфнувших фич: {drifted_features}")
    
    return drift_detected

if __name__ == "__main__":
    check_drift()