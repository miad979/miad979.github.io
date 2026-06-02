**Import Libraries**

Before building an ANN model, we need:

Visualization -- matplotlib, seaborn

Deep Learning -- TensorFlow/Keras

Preprocessing & evaluation -- scikit-learn

These libraries help in:

Preparing data

Building model

Evaluating performance
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix, mean_squared_error

import warnings
warnings.filterwarnings('ignore')
```

**PART 1: Load Dataset**

We load the Iris dataset which contains:

150 samples
4 input features
3 output classes

This dataset is ideal because:

Small and clean
Perfect for ANN demonstration
```python
iris = load_iris()

X = pd.DataFrame(iris.data, columns=iris.feature_names)
y = pd.Series(iris.target)

target_names = iris.target_names

print(X.shape, y.shape)
print(X.head())
```

```text
(150, 4) (150,)
   sepal length (cm)  sepal width (cm)  petal length (cm)  petal width (cm)
0                5.1               3.5                1.4               0.2
1                4.9               3.0                1.4               0.2
2                4.7               3.2                1.3               0.2
3                4.6               3.1                1.5               0.2
4                5.0               3.6                1.4               0.2
```

**PART 2: Encoding Target**

Neural networks require numerical input:

Labels must be encoded

Steps:

Label Encoding  -- convert labels to numbers

One-hot Encoding   -- required for multi-class classification
```python
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

num_classes = len(np.unique(y_encoded))
y_one_hot = to_categorical(y_encoded)
```

**PART 3: Train-Test Split**

We split data into:

Training set (80%) -- learn patterns

Testing set (20%) -- evaluate performance

Stratified sampling ensures:

Equal class distribution
```python
X_train, X_test, y_train_oh, y_test_oh = train_test_split(
    X, y_one_hot, test_size=0.2, random_state=42, stratify=y_encoded)

_, _, _, y_test_original = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)
```

**PART 4: Feature Scaling**

ANN is sensitive to feature scale.

Why scaling is important:

Faster convergence

Prevents dominance of large values

Improves accuracy

We use **StandardScaler**:

Mean = 0

Std = 1
```python
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

**PART 5: Build ANN Model (Classification)**

**Model structure:**

Input layer -- 4 neurons

Hidden layer -- learns patterns

Output layer -- 3 classes

Activation:

ReLU -- hidden layer

Softmax -- output layer
```python
model = keras.Sequential([
    keras.Input(shape=(4,)),
    layers.Dense(10, activation='relu'),
    layers.Dense(3, activation='softmax')
])
```

**PART 6: Compile Model**

We define:

Optimizer -- Adam (fast & efficient)

Loss -- categorical_crossentropy

Metric -- accuracy
```python
model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])
```

**PART 7: Train Model**

**Training process:**

Epochs -- number of learning cycles

Batch size -- samples per update

Validation -- check overfitting
```python
history = model.fit(X_train_scaled, y_train_oh,
                    epochs=50,
                    batch_size=8,
                    validation_split=0.1)
```

