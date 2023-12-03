import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import time

# Função para carregar os dados da base Iris a partir do arquivo local
def carregar_dados_iris(classe1, classe2):
    dados_iris = pd.read_csv("iris.data", header=None, names=["comprimento_sepala", "largura_sepala", "comprimento_petala", "largura_petala", "classe"])
    dados_iris = dados_iris[(dados_iris["classe"] == classe1) | (dados_iris["classe"] == classe2)]
    dados_iris["classe"] = np.where(dados_iris["classe"] == classe1, 1, -1)
    return dados_iris

# Função para treinar o Perceptron
def treinar_perceptron(dados, pesos, taxa_aprendizado, iteracoes):
    erros = []

    for _ in range(iteracoes):
        erro_total = 0
        for j in range(len(dados)):
            x = dados.iloc[j, :-1].values
            y = dados.iloc[j, -1]

            previsao = np.dot(pesos, x)
            if y * previsao <= 0:
                pesos += taxa_aprendizado * y * x
                erro_total += 1

        erros.append(erro_total)

    return pesos, erros

# Função para fazer previsões com o perceptron treinado
def prever_perceptron(pesos, x):
    previsao = np.dot(pesos, x)
    return 1 if previsao > 0 else -1

# Função para avaliar a precisão do perceptron
def avaliar_perceptron(pesos, dados):
    previsoes = [prever_perceptron(pesos, dados.iloc[i, :-1].values) for i in range(len(dados))]
    verdadeiros = dados["classe"].values
    matriz_confusao = confusion_matrix(verdadeiros, previsoes)

    if matriz_confusao.shape == (1, 1):
        precisao = 1.0  # Lidando com o caso em que há apenas um valor na matriz de confusão
    else:
        precisao = matriz_confusao[0, 0] / (matriz_confusao[0, 0] + matriz_confusao[0, 1])

    return precisao

# Função para inicializar a população do AG
def inicializar_populacao(num_individuos, num_pesos):
    return [np.random.uniform(-1, 1, num_pesos) for _ in range(num_individuos)]

# Função para avaliar a população do AG
def avaliar_populacao(populacao, dados_treinamento):
    return [avaliar_perceptron(individuo, dados_treinamento) for individuo in populacao]

# Função de seleção para o AG
def selecionar(populacao, fitness, percentual_selecao):
    num_selecionados = int(len(populacao) * percentual_selecao)
    indices_selecionados = np.argsort(fitness)[-num_selecionados:]
    selecionados = [populacao[i] for i in indices_selecionados]
    return selecionados

# Função de crossover para o AG
def crossover(pai1, pai2, taxa_crossover):
    if random.uniform(0, 1) < taxa_crossover:
        ponto_corte = random.randint(1, len(pai1) - 1)
        filho1 = np.concatenate((pai1[:ponto_corte], pai2[ponto_corte:]))
        filho2 = np.concatenate((pai2[:ponto_corte], pai1[ponto_corte:]))
        return filho1, filho2
    else:
        return pai1, pai2

# Função de mutação para o AG
def mutacao(individuo, taxa_mutacao):
    for i in range(len(individuo)):
        if random.uniform(0, 1) < taxa_mutacao:
            individuo[i] += random.uniform(-0.5, 0.5)
    return individuo

# Função do Algoritmo Genético (AG)
def algoritmo_genetico(dados_treinamento, num_individuos, taxa_crossover, taxa_mutacao, percentual_selecao, num_geracoes):
    num_pesos = len(dados_treinamento.columns) - 1
    populacao = inicializar_populacao(num_individuos, num_pesos)

    melhores_individuos = []

    for geracao in range(num_geracoes):
        # Avaliação da população
        fitness = avaliar_populacao(populacao, dados_treinamento)

        # Seleção de indivíduos
        selecionados = selecionar(populacao, fitness, percentual_selecao)

        # Recombinação (Crossover)
        nova_populacao = []
        for i in range(0, len(selecionados), 2):
            pai1 = selecionados[i]
            pai2 = selecionados[i + 1] if i + 1 < len(selecionados) else selecionados[i]
            filho1, filho2 = crossover(pai1, pai2, taxa_crossover)
            nova_populacao.extend([filho1, filho2])

        # Mutação
        nova_populacao = [mutacao(individuo, taxa_mutacao) for individuo in nova_populacao]

        # Substituir a antiga população pela nova
        populacao = nova_populacao

        # Armazenar o melhor indivíduo de cada geração
        melhor_individuo = populacao[np.argmax(fitness)]
        melhores_individuos.append(melhor_individuo)

    # Avaliação final da população
    fitness_final = avaliar_populacao(populacao, dados_treinamento)

    # Seleção do melhor indivíduo
    melhor_individuo = populacao[np.argmax(fitness_final)]

    return melhor_individuo, melhores_individuos

# Carregando os dados da base Iris
dados_iris = carregar_dados_iris("Iris-setosa", "Iris-versicolor")

# Dividindo os dados em treinamento e teste (70% treinamento, 30% teste)
percentual_treinamento = 0.7
tamanho_treinamento = int(percentual_treinamento * len(dados_iris))
dados_treinamento = dados_iris[:tamanho_treinamento]
dados_teste = dados_iris[tamanho_treinamento:]

# Parâmetros do perceptron
taxa_aprendizado_perceptron = 0.1
iteracoes_perceptron = 100

# Parâmetros do AG
num_individuos_ag = 100
taxa_crossover_ag = 0.5
taxa_mutacao_ag = 0.4
percentual_selecao_ag = 0.7
num_geracoes_ag = 90

# Inicialização dos pesos com AG
pesos_iniciais, melhores_individuos = algoritmo_genetico(dados_treinamento, num_individuos_ag, taxa_crossover_ag, taxa_mutacao_ag, percentual_selecao_ag, num_geracoes_ag)

# Treinando o Perceptron com pesos iniciais do AG
inicio_treinamento = time.time()
pesos_treinados, erros_treinamento = treinar_perceptron(dados_treinamento, pesos_iniciais, taxa_aprendizado_perceptron, iteracoes_perceptron)
tempo_treinamento = time.time() - inicio_treinamento

# Avaliando o Perceptron nos dados de teste
precisao_teste = avaliar_perceptron(pesos_treinados, dados_teste)

# Exibindo resultados
print("Pesos Treinados:", pesos_treinados)
print("Precisão nos dados de teste:", precisao_teste)
print("Tempo de execução (treinamento): {:.2f} segundos".format(tempo_treinamento))
print("Erros durante o treinamento:", erros_treinamento)

# Gráfico 1: Mutação da Melhor Precisão Gerada
melhores_precisoes = [avaliar_perceptron(individuo, dados_treinamento) for individuo in melhores_individuos]
plt.plot(melhores_precisoes, marker='o')
plt.title('Mutação da Melhor Precisão Gerada')
plt.xlabel('Geração')
plt.ylabel('Precisão')
plt.show()

# Gráfico 2: Evolução dos Erros durante o Treinamento
plt.plot(erros_treinamento, marker='o')
plt.title('Evolução dos Erros durante o Treinamento')
plt.xlabel('Época')
plt.ylabel('Erros')
plt.show()

# Gráfico 3: Melhores Indivíduos
for i in range(len(melhores_individuos[0])):
    plt.plot([individuo[i] for individuo in melhores_individuos], label=f'Peso {i+1}')

plt.title('Evolução dos Melhores Indivíduos')
plt.xlabel('Geração')
plt.ylabel('Valor do Peso')
plt.legend()
plt.show()