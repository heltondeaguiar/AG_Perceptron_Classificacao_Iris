# -*- coding: utf-8 -*-
"""AG_Perceptron_Classificacao_Iris.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17jUhd2HnlA3REqyKUYKp39n0wIKkPGzH

**Combinando algoritmos bioinspirados**

GRUPO:

*   Ana Gabriela de Abreu Campos - 11621BSI204
*   Gabriel Oliveira Souza - 11821BSI207
*   Helton Pereira de Aguiar - 11811BSI242

O objetivo deste trabalho é utilizar um algoritmo genético (AG) para otimização os pesos de uma rede neural artificial do tipo Perceptron. A equipe deve utilizar a mesma rede implementada na atividade anterior, com eventuais melhorias se necessário. Não é permitido usar bibliotecas com implementações prontas de Perceptron. O uso dessas bibliotecas, entretanto, é permitido para auxiliar outros cálculos, como o de precisão, por exemplo. O Perceptron deve ser utilizado para predizer os dados da base Iris, conforme feito no trabalho anterior.

Cada grupo deve escolher a sua função de avaliação (fitness), que pode ser a precisão ou o erro médio quadrático. Deve, também, escolher como representar os pesos da rede. Note que os pesos são valores reais, ou seja, é necessário utilizar cromossomos compostos por números reais (consulte o material de aula para detalhes de implementação dos operadores genéticos). O AG deve, então, evoluir esses pesos até que um critério de parada seja satisfeito, como um número máximo de gerações, ou até que um valor máximo prédefinido de precisão seja atingido (ou, analogamente, até que um valor mínimo de erro médio seja alcançado).

Note que o algoritmo genético está substituindo a etapa de treinamento da rede; ou seja, todo o treinamento feito no trabalho anterior deve ser substituído pelo AG. Em outras palavras, cada grupo deve selecionar um conjunto de dados para treinamento e, em seguida, aplicar as seguintes etapas:

1. Gerar uma população de pesos com o AG;
2. Para cada indivíduo, aplicar o Perceptron para classificar os dados de treinamento;
3. Para cada classificação, computar o valor do fitness e seguir com as demais etapas do
AG (seleção, recombinação e mutação).

Uma vez que o AG chegou ao fim, deve-se utilizar o melhor indivíduo (vetor de pesos) para classificar os demais dados. O grupo deve reportar, cuidadosamente, todos os parâmetros utilizados nos experimentos. Os resultados devem ser comparados com aqueles obtidos no trabalho anterior.
"""

import random
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# Função para carregar os dados da base Iris
def carregar_dados_iris(classe1, classe2):
    dados_iris = pd.read_csv("iris.data", header=None, names=["comprimento_sepala", "largura_sepala", "comprimento_petala", "largura_petala", "classe"])
    dados_iris = dados_iris[(dados_iris["classe"] == classe1) | (dados_iris["classe"] == classe2)]
    dados_iris["classe"] = np.where(dados_iris["classe"] == classe1, 1, -1)
    return dados_iris

# Função para calcular a precisão do Perceptron com pesos dados
def calcular_precisao(pesos, dados):
    previsoes = [1 if np.dot(pesos, dados.iloc[i, :-1].values) > 0 else -1 for i in range(len(dados))]
    verdadeiros = dados["classe"].values
    return accuracy_score(verdadeiros, previsoes)

# Função para treinar o Perceptron com regularização L2
def treinar_perceptron(dados, taxa_aprendizado, iteracoes, alpha):
    num_caracteristicas = dados.shape[1] - 1
    pesos = np.random.uniform(-1, 1, num_caracteristicas)
    erros = []

    for i in range(iteracoes):
        erro_total = 0
        for j in range(len(dados)):
            x = dados.iloc[j, :-1].values
            y = dados.iloc[j, -1]

            previsao = np.dot(pesos, x)
            if y * previsao <= 0:
                pesos += taxa_aprendizado * y * x - alpha * pesos
                erro_total += 1

        erros.append(erro_total)

    return pesos, erros

# Parâmetros de treinamento
taxa_aprendizado = 0.8
iteracoes = 100
alpha = 0.05 # Fator de regularização L2

# Carregando os dados da base Iris
dados_iris = carregar_dados_iris("Iris-setosa", "Iris-versicolor")
# print(dados_iris)

# Dividindo os dados em treinamento e teste (70% treinamento, 30% teste - segunda prática)
dados_treinamento, dados_teste = train_test_split(dados_iris, test_size=0.3, random_state=42)

# Monitorando o tempo de execução
tempo_inicial = time.time()

# Treinando o Perceptron com regularização
pesos_treinados, erros = treinar_perceptron(dados_treinamento, taxa_aprendizado, iteracoes, alpha)

# Tempo de execução
tempo_execucao = time.time() - tempo_inicial

# Exibindo os pesos treinados
print("Pesos Treinados:")
print(pesos_treinados)

# Avaliando a precisão do Perceptron nos dados de teste
precisao_teste = calcular_precisao(pesos_treinados, dados_teste)
print(f"Precisão nos dados de teste: {precisao_teste}")
print(f"Tempo de execução: {tempo_execucao:.2f} segundos")

# Criando um DataFrame para as iterações e erros
resultados = pd.DataFrame({
    "Iteração": range(1, iteracoes + 1),
    "Erros": erros
})

# Exibindo a tabela completa sem restrições
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print("Tabela de Resultados:")
    print(resultados)

# Plotando o gráfico de erros durante o treinamento
plt.figure(figsize=(10, 6))
plt.plot(range(1, iteracoes + 1), erros)
plt.xlabel("Iterações")
plt.ylabel("Erros")
plt.title("Erro de Treinamento ao Longo das Iterações")
plt.grid(True)
plt.show()