```text
Epoch 1/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m4s[0m 101ms/step - accuracy: 0.6204 - loss: 1.0383 - val_accuracy: 0.9167 - val_loss: 0.7761
Epoch 2/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 30ms/step - accuracy: 0.6296 - loss: 0.9892 - val_accuracy: 0.9167 - val_loss: 0.7502
Epoch 3/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m1s[0m 28ms/step - accuracy: 0.6296 - loss: 0.9434 - val_accuracy: 0.9167 - val_loss: 0.7229
Epoch 4/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m1s[0m 36ms/step - accuracy: 0.6204 - loss: 0.9042 - val_accuracy: 0.9167 - val_loss: 0.6968
Epoch 5/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 25ms/step - accuracy: 0.6204 - loss: 0.8644 - val_accuracy: 0.9167 - val_loss: 0.6678
Epoch 6/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m1s[0m 32ms/step - accuracy: 0.6204 - loss: 0.8285 - val_accuracy: 0.8333 - val_loss: 0.6388
Epoch 7/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m1s[0m 49ms/step - accuracy: 0.6204 - loss: 0.7936 - val_accuracy: 0.8333 - val_loss: 0.6130
Epoch 8/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 16ms/step - accuracy: 0.6111 - loss: 0.7611 - val_accuracy: 0.7500 - val_loss: 0.5876
Epoch 9/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 13ms/step - accuracy: 0.6296 - loss: 0.7300 - val_accuracy: 0.8333 - val_loss: 0.5669
Epoch 10/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 17ms/step - accuracy: 0.6944 - loss: 0.6994 - val_accuracy: 0.8333 - val_loss: 0.5466
Epoch 11/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 21ms/step - accuracy: 0.7407 - loss: 0.6705 - val_accuracy: 0.8333 - val_loss: 0.5285
Epoch 12/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 16ms/step - accuracy: 0.7407 - loss: 0.6434 - val_accuracy: 0.8333 - val_loss: 0.5127
Epoch 13/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 13ms/step - accuracy: 0.7685 - loss: 0.6163 - val_accuracy: 0.8333 - val_loss: 0.4969
Epoch 14/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 18ms/step - accuracy: 0.7963 - loss: 0.5922 - val_accuracy: 0.8333 - val_loss: 0.4855
Epoch 15/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 17ms/step - accuracy: 0.8148 - loss: 0.5688 - val_accuracy: 0.8333 - val_loss: 0.4758
Epoch 16/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 14ms/step - accuracy: 0.8148 - loss: 0.5464 - val_accuracy: 0.8333 - val_loss: 0.4661
Epoch 17/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 14ms/step - accuracy: 0.8333 - loss: 0.5260 - val_accuracy: 0.7500 - val_loss: 0.4564
Epoch 18/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 16ms/step - accuracy: 0.8333 - loss: 0.5070 - val_accuracy: 0.7500 - val_loss: 0.4498
Epoch 19/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 12ms/step - accuracy: 0.8241 - loss: 0.4893 - val_accuracy: 0.6667 - val_loss: 0.4437
Epoch 20/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 16ms/step - accuracy: 0.8333 - loss: 0.4711 - val_accuracy: 0.6667 - val_loss: 0.4344
Epoch 21/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 22ms/step - accuracy: 0.8426 - loss: 0.4557 - val_accuracy: 0.6667 - val_loss: 0.4272
Epoch 22/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m1s[0m 23ms/step - accuracy: 0.8241 - loss: 0.4419 - val_accuracy: 0.6667 - val_loss: 0.4257
Epoch 23/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 13ms/step - accuracy: 0.8241 - loss: 0.4271 - val_accuracy: 0.6667 - val_loss: 0.4201
Epoch 24/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 16ms/step - accuracy: 0.8241 - loss: 0.4149 - val_accuracy: 0.6667 - val_loss: 0.4132
Epoch 25/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 19ms/step - accuracy: 0.8333 - loss: 0.4034 - val_accuracy: 0.6667 - val_loss: 0.4087
Epoch 26/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 7ms/step - accuracy: 0.8333 - loss: 0.3928 - val_accuracy: 0.6667 - val_loss: 0.4031
Epoch 27/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 7ms/step - accuracy: 0.8426 - loss: 0.3825 - val_accuracy: 0.6667 - val_loss: 0.3975
Epoch 28/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 6ms/step - accuracy: 0.8611 - loss: 0.3729 - val_accuracy: 0.6667 - val_loss: 0.3929
Epoch 29/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 6ms/step - accuracy: 0.8796 - loss: 0.3643 - val_accuracy: 0.6667 - val_loss: 0.3865
Epoch 30/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 6ms/step - accuracy: 0.8889 - loss: 0.3560 - val_accuracy: 0.6667 - val_loss: 0.3864
Epoch 31/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 6ms/step - accuracy: 0.8889 - loss: 0.3476 - val_accuracy: 0.6667 - val_loss: 0.3811
Epoch 32/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 6ms/step - accuracy: 0.8889 - loss: 0.3403 - val_accuracy: 0.7500 - val_loss: 0.3764
Epoch 33/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 7ms/step - accuracy: 0.8889 - loss: 0.3333 - val_accuracy: 0.7500 - val_loss: 0.3711
Epoch 34/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 6ms/step - accuracy: 0.8889 - loss: 0.3265 - val_accuracy: 0.7500 - val_loss: 0.3668
Epoch 35/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 6ms/step - accuracy: 0.8889 - loss: 0.3198 - val_accuracy: 0.7500 - val_loss: 0.3609
Epoch 36/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 6ms/step - accuracy: 0.8889 - loss: 0.3135 - val_accuracy: 0.7500 - val_loss: 0.3554
Epoch 37/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 6ms/step - accuracy: 0.8889 - loss: 0.3075 - val_accuracy: 0.7500 - val_loss: 0.3481
Epoch 38/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 6ms/step - accuracy: 0.8981 - loss: 0.3008 - val_accuracy: 0.7500 - val_loss: 0.3424
Epoch 39/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 6ms/step - accuracy: 0.8981 - loss: 0.2952 - val_accuracy: 0.7500 - val_loss: 0.3387
Epoch 40/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 6ms/step - accuracy: 0.8981 - loss: 0.2891 - val_accuracy: 0.7500 - val_loss: 0.3319
Epoch 41/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 7ms/step - accuracy: 0.8981 - loss: 0.2838 - val_accuracy: 0.7500 - val_loss: 0.3266
Epoch 42/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 6ms/step - accuracy: 0.8981 - loss: 0.2787 - val_accuracy: 0.7500 - val_loss: 0.3195
Epoch 43/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 7ms/step - accuracy: 0.9074 - loss: 0.2736 - val_accuracy: 0.7500 - val_loss: 0.3154
Epoch 44/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 10ms/step - accuracy: 0.9074 - loss: 0.2688 - val_accuracy: 0.7500 - val_loss: 0.3118
Epoch 45/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 12ms/step - accuracy: 0.9074 - loss: 0.2641 - val_accuracy: 0.8333 - val_loss: 0.3035
Epoch 46/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 9ms/step - accuracy: 0.9074 - loss: 0.2593 - val_accuracy: 0.8333 - val_loss: 0.2986
Epoch 47/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 9ms/step - accuracy: 0.9074 - loss: 0.2545 - val_accuracy: 0.8333 - val_loss: 0.2947
Epoch 48/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 11ms/step - accuracy: 0.9074 - loss: 0.2505 - val_accuracy: 0.8333 - val_loss: 0.2873
Epoch 49/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 9ms/step - accuracy: 0.9074 - loss: 0.2463 - val_accuracy: 0.8333 - val_loss: 0.2847
Epoch 50/50
[1m14/14[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 11ms/step - accuracy: 0.9167 - loss: 0.2420 - val_accuracy: 0.8333 - val_loss: 0.2787
```

