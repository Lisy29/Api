# Importamos las bibliotecas necesarias
import pandas as pd
from sklearn.model_selection import KFold, cross_val_score, GridSearchCV, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, accuracy_score, roc_curve, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import joblib
import seaborn as sns

# Cargar el archivo CSV proporcionado
file_path = 'data/airline_passenger_satisfaction_model.csv'
df = pd.read_csv(file_path)

# Dividimos el dataset en características (X) y variable objetivo (y)
X = df.drop(columns=['satisfaction'])
y = df['satisfaction']

# Dividir los datos en conjunto de entrenamiento y conjunto de prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Configurar la validación cruzada con K-Fold
kf = KFold(n_splits=5, shuffle=True, random_state=42)  # 5-fold cross-validation

# Definir el espacio de búsqueda de hiperparámetros para Regresión Logística
param_grid_lr = {
    'C': [0.01, 0.1, 1, 10, 100],
    'penalty': ['l2'],
    'solver': ['lbfgs', 'liblinear'],
    'max_iter': [100, 200, 300]
}

# Configurar la búsqueda de hiperparámetros para Regresión Logística
log_reg_model = LogisticRegression(random_state=42)
grid_search_lr = GridSearchCV(estimator=log_reg_model, param_grid=param_grid_lr, cv=kf, scoring='accuracy', n_jobs=-1, verbose=2)

# Entrenar el modelo de Regresión Logística con la búsqueda de hiperparámetros
grid_search_lr.fit(X_train, y_train)

# Evaluar el modelo ajustado en el conjunto de test
best_lr_model = grid_search_lr.best_estimator_
y_pred_lr = best_lr_model.predict(X_test)

# Imprimir los resultados del modelo de Regresión Logística
print("Best parameters found for Logistic Regression:", grid_search_lr.best_params_)
print("Logistic Regression Test Accuracy:", accuracy_score(y_test, y_pred_lr))
print("Logistic Regression Confusion Matrix:\n", confusion_matrix(y_test, y_pred_lr))
print("Logistic Regression Classification Report:\n", classification_report(y_test, y_pred_lr)) # Reporte de clasificación (incluye precision, recall y f1-score)
roc_auc = roc_auc_score(y_test, best_lr_model.predict_proba(X_test)[:, 1])
print("Logistic Regresion AUC:", roc_auc)

# Cálculo de métricas adicionales
accuracy = accuracy_score(y_test, y_pred_lr)
precision = precision_score(y_test, y_pred_lr, average='binary')  # Cambia 'binary' según el tipo de clasificación
recall = recall_score(y_test, y_pred_lr, average='binary')
f1 = f1_score(y_test, y_pred_lr, average='binary')

# Modelo de Regresión Logística
log_reg_model = LogisticRegression(max_iter=1000, random_state=42)

# Evaluar el modelo utilizando validación cruzada
cv_scores_log_reg = cross_val_score(log_reg_model, X, y, cv=kf, scoring='accuracy')

# Imprimir los resultados
print("\nLogistic Regression Cross-Validation Accuracy Scores:", cv_scores_log_reg)
print("Logistic Regression Mean Accuracy:", cv_scores_log_reg.mean())
print("Logistic Regression Standard Deviation:", cv_scores_log_reg.std())

# Plot ROC Curve for Logistic Regresion
fpr_lr, tpr_lr, _ = roc_curve(y_test, best_lr_model.predict_proba(X_test)[:, 1])

plt.figure()
plt.plot(fpr_lr, tpr_lr, color='green', lw=2, label='Logistic Regression (AUC = %0.2f)' % roc_auc_score(y_test, best_lr_model.predict_proba(X_test)[:, 1]))
plt.plot([0, 1], [0, 1], color='red', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc="lower right")
plt.show()

# Guardar el modelo en un archivo
joblib.dump(log_reg_model, 'models/lr_model.pkl')
print("Modelo guardado como lr_model.pkl")

#Métricas
metricsdf = pd.DataFrame({
    'Model': ['LR'],
    'Accuracy': [accuracy],
    'Precision': [precision],
    'Recall': [recall],
    'F1_Score': [f1],
    'AUC_ROC': [roc_auc],
    'Best_Parameters': [str(grid_search_lr.best_params_)]
})

# Cargar métricas existentes (si las hay) y guardar en un archivo CSV
try:
    existing_metrics = pd.read_csv('metrics/model_metrics.csv')
    updated_metrics = pd.concat([existing_metrics, metricsdf], ignore_index=True)
except FileNotFoundError:
    updated_metrics = metricsdf

updated_metrics.to_csv('metrics/model_metrics.csv', index=False)
print("Métricas guardadas en 'model_metrics.csv'")

# Visualización
plt.figure(figsize=(10, 6))
sns.barplot(x=['Accuracy', 'Precision', 'Recall', 'F1_Score', 'AUC_ROC'], 
            y=[accuracy, precision, recall, f1, roc_auc])
plt.title('Métricas del Modelo Logistic Regresion')
plt.ylim(0, 1)
plt.savefig('metrics/lr_metrics.png')
plt.close()
print("Gráfico de métricas guardado como 'lr_metrics.png'")