import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

import tensorflow as tf
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve, average_precision_score
from tensorflow.keras.utils import to_categorical

SEED = 42
np.random.seed(SEED)
tf.random.set_seed(SEED)


def load_iris():
    from sklearn.datasets import load_iris as _load
    data = _load()
    X = pd.DataFrame(data.data, columns=data.feature_names)
    y = data.target
    return X.values, y

def load_glass():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/glass/glass.data"
    cols = ['Id','RI','Na','Mg','Al','Si','K','Ca','Ba','Fe','Type']
    df = pd.read_csv(url, names=cols)
    df.drop('Id', axis=1, inplace=True)
    le = LabelEncoder()
    y = le.fit_transform(df['Type'])
    X = df.drop('Type', axis=1).values
    return X, y

def load_wine():
    from sklearn.datasets import load_wine as _load
    data = _load()
    X = data.data
    y = data.target
    return X, y

def preprocess(X, y, num_classes):
    X_train, X_tmp, y_train, y_tmp = train_test_split(
        X, y, test_size=0.30, stratify=y, random_state=SEED)
    X_val, X_test, y_val, y_test = train_test_split(
        X_tmp, y_tmp, test_size=0.50, stratify=y_tmp, random_state=SEED)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val   = scaler.transform(X_val)
    X_test  = scaler.transform(X_test)

    classes = np.unique(y_train)
    cw = compute_class_weight('balanced', classes=classes, y=y_train)
    class_weight_dict = dict(zip(range(len(classes)), cw))

    y_train_oh = to_categorical(y_train, num_classes)
    y_val_oh   = to_categorical(y_val,   num_classes)
    y_test_oh  = to_categorical(y_test,  num_classes)

    return (X_train, X_val, X_test,
            y_train, y_val, y_test,
            y_train_oh, y_val_oh, y_test_oh,
            class_weight_dict)


def create_model_1(input_dim, num_classes):
    inputs = tf.keras.Input(shape=(input_dim,))
    x = tf.keras.layers.Dense(16, activation='relu',
        kernel_regularizer=tf.keras.regularizers.l2(1e-4))(inputs)
    x = tf.keras.layers.Dropout(0.15)(x)
    x = tf.keras.layers.Dense(8, activation='relu',
        kernel_regularizer=tf.keras.regularizers.l2(1e-4))(x)
    x = tf.keras.layers.Dropout(0.10)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(x)
    return tf.keras.Model(inputs, outputs)

def create_model_2(input_dim, num_classes):
    inputs = tf.keras.Input(shape=(input_dim,))
    x = tf.keras.layers.Dense(64, activation='relu',
        kernel_regularizer=tf.keras.regularizers.l2(1e-4))(inputs)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.30)(x)
    x = tf.keras.layers.Dense(32, activation='relu',
        kernel_regularizer=tf.keras.regularizers.l2(1e-4))(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Dropout(0.20)(x)
    x = tf.keras.layers.Dense(16, activation='relu',
        kernel_regularizer=tf.keras.regularizers.l2(1e-4))(x)
    x = tf.keras.layers.Dropout(0.10)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(x)
    return tf.keras.Model(inputs, outputs)

def create_model_3(input_dim, num_classes):
    inputs = tf.keras.Input(shape=(input_dim,))
    x = tf.keras.layers.Dense(128, activation='tanh',
        kernel_regularizer=tf.keras.regularizers.l2(1e-4))(inputs)
    x = tf.keras.layers.Dropout(0.30)(x)
    x = tf.keras.layers.Dense(64, activation='relu',
        kernel_regularizer=tf.keras.regularizers.l2(1e-4))(x)
    x = tf.keras.layers.Dropout(0.20)(x)
    x = tf.keras.layers.Dense(32, activation='relu',
        kernel_regularizer=tf.keras.regularizers.l2(1e-4))(x)
    x = tf.keras.layers.Dropout(0.15)(x)
    x = tf.keras.layers.Dense(16, activation='relu',
        kernel_regularizer=tf.keras.regularizers.l2(1e-4))(x)
    x = tf.keras.layers.Dropout(0.10)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(x)
    return tf.keras.Model(inputs, outputs)

def train_model(model, X_train, y_train_oh, X_val, y_val_oh,
                class_weight_dict, batch_size, max_epochs, patience):
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=[
            tf.keras.metrics.CategoricalAccuracy(name='accuracy'),
            tf.keras.metrics.AUC(name='auc', multi_label=False)
        ]
    )
    es = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss', patience=patience, restore_best_weights=True)
    history = model.fit(
        X_train, y_train_oh,
        validation_data=(X_val, y_val_oh),
        epochs=max_epochs,
        batch_size=batch_size,
        class_weight=class_weight_dict,
        callbacks=[es],
        verbose=0
    )
    return history


