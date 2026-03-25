"""
=============================================================
  CLASIFICACIÓN BINARIA — 3 PROBLEMAS
  Alumna: Itzelt Yamileth Cedillo Hernandez 2330457
  Universidad Politécnica de Victoria — Ingeniería Mecatrónica
=============================================================
  Problema 1 — Heart Disease (BRFSS 2015)
  Problema 2 — Credit Card Fraud Detection
  Problema 3 — Titanic Survival
"""
 
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
import kagglehub
from kagglehub import KaggleDatasetAdapter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    precision_recall_curve,
)
 
SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)
 
print("Dispositivos disponibles:", tf.config.list_physical_devices())
 

 
def split_and_scale(X, y):
    """Split 70/15/15 estratificado + StandardScaler sin data leakage."""
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, stratify=y, random_state=SEED
    )
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, stratify=y_temp, random_state=SEED
    )
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val   = scaler.transform(X_val)
    X_test  = scaler.transform(X_test)
    print(f"Train: {len(X_train)} | Val: {len(X_val)} | Test: {len(X_test)}")
    return X_train, X_val, X_test, y_train, y_val, y_test
 
 
def get_class_weights(y_train):
    weights = compute_class_weight(class_weight="balanced",
                                   classes=np.array([0, 1]), y=y_train)
    cw = {0: float(weights[0]), 1: float(weights[1])}
    print(f"Pesos de clase: {cw}")
    return cw
 
 
def evaluate_threshold(pred_test, y_test, t):
    y_pred = (pred_test >= t).astype(int)
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    rec = tp / (tp + fn + 1e-12)
    pre = tp / (tp + fp + 1e-12)
    return cm, pre, rec
 
 
def find_best_threshold(pred_test, y_test, target_recall, n=100):
    thresholds = np.linspace(0.05, 0.95, n)
    recall_values, precision_values = [], []
    for t in thresholds:
        _, pre, rec = evaluate_threshold(pred_test, y_test, t)
        recall_values.append(rec)
        precision_values.append(pre)
 
    best_threshold, best_precision = 0.5, -1
    for t, pre, rec in zip(thresholds, precision_values, recall_values):
        if rec >= target_recall and pre > best_precision:
            best_precision = pre
            best_threshold = t
 
    return best_threshold, thresholds, recall_values, precision_values
 
 
################################################################
#  FUNCIONES DE GRAFICADO COMUNES
################################################################
 