**PART 8: Training Visualization**


Graphs help us understand:

**Learning progress**

**Overfitting**

Good model:

Training & validation curves close
```python
plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title("Accuracy")

plt.subplot(1,2,2)
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title("Loss")

plt.show()
```

![output image 17-0](images/cell-17-0.png)

**PART 9: Model Evaluation**

We evaluate using:

Accuracy -- overall correctness

Precision -- correctness of prediction

Recall -- detection ability

F1-score -- balance
```python
y_pred_proba = model.predict(X_test_scaled)
y_pred = np.argmax(y_pred_proba, axis=1)

print("Accuracy:", accuracy_score(y_test_original, y_pred))
print("Precision:", precision_score(y_test_original, y_pred, average='macro'))
print("Recall:", recall_score(y_test_original, y_pred, average='macro'))
print("F1:", f1_score(y_test_original, y_pred, average='macro'))

print(classification_report(y_test_original, y_pred, target_names=target_names))
```

```text
[1m1/1[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 93ms/step
Accuracy: 0.8666666666666667
Precision: 0.9047619047619048
Recall: 0.8666666666666667
F1: 0.8611111111111112
              precision    recall  f1-score   support

      setosa       1.00      1.00      1.00        10
  versicolor       1.00      0.60      0.75        10
   virginica       0.71      1.00      0.83        10

    accuracy                           0.87        30
   macro avg       0.90      0.87      0.86        30
weighted avg       0.90      0.87      0.86        30

```

**PART 10: Confusion Matrix**

Shows:

**Correct vs incorrect predictions**

**Class-wise performance**

Ideal:

Only diagonal values
```python
cm = confusion_matrix(y_test_original, y_pred)

sns.heatmap(cm, annot=True, fmt='d',
            xticklabels=target_names,
            yticklabels=target_names)

plt.title("Confusion Matrix")
plt.show()
```

![output image 21-0](images/cell-21-0.png)

**PART 11: Deep Model + Early Stopping**

**Why deeper model?**

Learn complex patterns

**Why EarlyStopping?**

Prevent overfitting

Stop when validation loss increases
```python
model_deep = keras.Sequential([
    keras.Input(shape=(4,)),
    layers.Dense(64, activation='relu'),
    layers.Dense(32, activation='relu'),
    layers.Dense(3, activation='softmax')
])

model_deep.compile(optimizer='adam',
                   loss='categorical_crossentropy',
                   metrics=['accuracy'])

early = EarlyStopping(monitor='val_loss',
                      patience=10,
                      restore_best_weights=True)

history_deep = model_deep.fit(X_train_scaled, y_train_oh,
                             epochs=100,
                             batch_size=8,
                             validation_split=0.1,
                             callbacks=[early],
                             verbose=0)
```

**PART 12: Dropout Model**

**Dropout:**

Randomly removes neurons

Prevents overfitting

Improves generalization
```python
model_dropout = keras.Sequential([
    keras.Input(shape=(4,)),
    layers.Dense(64, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(32, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(3, activation='softmax')
])
```