def plot_training(history, model_name, color='steelblue'):
    """Figura 1 / 6 / 11 — Loss y Accuracy Train vs Validación"""
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle(f'Modelo {model_name}', fontsize=13)

    ax = axes[0]
    ax.plot(history.history['loss'],     color=color, label='Train')
    ax.plot(history.history['val_loss'], color=color, linestyle='--', label='Validacion')
    ax.set_title('Evolucion de la perdida')
    ax.set_xlabel('Epoca'); ax.set_ylabel('Loss')
    ax.legend(); ax.grid(True, alpha=0.3)

    ax = axes[1]
    ax.plot(history.history['accuracy'],     color=color, label='Train')
    ax.plot(history.history['val_accuracy'], color=color, linestyle='--', label='Validacion')
    ax.set_title('Evolucion de la exactitud')
    ax.set_xlabel('Epoca'); ax.set_ylabel('Accuracy')
    ax.legend(); ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_confusion_matrix(y_true, y_pred_classes, class_names, model_name, cmap):
    """Figura 2 / 7 / 12 — Matriz de Confusión"""
    cm = confusion_matrix(y_true, y_pred_classes)
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, cmap=cmap)
    plt.colorbar(im, ax=ax)
    ax.set_xticks(range(len(class_names))); ax.set_xticklabels(class_names, rotation=30, ha='right')
    ax.set_yticks(range(len(class_names))); ax.set_yticklabels(class_names)
    ax.set_xlabel('Clase Predicha'); ax.set_ylabel('Clase Real')
    ax.set_title(f'Matriz de Confusion — Modelo {model_name}')
    for i in range(len(class_names)):
        for j in range(len(class_names)):
            ax.text(j, i, str(cm[i, j]), ha='center', va='center',
                    color='white' if cm[i, j] > cm.max()/2 else 'black', fontsize=12)
    plt.tight_layout()
    return fig


