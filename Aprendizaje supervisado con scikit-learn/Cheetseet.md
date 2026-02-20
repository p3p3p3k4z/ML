
##🛠️ Fase 1: Preprocesamiento (Data Cleaning)

Antes de que el modelo aprenda, los datos deben ser numéricos y estar completos.

### Datos Categóricos (Dummy Variables)

Transforma texto en columnas binarias (0 y 1).

```python
# Regla N-1: drop_first=True evita redundancia
df_dummies = pd.get_dummies(df, drop_first=True)
```

### Tratamiento de Nulos (Imputation)

No borres datos si puedes "adivinar" su valor.

- **Numéricos:** `strategy="mean"` o `"median"`.
    
- **Categóricos:** `strategy="most_frequent"`.
    


```python
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy="mean")
X_train_imputed = imputer.fit_transform(X_train)
```

### Centrado y Escalado (Scaling)

Vital para modelos basados en distancia (KNN, LogReg).

- **StandardScaler:** Media 0 y Varianza 1. $z = \frac{x - \mu}{\sigma}$
    

```python
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
```

---

## 📊 Fase 2: Modelado y Evaluación

### Clasificación (¿Es A o B?)

- **Modelos:** `KNeighborsClassifier`, `LogisticRegression`, `DecisionTreeClassifier`.
    
- **Métricas Clave:**
    
    - **Matriz de Confusión:** Para ver errores Tipo I (FP) y Tipo II (FN).
        
    - **Precisión:** $\frac{TP}{TP + FP}$ (Evitar falsas alarmas).
        
    - **Recall:** $\frac{TP}{TP + FN}$ (No omitir casos reales).
        
    - **ROC AUC:** Capacidad del modelo para distinguir clases (0.5 es azar, 1.0 es perfecto).
        

### Regresión (¿Cuánto vale X?)

- **Modelos:** `LinearRegression`, `Ridge` (Regularización $L_2$), `Lasso` (Regularización $L_1$).
    
- **Métricas Clave:**
    
    - **$R^2$:** Qué tanta variabilidad explicas (mejor cuanto más cerca de 1).
        
    - **RMSE:** El error promedio en las mismas unidades que el objetivo.
        
        $$RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2}$$
        

---

## 🚀 Fase 3: Optimización (Hyperparameter Tuning)

Para no "adivinar" los parámetros, deja que el código busque por ti.

|**Técnica**|**Cuándo usarla**|
|---|---|
|**GridSearchCV**|Espacios de búsqueda pequeños. Es exhaustivo y lento.|
|**RandomizedSearchCV**|Espacios grandes. Más rápido, ideal para pipelines de CI/CD.|


```python
# Sintaxis para Pipeline: nombrepaso__nombreparametro
params = {"model__n_neighbors": np.arange(1, 50)}
cv = GridSearchCV(pipeline, param_grid=params, cv=5)
```

---

## 🏗️ Fase 4: Producción y DevOps (Pipelines)

El **Pipeline** es tu "script de automatización" que encapsula todo el flujo. Es el archivo que realmente despliegas en un servidor.


```python
from sklearn.pipeline import Pipeline

# Definir el flujo (Transformer, Transformer, Estimator)
steps = [
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(C=0.5))
]

pipeline = Pipeline(steps)
pipeline.fit(X_train, y_train) # Entrena todo el flujo a la vez
```

---

## 💡 Pro-Tips para tu Carrera

1. **Evita el Data Leakage:** Nunca hagas `fit` sobre el Test Set. El escalador y el imputador solo aprenden del Train Set.
    
2. **Lasso como SysAdmin:** Si tienes demasiadas métricas en tus logs y no sabes cuáles importan, usa `Lasso`. Reducirá a cero los coeficientes de las variables que no aportan nada.
    
3. **Cross-Validation:** No confíes en un solo `train_test_split`. Usa `KFold` para asegurar que tu modelo sea robusto ante diferentes segmentos de datos.
    
