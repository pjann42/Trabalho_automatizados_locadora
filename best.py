import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(100)

losses = []
weights = []
biases = []

learning_rate = 0.001
epochs = 5000

# Função sigmoide
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Derivada da função sigmoide
def sigmoid_derivative(x):
    return x * (1 - x)

# Normaliza os dados
def normalize(X):
    return (X - np.min(X, axis=0)) / (np.max(X, axis=0) - np.min(X, axis=0))

# Inicializa os pesos de forma aleatória
def initialize_weights(input_size, output_size):
    limit = np.sqrt(6 / (input_size + output_size))
    return np.random.uniform(-limit, limit, (input_size, output_size))

# Cálculo da perda usando entropia cruzada
def cross_entropy(y_true, y_pred):
    return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred ))

# Carrega os dados
#data = pd.read_csv('classification2.csv', header=None)
data = pd.read_csv('diabetes.csv', header=None)

# Separando dados de entrada (X) e rótulos (y)
X = data.iloc[:, :-1].values  # Todas as colunas menos a última
y = data.iloc[:, -1].values.reshape(-1, 1)  # A última coluna como rótulos

# Normalizando dados de entrada
X = normalize(X)

# Dividindo os dados em treino e validação
train_size = int(0.8 * X.shape[0])
indices = np.random.permutation(X.shape[0])

X_train = X[indices[:train_size]]
y_train = y[indices[:train_size]]
X_val = X[indices[train_size:]]
y_val = y[indices[train_size:]]

# Inicializando pesos e biases
sz = [X_train.shape[1], 3 , 1]  

for i in range(len(sz) - 1):
    weights.append(initialize_weights(sz[i], sz[i + 1]))
    biases.append(np.zeros((1, sz[i + 1])))

# Treinamento da rede neural
print(weights)

for epoch in range(epochs):

    # Passo 1: Forward pass
    activations = [X_train]  # Começa com os dados de entrada

    for i in range(len(weights)):

        # 1. Calcula a combinação linear (z) para a camada atual
        # O que estamos fazendo aqui é pegar as ativações da camada anterior (ou seja, a entrada) e multiplicá-las pelos pesos da camada atual.

        # Depois, adicionamos os bias.
        z = np.dot(activations[i], weights[i]) + biases[i]
        
        # 2. Aplica a função de ativação (sigmoide) na combinação linear
        # A função sigmoide transforma a combinação linear em uma ativação entre 0 e 1.
        activation = sigmoid(z)
        
        # 3. Armazena a ativação da camada atual para uso posterior
        activations.append(activation) 
    

    # Passo 2: Cálculo do erro
    error = y_train - activations[-1]  # Erro entre rótulos verdadeiros e previsões


    # Passo 3: Cálculo da perda
    loss = cross_entropy(y_train, activations[-1])
    
    losses.append(loss)

    # Passo 4: Backpropagation
    deltas = []  # Lista para armazenar os deltas

    # Delta da camada de saída
    delta_output = error * sigmoid_derivative(activations[-1])  # Cálculo do delta da saída
    deltas.append(delta_output)

    # Cálculo do delta da camada oculta
    for i in reversed(range(len(weights) - 1)):

        # 1. Pegamos o delta da camada seguinte
        delta_proxima = deltas[-1]  # Dimensão: (n_samples, n_neurons_proxima)

        # 2. Calculamos a combinação linear do delta com os pesos transpostos da próxima camada
        # Transpomos a matriz de pesos da próxima camada (dimensão: n_neurons_atual × n_neurons_proxima)
        # e multiplicamos pelo delta da camada seguinte.
        gradiente = delta_proxima.dot(weights[i + 1].T)  # Dimensão: (n_samples, n_neurons_atual)
        
        # 3. Calculamos o delta da camada oculta multiplicando pelo derivada da função sigmoide
        # Multiplicamos o gradiente pela derivada da função sigmoide das ativações da camada atual.
        delta_oculta = gradiente * sigmoid_derivative(activations[i + 1])  # Dimensão: (n_samples, n_neurons_atual)

        # 4. Armazenamos o delta da camada oculta na lista de deltas
        deltas.append(delta_oculta)

    # Inverte a lista de deltas para a ordem correta
    deltas.reverse()

    df_deltas = []

    # for idx, delta in enumerate(deltas):
    #     df_delta = pd.DataFrame(delta)
    #     df_delta.columns = [f'Delta_Camada_{idx}_Neuron_{i}' for i in range(delta.shape[1])]  # Nomeia as colunas
    #     df_deltas.append(df_delta)  # Armazena no array para visualização posterior

    # # Exibe os DataFrames (deltas) de cada camada
    # for idx, df_delta in enumerate(df_deltas):
    #     print(f'Delta da Camada {idx}:')
    #     print(df_delta)
    #     print('-----------------------')

    # Atualização dos pesos e biases
    for i in range(len(weights)):
        # 1. Obtém as ativações da camada anterior
        ativacoes_anterior = activations[i]  # Dimensão: (n_samples, n_neurons_anterior)
        
        # 2. Obtém os deltas (gradientes de erro) da camada atual
        deltas_atual = deltas[i]  # Dimensão: (n_samples, n_neurons_atual)
        
        # 3. Transpõe a matriz de ativações da camada anterior
        ativacoes_anterior_T = ativacoes_anterior.T  # Dimensão: (n_neurons_anterior, n_samples)
        
        # 4. Calcula o gradiente dos pesos
        # Cada elemento do resultado representa a soma ponderada dos gradientes de erro (deltas)
        # multiplicados pelas ativações da camada anterior.
        gradiente_pesos = np.dot(ativacoes_anterior_T, deltas_atual)  # Dimensão: (n_neurons_anterior, n_neurons_atual)
        
        # 5. Atualiza os pesos com o gradiente multiplicado pela taxa de aprendizado
        weights[i] += gradiente_pesos * learning_rate

        # 6. Calcula a atualização dos biases (somando os deltas da camada atual ao longo de todos os samples)
        bias_atualizacao = np.sum(deltas_atual, axis=0, keepdims=True)
        
        # 7. Atualiza os biases com a soma dos deltas multiplicada pela taxa de aprendizado
        biases[i] += bias_atualizacao * learning_rate

    if epoch % 1000 == 0:
        print(f"Perda na época {epoch}: {loss}")