def plot_roc_curves(y_true_oh, y_proba, class_names, model_name, colors):
    """Figura 3 / 8 / 13 — Curvas ROC OvR"""
    n_classes = len(class_names)
    fpr, tpr, roc_auc = {}, {}, {}
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_true_oh[:, i], y_proba[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
    macro_auc = np.mean(list(roc_auc.values()))

    fig, ax = plt.subplots(figsize=(7, 5))
    for i, name in enumerate(class_names):
        ax.plot(fpr[i], tpr[i], color=colors[i],
                label=f'{name} (AUC={roc_auc[i]:.3f})')
    ax.plot([0,1],[0,1],'k--', label='Aleatorio')
    ax.set_xlabel('Tasa de Falsos Positivos (FPR)')
    ax.set_ylabel('Tasa de Verdaderos Positivos (TPR)')
    ax.set_title(f'Modelo {model_name}\nAUC-macro={macro_auc:.3f}')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def plot_pr_curves(y_true_oh, y_proba, class_names, model_name, colors):
    """Figura 4 / 9 / 14 — Curvas Precision-Recall"""
    n_classes = len(class_names)
    ap_scores = []
    fig, ax = plt.subplots(figsize=(7, 5))
    for i, name in enumerate(class_names):
        prec, rec, _ = precision_recall_curve(y_true_oh[:, i], y_proba[:, i])
        ap = average_precision_score(y_true_oh[:, i], y_proba[:, i])
        ap_scores.append(ap)
        ax.plot(rec, prec, color=colors[i], label=f'{name} (AP={ap:.3f})')
    macro_ap = np.mean(ap_scores)
    ax.set_xlabel('Recall'); ax.set_ylabel('Precision')
    ax.set_title(f'Modelo {model_name}\nAUC-PR macro={macro_ap:.3f}')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def plot_threshold_coverage(y_true, y_proba, model_name, color):
    """Figura 5 / 10 / 15 — Accuracy vs Cobertura según Umbral de Confianza"""
    thresholds = np.linspace(0, 1, 200)
    accs, coverages = [], []
    max_conf = y_proba.max(axis=1)
    y_pred   = y_proba.argmax(axis=1)

    for t in thresholds:
        mask = max_conf >= t
        cov  = mask.mean() * 100
        acc  = (y_pred[mask] == y_true[mask]).mean() if mask.sum() > 0 else np.nan
        accs.append(acc); coverages.append(cov)

    fig, ax1 = plt.subplots(figsize=(8, 4))
    ax2 = ax1.twinx()
    ax1.plot(thresholds, accs,      color=color,  marker='>', markersize=2, label='Accuracy')
    ax2.plot(thresholds, coverages, color='red',  marker='s', markersize=2,
             linestyle='--', label='Cobertura (%)')
    ax1.set_xlabel('Umbral de confianza minima')
    ax1.set_ylabel('Accuracy',       color=color)
    ax2.set_ylabel('Cobertura (%)',   color='red')
    ax1.tick_params(axis='y', labelcolor=color)
    ax2.tick_params(axis='y', labelcolor='red')
    ax1.set_title(f'Modelo {model_name}: Accuracy vs Cobertura segun Umbral de Confianza')
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='center right', fontsize=8)
    ax1.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def run_model(name, X, y, num_classes, class_names,
              model_fn, batch_size, max_epochs, patience,
              train_color, cm_cmap, roc_colors, label):

    (X_train, X_val, X_test,
     y_train, y_val, y_test,
     y_train_oh, y_val_oh, y_test_oh,
     cw_dict) = preprocess(X, y, num_classes)

    model = model_fn(X_train.shape[1], num_classes)
    history = train_model(model, X_train, y_train_oh, X_val, y_val_oh,
                          cw_dict, batch_size, max_epochs, patience)

    y_proba = model.predict(X_test, verbose=0)
    y_pred  = y_proba.argmax(axis=1)

    acc = (y_pred == y_test).mean()
    print(f"\n=== {name} | Test Accuracy: {acc:.4f} | Épocas: {len(history.history['loss'])} ===")

    figs = {
        'training':   plot_training(history, label, train_color),
        'cm':         plot_confusion_matrix(y_test, y_pred, class_names, label, cm_cmap),
        'roc':        plot_roc_curves(y_test_oh, y_proba, class_names, label, roc_colors),
        'pr':         plot_pr_curves(y_test_oh, y_proba, class_names, label, roc_colors),
        'threshold':  plot_threshold_coverage(y_test, y_proba, label, train_color),
    }
    return figs



if __name__ == '__main__':

    X1, y1 = load_iris()
    figs1 = run_model(
        name='Iris',
        X=X1, y=y1, num_classes=3,
        class_names=['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'],
        model_fn=create_model_1,
        batch_size=16, max_epochs=300, patience=30,
        train_color='steelblue',
        cm_cmap='Blues',
        roc_colors=['#1f77b4', '#9467bd', '#bcbd22'],
        label='1 — Iris'
    )

    X2, y2 = load_glass()
    figs2 = run_model(
        name='Glass',
        X=X2, y=y2, num_classes=6,
        class_names=['BW-Float','BW-Non-F','VW-Float','Containers','Tableware','Headlamps'],
        model_fn=create_model_2,
        batch_size=16, max_epochs=300, patience=25,
        train_color='darkorange',
        cm_cmap='Oranges',
        roc_colors=['#1f77b4','#ff7f0e','#d62728','#9467bd','#bcbd22','#8c564b'],
        label='2 — Glass Identification'
    )

    X3, y3 = load_wine()
    figs3 = run_model(
        name='Wine',
        X=X3, y=y3, num_classes=3,
        class_names=['class_1', 'class_2', 'class_3'],
        model_fn=create_model_3,
        batch_size=16, max_epochs=300, patience=30,
        train_color='seagreen',
        cm_cmap='Greens',
        roc_colors=['#1f77b4', '#9467bd', '#bcbd22'],
        label='3 — Wine UCI'
    )

    for model_id, figs in [('M1_Iris', figs1), ('M2_Glass', figs2), ('M3_Wine', figs3)]:
        for fig_name, fig in figs.items():
            fname = f'{model_id}_{fig_name}.png'
            fig.savefig(fname, dpi=150, bbox_inches='tight')
            plt.close(fig)
            print(f'Guardado: {fname}')

    print('\n✓ Todas las gráficas generadas correctamente.')