def plot_training_curves(history, title, metrics_keys, save_name):
    """Curvas de entrenamiento 2x2."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(title, fontsize=14, fontweight="bold")
    labels = ["Loss", metrics_keys[0].upper(), metrics_keys[1].upper(), metrics_keys[2].upper()]
    keys   = ["loss"] + metrics_keys
    for ax, key, label in zip(axes.ravel(), keys, labels):
        ax.plot(history.history[key],           label="Train")
        ax.plot(history.history[f"val_{key}"],  label="Validacion")
        ax.set_title(label)
        ax.legend()
        ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_name, dpi=150)
    plt.show()
    print(f"Guardado: {save_name}")
 
 
def plot_roc(y_test, pred_test, auc_roc, title, save_name, color="steelblue"):
    fpr, tpr, _ = roc_curve(y_test, pred_test)
    plt.figure(figsize=(7, 5))
    plt.plot(fpr, tpr, color=color, lw=2, label=f"ROC (AUC = {auc_roc:.3f})")
    plt.plot([0, 1], [0, 1], "k--", lw=1)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_name, dpi=150)
    plt.show()
    print(f"Guardado: {save_name}")
 
 
def plot_pr(y_test, pred_test, auc_pr, title, save_name, color="darkorange"):
    pre_curve, rec_curve, _ = precision_recall_curve(y_test, pred_test)
    plt.figure(figsize=(7, 5))
    plt.plot(rec_curve, pre_curve, color=color, lw=2, label=f"PR (AUC = {auc_pr:.3f})")
    plt.axhline(y=y_test.mean(), color="gray", linestyle="--", label="Baseline (prior)")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_name, dpi=150)
    plt.show()
    print(f"Guardado: {save_name}")
 
 
def plot_confusion(cm, class_names, threshold, title, save_name, cmap="Blues"):
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap=cmap,
                xticklabels=class_names, yticklabels=class_names)
    plt.xlabel("Predicho")
    plt.ylabel("Real")
    plt.title(f"{title} (umbral = {threshold:.2f})")
    plt.tight_layout()
    plt.savefig(save_name, dpi=150)
    plt.show()
    print(f"Guardado: {save_name}")
 
 
def plot_threshold_analysis(thresholds, recall_values, precision_values,
                            best_threshold, target_recall, title, save_name,
                            recall_color="steelblue", precision_color="darkorange"):
    plt.figure(figsize=(8, 5))
    plt.plot(thresholds, recall_values,    label="Recall",    color=recall_color,    lw=2)
    plt.plot(thresholds, precision_values, label="Precision", color=precision_color, lw=2)
    plt.axvline(x=best_threshold, color="red",   linestyle="--",
                label=f"Umbral elegido = {best_threshold:.2f}")
    plt.axhline(y=target_recall,  color="green", linestyle=":",  alpha=0.7,
                label=f"Recall objetivo >= {target_recall}")
    plt.xlabel("Umbral")
    plt.ylabel("Score")
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_name, dpi=150)
    plt.show()
    print(f"Guardado: {save_name}")
 
 
###################################################
#  PROBLEMA 1 — HEART DISEASE (BRFSS 2015)        #
###################################################
 
print("\n" + "="*60)
print("  PROBLEMA 1 — HEART DISEASE")
print("="*60)
 
df1 = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "alexteboul/heart-disease-health-indicators-dataset",
    "heart_disease_health_indicators_BRFSS2015.csv",
)
print(f"Shape: {df1.shape}")
print(df1.head())
print(df1["HeartDiseaseorAttack"].value_counts())
 
TARGET1 = "HeartDiseaseorAttack"
X1 = df1.drop(columns=[TARGET1]).values.astype(np.float32)
y1 = df1[TARGET1].values.astype(np.int32)
print(f"Clase 0: {np.sum(y1==0)} | Clase 1: {np.sum(y1==1)}")
 
# Preprocesamiento 
X1_train, X1_val, X1_test, y1_train, y1_val, y1_test = split_and_scale(X1, y1)
cw1 = get_class_weights(y1_train)
 
# Modelo 
def create_model_heart(input_dim):
    inputs = tf.keras.Input(shape=(input_dim,))
    x = tf.keras.layers.Dense(128, activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(1e-4))(inputs)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.30)(x)
    x = tf.keras.layers.Dense(64, activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(1e-4))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.25)(x)
    x = tf.keras.layers.Dense(32, activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(1e-4))(x)
    x = tf.keras.layers.Dropout(0.20)(x)
    outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)
    return tf.keras.Model(inputs, outputs)
 
model1 = create_model_heart(X1_train.shape[1])
model1.summary()
 
model1.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="binary_crossentropy",
    metrics=[
        tf.keras.metrics.AUC(curve="ROC", name="auc_roc"),
        tf.keras.metrics.AUC(curve="PR",  name="auc_pr"),
        tf.keras.metrics.Recall(name="recall"),
        tf.keras.metrics.Precision(name="precision"),
    ],
)
 
callbacks1 = [
    tf.keras.callbacks.EarlyStopping(
        monitor="val_auc_roc", mode="max", patience=20,
        restore_best_weights=True, verbose=1),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_auc_roc", mode="max", factor=0.5,
        patience=8, min_lr=1e-6, verbose=1),
]
 
history1 = model1.fit(
    X1_train, y1_train,
    validation_data=(X1_val, y1_val),
    epochs=300, batch_size=512,
    class_weight=cw1, callbacks=callbacks1, verbose=1,
)
 
#  Evaluacion 
pred1 = model1.predict(X1_test).ravel()
auc_roc1 = roc_auc_score(y1_test, pred1)
auc_pr1  = average_precision_score(y1_test, pred1)
print(f"AUC-ROC: {auc_roc1:.4f} | AUC-PR: {auc_pr1:.4f}")
 
TARGET_RECALL1 = 0.70
best_t1, thresholds1, rec1, pre1 = find_best_threshold(pred1, y1_test, TARGET_RECALL1)
cm1, pf1, rf1 = evaluate_threshold(pred1, y1_test, best_t1)
tn1, fp1, fn1, tp1 = cm1.ravel()
print(f"Umbral: {best_t1:.2f} | Recall: {rf1:.4f} | Precision: {pf1:.4f} | FN: {fn1}")
print(classification_report(
    y1_test, (pred1 >= best_t1).astype(int),
    target_names=["Sin enfermedad", "Con enfermedad"]))
 
#  Gráficas 
plot_training_curves(history1,
    "Curvas de Entrenamiento — Heart Disease MLP",
    ["auc_roc", "recall", "precision"],
    "training_curves_heart.png")
 
plot_roc(y1_test, pred1, auc_roc1,
    "Curva ROC — Heart Disease", "roc_curve_heart.png")
 
plot_pr(y1_test, pred1, auc_pr1,
    "Curva Precision-Recall — Heart Disease", "pr_curve_heart.png",
    color="darkorange")
 
plot_confusion(cm1, ["Sin enfermedad", "Con enfermedad"], best_t1,
    "Matriz de Confusión — Heart Disease", "confusion_matrix_heart.png")
 
plot_threshold_analysis(thresholds1, rec1, pre1, best_t1, TARGET_RECALL1,
    "Precision y Recall vs Umbral — Justificación del corte",
    "threshold_heart.png")
 
 
# #################################################
#  PROBLEMA 2 — CREDIT CARD FRAUD DETECTION       #
# #################################################
 
print("\n" + "="*60)
print("  PROBLEMA 2 — CREDIT CARD FRAUD")
print("="*60)
 
#  Carga 
df2 = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "mlg-ulb/creditcardfraud",
    "creditcard.csv",
)
print(f"Shape: {df2.shape}")
print(df2["Class"].value_counts())
 
TARGET2 = "Class"
X2 = df2.drop(columns=[TARGET2, "Time"]).values.astype(np.float32)
y2 = df2[TARGET2].values.astype(np.int32)
print(f"Clase 0 (Legítima): {np.sum(y2==0)} | Clase 1 (Fraude): {np.sum(y2==1)}")
print(f"Proporción fraude: {y2.mean()*100:.4f}%")
 
# Preprocesamiento
X2_train, X2_val, X2_test, y2_train, y2_val, y2_test = split_and_scale(X2, y2)
cw2 = get_class_weights(y2_train)
 
#  Modelo
def create_model_fraud(input_dim):
    inputs = tf.keras.Input(shape=(input_dim,))
    x = tf.keras.layers.Dense(256, activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(1e-4))(inputs)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.40)(x)
    x = tf.keras.layers.Dense(128, activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(1e-4))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.35)(x)
    x = tf.keras.layers.Dense(64, activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(1e-4))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.30)(x)
    x = tf.keras.layers.Dense(32, activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(1e-4))(x)
    x = tf.keras.layers.Dropout(0.20)(x)
    outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)
    return tf.keras.Model(inputs, outputs)
 
model2 = create_model_fraud(X2_train.shape[1])
model2.summary()
 
model2.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="binary_crossentropy",
    metrics=[
        tf.keras.metrics.AUC(curve="ROC", name="auc_roc"),
        tf.keras.metrics.AUC(curve="PR",  name="auc_pr"),
        tf.keras.metrics.Recall(name="recall"),
        tf.keras.metrics.Precision(name="precision"),
    ],
)
 
callbacks2 = [
    tf.keras.callbacks.EarlyStopping(
        monitor="val_auc_pr", mode="max", patience=15,
        restore_best_weights=True, verbose=1),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_auc_pr", mode="max", factor=0.5,
        patience=6, min_lr=1e-6, verbose=1),
]
 
history2 = model2.fit(
    X2_train, y2_train,
    validation_data=(X2_val, y2_val),
    epochs=300, batch_size=1024,
    class_weight=cw2, callbacks=callbacks2, verbose=1,
)
 
# Evaluación 
pred2 = model2.predict(X2_test).ravel()
auc_roc2 = roc_auc_score(y2_test, pred2)
auc_pr2  = average_precision_score(y2_test, pred2)
print(f"AUC-ROC: {auc_roc2:.4f} | AUC-PR: {auc_pr2:.4f}")
 
TARGET_RECALL2 = 0.80
best_t2, thresholds2, rec2, pre2 = find_best_threshold(pred2, y2_test, TARGET_RECALL2)
cm2, pf2, rf2 = evaluate_threshold(pred2, y2_test, best_t2)
tn2, fp2, fn2, tp2 = cm2.ravel()
print(f"Umbral: {best_t2:.2f} | Recall: {rf2:.4f} | Precision: {pf2:.4f} | FN: {fn2}")
print(classification_report(
    y2_test, (pred2 >= best_t2).astype(int),
    target_names=["Transaccion Legitima", "Fraude"]))
 
#  Gráficas
plot_training_curves(history2,
    "Curvas de Entrenamiento — Credit Card Fraud MLP",
    ["auc_roc", "auc_pr", "recall"],
    "training_curves_fraud.png")
 
plot_roc(y2_test, pred2, auc_roc2,
    "Curva ROC — Credit Card Fraud", "roc_curve_fraud.png")
 
plot_pr(y2_test, pred2, auc_pr2,
    "Curva Precision-Recall — Credit Card Fraud", "pr_curve_fraud.png",
    color="crimson")
 
plot_confusion(cm2, ["Legitima", "Fraude"], best_t2,
    "Matriz de Confusión — Credit Card Fraud", "confusion_matrix_fraud.png",
    cmap="Reds")
 
plot_threshold_analysis(thresholds2, rec2, pre2, best_t2, TARGET_RECALL2,
    "Precision y Recall vs Umbral — Credit Card Fraud",
    "threshold_fraud.png",
    recall_color="steelblue", precision_color="crimson")
 
 
##################################################################################
#                          PROBLEMA 3 — TITANIC SURVIVAL                         #
##################################################################################
 
print("\n" + "="*60)
print("  PROBLEMA 3 — TITANIC SURVIVAL")
print("="*60)
 

df3 = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "yasserh/titanic-dataset",
    "Titanic-Dataset.csv",
)
print(f"Shape: {df3.shape}")
print(df3["Survived"].value_counts())
 
# Preprocesamiento específico del Titanic
df3 = df3.drop(columns=["PassengerId", "Name", "Ticket", "Cabin"])
df3["Age"]      = df3["Age"].fillna(df3["Age"].median())
df3["Embarked"] = df3["Embarked"].fillna(df3["Embarked"].mode()[0])
df3 = pd.get_dummies(df3, columns=["Sex", "Embarked"], drop_first=True)
 
TARGET3 = "Survived"
X3 = df3.drop(columns=[TARGET3]).values.astype(np.float32)
y3 = df3[TARGET3].values.astype(np.int32)
print(f"Clase 0 (No sobrevivió): {np.sum(y3==0)} | Clase 1 (Sobrevivió): {np.sum(y3==1)}")
print(f"Features tras encoding: {X3.shape[1]}")
 
#  Preprocesamiento 
X3_train, X3_val, X3_test, y3_train, y3_val, y3_test = split_and_scale(X3, y3)
cw3 = get_class_weights(y3_train)
 
# Modelo 
def create_model_titanic(input_dim):
    inputs = tf.keras.Input(shape=(input_dim,))
    x = tf.keras.layers.Dense(64, activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(1e-4))(inputs)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.35)(x)
    x = tf.keras.layers.Dense(32, activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(1e-4))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.25)(x)
    x = tf.keras.layers.Dense(16, activation="relu",
        kernel_regularizer=tf.keras.regularizers.l2(1e-4))(x)
    x = tf.keras.layers.Dropout(0.20)(x)
    outputs = tf.keras.layers.Dense(1, activation="sigmoid")(x)
    return tf.keras.Model(inputs, outputs)
 
model3 = create_model_titanic(X3_train.shape[1])
model3.summary()
 
model3.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="binary_crossentropy",
    metrics=[
        tf.keras.metrics.AUC(curve="ROC", name="auc_roc"),
        tf.keras.metrics.AUC(curve="PR",  name="auc_pr"),
        tf.keras.metrics.Recall(name="recall"),
        tf.keras.metrics.Precision(name="precision"),
    ],
)
 
callbacks3 = [
    tf.keras.callbacks.EarlyStopping(
        monitor="val_auc_roc", mode="max", patience=30,
        restore_best_weights=True, verbose=1),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_auc_roc", mode="max", factor=0.5,
        patience=10, min_lr=1e-6, verbose=1),
]
 
history3 = model3.fit(
    X3_train, y3_train,
    validation_data=(X3_val, y3_val),
    epochs=300, batch_size=32,
    class_weight=cw3, callbacks=callbacks3, verbose=1,
)
 
#  Evaluacion 
pred3 = model3.predict(X3_test).ravel()
auc_roc3 = roc_auc_score(y3_test, pred3)
auc_pr3  = average_precision_score(y3_test, pred3)
print(f"AUC-ROC: {auc_roc3:.4f} | AUC-PR: {auc_pr3:.4f}")
 
TARGET_RECALL3 = 0.72
best_t3, thresholds3, rec3, pre3 = find_best_threshold(pred3, y3_test, TARGET_RECALL3)
cm3, pf3, rf3 = evaluate_threshold(pred3, y3_test, best_t3)
tn3, fp3, fn3, tp3 = cm3.ravel()
print(f"Umbral: {best_t3:.2f} | Recall: {rf3:.4f} | Precision: {pf3:.4f} | FN: {fn3}")
print(classification_report(
    y3_test, (pred3 >= best_t3).astype(int),
    target_names=["No sobrevivio", "Sobrevivio"]))
 
#  Gráficas 
plot_training_curves(history3,
    "Curvas de Entrenamiento — Titanic Survival MLP",
    ["auc_roc", "recall", "precision"],
    "training_curves_titanic.png")
 
plot_roc(y3_test, pred3, auc_roc3,
    "Curva ROC — Titanic Survival", "roc_curve_titanic.png")
 
plot_pr(y3_test, pred3, auc_pr3,
    "Curva Precision-Recall — Titanic Survival", "pr_curve_titanic.png",
    color="teal")
 
plot_confusion(cm3, ["No sobrevivio", "Sobrevivio"], best_t3,
    "Matriz de Confusión — Titanic Survival", "confusion_matrix_titanic.png")
 
plot_threshold_analysis(thresholds3, rec3, pre3, best_t3, TARGET_RECALL3,
    "Precision y Recall vs Umbral — Titanic Survival",
    "threshold_titanic.png",
    recall_color="steelblue", precision_color="teal")
 
print("\n✓ Los 3 problemas completados. Todas las gráficas guardadas.")