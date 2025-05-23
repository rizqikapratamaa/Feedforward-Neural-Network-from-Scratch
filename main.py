from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.datasets import fetch_openml
import numpy as np
from FFNN import FFNN
from Plotter import Plotter


def preprocess_mnist(num_samples=20000):
    mnist = fetch_openml('mnist_784', version=1, as_frame=False)
    X = mnist.data
    y = mnist.target.astype(np.int32)
    
    np.random.seed(42)
    indices = np.random.choice(len(X), num_samples, replace=False)
    X = X[indices]
    y = y[indices]
    
    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)
    
    y_one_hot = np.zeros((len(y), 10))
    y_one_hot[np.arange(len(y)), y] = 1
    
    X_train, X_temp, y_train, y_temp = train_test_split(X, y_one_hot, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
    
    return X_train, X_val, X_test, y_train, y_val, y_test

def preprocess_iris():
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    
    scaler = MinMaxScaler()
    X = scaler.fit_transform(X)
    
    y_one_hot = [[1 if i == label else 0 for i in range(3)] for label in y]
    
    # 70% training - 15% validation - 15% testing
    X_train, X_temp, y_train, y_temp = train_test_split(X, y_one_hot, test_size=0.3, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
    
    return X_train, X_val, X_test, y_train, y_val, y_test

if __name__ == "__main__":
    X_train, X_val, X_test, y_train, y_val, y_test = preprocess_mnist(num_samples=10000)
    
    ffnn = FFNN(
        input_size=784,
        hidden_sizes=[256, 128],
        output_size=10,
        learning_rate=0.001,
        hidden_activations=['relu', 'relu'],
        output_activation='softmax',
        loss_function='cce',
        reg_type='l2',
        reg_lambda=0.001,
        rms_norm=True,
        rms_prop=False,
        init_type='xavier',
        seed=69420
    )
    ffnn.train(X_train, y_train, X_val, y_val, epochs=20, batch_size=32, verbose=1)
    
    correct = 0
    for inputs, target in zip(X_test, y_test):
        prediction = ffnn.predict(inputs)
        predicted_class = np.argmax(prediction)
        actual_class = np.argmax(target)
        if predicted_class == actual_class:
            correct += 1
    
    print(f"Accuracy: {correct / len(y_test) * 100:.2f}%")

    plotter = Plotter()
    plotter.visualize_network(ffnn)