**PART 13: ANN for Regression**

Here ANN predicts continuous values.

Changes:

Output layer -- 1 neuron

Activation -- linear

Loss -- MSE
```python
X_reg = iris.data[:, :3]
y_reg = iris.data[:, 3]

X_train, X_test, y_train, y_test = train_test_split(X_reg, y_reg, test_size=0.2)

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model_reg = keras.Sequential([
    keras.Input(shape=(3,)),
    layers.Dense(10, activation='relu'),
    layers.Dense(8, activation='relu'),
    layers.Dense(1, activation='linear')
])

model_reg.compile(optimizer='adam', loss='mse')

model_reg.fit(X_train, y_train, epochs=50)

y_pred = model_reg.predict(X_test)

print("MSE:", mean_squared_error(y_test, y_pred))
```

```text
Epoch 1/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m1s[0m 12ms/step - loss: 2.1700
Epoch 2/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 13ms/step - loss: 2.0769
Epoch 3/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 12ms/step - loss: 1.9841
Epoch 4/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 12ms/step - loss: 1.8991
Epoch 5/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 12ms/step - loss: 1.8141
Epoch 6/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 12ms/step - loss: 1.7324 
Epoch 7/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 14ms/step - loss: 1.6579
Epoch 8/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 12ms/step - loss: 1.5716
Epoch 9/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 13ms/step - loss: 1.4977
Epoch 10/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 13ms/step - loss: 1.4250 
Epoch 11/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 16ms/step - loss: 1.3477
Epoch 12/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 15ms/step - loss: 1.2760
Epoch 13/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 13ms/step - loss: 1.2009
Epoch 14/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 12ms/step - loss: 1.1316
Epoch 15/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 13ms/step - loss: 1.0629
Epoch 16/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 10ms/step - loss: 0.9920 
Epoch 17/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 9ms/step - loss: 0.9298 
Epoch 18/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 8ms/step - loss: 0.8621 
Epoch 19/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 8ms/step - loss: 0.7991 
Epoch 20/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 8ms/step - loss: 0.7400 
Epoch 21/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 9ms/step - loss: 0.6812 
Epoch 22/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 8ms/step - loss: 0.6242 
Epoch 23/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 8ms/step - loss: 0.5728 
Epoch 24/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 9ms/step - loss: 0.5216 
Epoch 25/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 8ms/step - loss: 0.4729 
Epoch 26/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 9ms/step - loss: 0.4295 
Epoch 27/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 8ms/step - loss: 0.3875 
Epoch 28/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 9ms/step - loss: 0.3497 
Epoch 29/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 8ms/step - loss: 0.3142 
Epoch 30/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 9ms/step - loss: 0.2839 
Epoch 31/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 9ms/step - loss: 0.2539 
Epoch 32/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 9ms/step - loss: 0.2307 
Epoch 33/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 8ms/step - loss: 0.2091 
Epoch 34/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 8ms/step - loss: 0.1908 
Epoch 35/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 8ms/step - loss: 0.1758 
Epoch 36/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 10ms/step - loss: 0.1637
Epoch 37/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 9ms/step - loss: 0.1535 
Epoch 38/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 9ms/step - loss: 0.1447 
Epoch 39/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 8ms/step - loss: 0.1383 
Epoch 40/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 8ms/step - loss: 0.1323 
Epoch 41/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 11ms/step - loss: 0.1269
Epoch 42/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 9ms/step - loss: 0.1230 
Epoch 43/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 9ms/step - loss: 0.1192 
Epoch 44/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 8ms/step - loss: 0.1160 
Epoch 45/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 13ms/step - loss: 0.1128
Epoch 46/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 9ms/step - loss: 0.1095 
Epoch 47/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 9ms/step - loss: 0.1070 
Epoch 48/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 9ms/step - loss: 0.1042 
Epoch 49/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 8ms/step - loss: 0.1016 
Epoch 50/50
[1m4/4[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 8ms/step - loss: 0.0993 
[1m1/1[0m [32m━━━━━━━━━━━━━━━━━━━━[0m[37m[0m [1m0s[0m 64ms/step
MSE: 0.14538836986629697
```

```python
import matplotlib.pyplot as plt

plt.scatter(y_test, y_pred)
plt.xlabel("Actual Values")
plt.ylabel("Predicted Values")
plt.title("Actual vs Predicted (ANN Regression - Iris)")
plt.show()
```

![output image 28-0](images/cell-28-0.png)

```python
from sklearn.metrics import r2_score

r2 = r2_score(y_test, y_pred)
print("R2 Score:", r2)
```

```text
R2 Score: 0.7622689760729869
```