# Função para prever novos dados e retornar probabilidades
def predict(X_new):
    activation = X_new
    for i in range(len(weights)):
        z = np.dot(activation, weights[i]) + biases[i]
        activation = sigmoid(z)
    return activation  # Retorna as probabilidades


# Teste com os dados de validação
probabilities = predict(X_val)
predictions = (probabilities > 0.5).astype(int)

# Criando uma lista de tuplas com (probabilidade, previsão)
resultados = list(zip(probabilities.flatten(), predictions.flatten()))

# Cálculo da matriz de confusão
TP = np.sum((predictions.flatten() == 1) & (y_val.flatten() == 1))
TN = np.sum((predictions.flatten() == 0) & (y_val.flatten() == 0))
FP = np.sum((predictions.flatten() == 1) & (y_val.flatten() == 0))
FN = np.sum((predictions.flatten() == 0) & (y_val.flatten() == 1))

# Cálculo das métricas
accuracy = (TP + TN) / (TP + TN + FP + FN)
precision = TP / (TP + FP) if (TP + FP) > 0 else 0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0
f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

# Exibindo previsões e valores reais em três listas separadas
probabilidades = [f"{prob:.3f}" for prob, _ in resultados]
predicoes = [pred for _, pred in resultados]
valores_verdadeiros = y_val.flatten()

# Imprimindo as listas
print("Probabilidades (3 casas decimais):")
print(probabilidades)

print("Valores Preditos:")
print(np.array(predicoes))

print("Valores Verdadeiros:")
print(valores_verdadeiros)

# def plot_decision_boundary(X, y):
#     x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
#     y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
#     xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01),
#                          np.arange(y_min, y_max, 0.01))

#     Z = predict(np.c_[xx.ravel(), yy.ravel()])
#     Z = (Z > 0.5).astype(int).reshape(xx.shape)

#     plt.contourf(xx, yy, Z, alpha=0.8)
#     plt.scatter(X[:, 0], X[:, 1], c=y.flatten(), edgecolors='k', marker='o')
#     plt.xlabel('Feature 1')
#     plt.ylabel('Feature 2')
#     plt.title('Fronteira de Decisão da Rede Neural')
#     plt.show()

# def plot_predictions(X, y, predictions):
#     x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
#     y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
#     xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01),
#                          np.arange(y_min, y_max, 0.01))

#     Z = predict(np.c_[xx.ravel(), yy.ravel()])
#     Z = (Z > 0.5).astype(int).reshape(xx.shape)

#     plt.contourf(xx, yy, Z, alpha=0.8, cmap='coolwarm')
#     plt.scatter(X[:, 0], X[:, 1], c=predictions.flatten(), edgecolors='k', marker='o')
#     plt.xlabel('Feature 1')
#     plt.ylabel('Feature 2')
#     plt.title('Previsões da Rede Neural com Fronteira de Decisão')
#     plt.show()

def plot_cost(losses):
    plt.figure(figsize=(10, 5))
    plt.plot(losses, label='Custo (Perda)')
    plt.xlabel('Épocas')
    plt.ylabel('Perda')
    plt.title('Função de Custo Durante o Treinamento')
    plt.legend()
    plt.show()

# Exibindo os resultados
print("Matriz de Confusão:")
print(f"TP: {TP}, TN: {TN}, FP: {FP}, FN: {FN}")
print(f"Acurácia: {accuracy:.4f}")
print(f"Precisão: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1_score:.4f}")


# plot_decision_boundary(X_train, y_train)
# plot_predictions(X_val, y_val, predictions)
plot_cost(losses)
