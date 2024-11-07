import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Funções dos modelos
def MQO_Default(x, y):
    return np.linalg.pinv(x.T @ x) @ x.T @ y

def MQO_Regularizado(x, y, lambdaa):
    i = np.eye(x.shape[1])
    return np.linalg.pinv(x.T @ x + lambdaa * i) @ x.T @ y

def Media_Observaveis(y):
    return np.mean(y) * np.ones_like(y)

# Carregar e organizar os dados
datasMQO = np.loadtxt("aerogerador.dat")
x_raw = datasMQO[:, 0]
y_raw = datasMQO[:, 1]
x_raw = np.vstack([np.ones(len(x_raw)), x_raw]).T  # Adicionar intercepto

# Visualização inicial dos dados
plt.scatter(x_raw[:, 1], y_raw, color='blue', alpha=0.6)
plt.xlabel("Velocidade do Vento")
plt.ylabel("Potência Gerada")
plt.title("Gráfico de Dispersão da Potência Gerada vs Velocidade do Vento")
plt.show()

colors = ['red', 'purple', 'orange', 'brown']
lambdas = [0.25, 0.5, 0.75, 1]
Rounds = 500
rss_media = []
rss_mqo_default = []
rss_mqo_regularizado = {l: [] for l in lambdas}

# Simulação Monte Carlo para validação
for _ in range(Rounds):
    # Divisão dos dados em treino e teste
    indices = np.random.permutation(len(y_raw))
    split = int(len(y_raw) * 0.8)
    train_idx, test_idx = indices[:split], indices[split:]
    
    x_train, x_test = x_raw[train_idx], x_raw[test_idx]
    y_train, y_test = y_raw[train_idx], y_raw[test_idx]

    # Plot da dispersão dos dados de treino
    #plt.scatter(x_train[:, 1], y_train, color='blue', alpha=0.6, label="Dados de treino")

    # Media dos valores observaveis
    y_pred_media = Media_Observaveis(y_train)
    rss_media.append(np.sum((y_test - y_pred_media[:len(y_test)]) ** 2))

    # MQO padrão
    beta_default = MQO_Default(x_train, y_train)
    y_pred_default = x_test @ beta_default  # Calcula predição para dados de treino
    #plt.plot(x_train[:, 1], y_pred_default, color='green', label="MQO_Default") plota a linha para cada mqo_default em cada round
    rss_mqo_default.append(np.sum((y_test - y_pred_default) ** 2))

    # MQO regularizado para cada valor de lambda
    for l, color in zip(lambdas, colors):
        beta_reg = MQO_Regularizado(x_train, y_train, l)
        y_pred_reg = x_test @ beta_reg  # Calcula predição para dados de treino
        #plt.plot(x_train[:, 1], y_pred_reg, color=color, label=f"MQO_Reg_lambda_{l}") plota a linha para cada lambda em cada round
        rss_mqo_regularizado[l].append(np.sum((y_test - y_pred_reg) ** 2))

    # Mostrar a legenda e o grafico para o round atual
    #plt.xlabel("Velocidade do Vento")
    #plt.ylabel("Potência Gerada")
    #plt.title(f"Round {_ + 1}: Modelos de Regressão sobre Dados de Treino")
    #plt.legend()
    #plt.show()

# Calculo dos resultados de cada modelo
def calc_stats(rss):
    return {
        "Media": np.mean(rss),
        "Desvio_Padrao": np.std(rss),
        "Maior": np.max(rss),
        "Menor": np.min(rss)
    }

resultados = {
    "Media de valroes observaveis": calc_stats(rss_media),
    "MQO_Default": calc_stats(rss_mqo_default)
}
for l in lambdas:
    resultados[f"MQO_Reg_lambda_{l}"] = calc_stats(rss_mqo_regularizado[l])

# Resultados
df_resultados = pd.DataFrame(resultados).T
print(df_resultados)
