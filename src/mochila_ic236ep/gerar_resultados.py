import csv
import os
import random
import statistics
import time

from src.mochila_ic236ep.utils import ler_instancia
from src.mochila_ic236ep.heuristics import heuristica_gulosa
from src.mochila_ic236ep.metaheuristics import AlgoritmoGenetico


CAMINHO_INSTANCIA = "src/mochila_ic236ep/instancia_grande.txt"
PASTA_RESULTADOS = "resultados"

NUM_EXECUCOES = 30


PARAMETROS_AG_ORIGINAL = {
    "tam_populacao": 50,
    "geracoes": 100,
    "tx_mutacao": 0.05,
    "tx_crossover": 0.8,
    "torneio_k": 3,
}


PARAMETROS_AG_OTIMIZADO = {
    "tam_populacao": 110,
    "geracoes": 250,
    "tx_mutacao": 0.04912570414720041,
    "tx_crossover": 0.8185280449452739,
    "torneio_k": 6,
}


def executar_guloso(instancia):
    inicio = time.perf_counter()

    _, valor, peso = heuristica_gulosa(instancia)

    tempo_ms = (time.perf_counter() - inicio) * 1000

    return {
        "metodo": "Guloso",
        "execucao": 1,
        "valor": valor,
        "peso": peso,
        "tempo_ms": tempo_ms,
        "tam_populacao": "",
        "geracoes": "",
        "tx_mutacao": "",
        "tx_crossover": "",
        "torneio_k": "",
    }


def executar_ag(instancia, nome_metodo, parametros, num_execucoes):
    resultados = []

    for i in range(num_execucoes):
        # Define uma semente para deixar o experimento mais reprodutível
        random.seed(i)

        inicio = time.perf_counter()

        ag = AlgoritmoGenetico(
            instancia=instancia,
            tam_populacao=parametros["tam_populacao"],
            geracoes=parametros["geracoes"],
            tx_mutacao=parametros["tx_mutacao"],
            tx_crossover=parametros["tx_crossover"],
            torneio_k=parametros["torneio_k"],
        )

        _, valor, peso, _ = ag.executar()

        tempo_ms = (time.perf_counter() - inicio) * 1000

        resultado = {
            "metodo": nome_metodo,
            "execucao": i + 1,
            "valor": valor,
            "peso": peso,
            "tempo_ms": tempo_ms,
            "tam_populacao": parametros["tam_populacao"],
            "geracoes": parametros["geracoes"],
            "tx_mutacao": parametros["tx_mutacao"],
            "tx_crossover": parametros["tx_crossover"],
            "torneio_k": parametros["torneio_k"],
        }

        resultados.append(resultado)

        print(
            f"{nome_metodo} - Execução {i + 1}: "
            f"valor={valor}, peso={peso}, tempo={tempo_ms:.4f} ms"
        )

    return resultados


def salvar_csv(caminho, dados):
    if not dados:
        return

    colunas = list(dados[0].keys())

    with open(caminho, mode="w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(dados)


def gerar_resumo(dados):
    resumo = []

    metodos = sorted(set(item["metodo"] for item in dados))

    for metodo in metodos:
        dados_metodo = [item for item in dados if item["metodo"] == metodo]

        valores = [float(item["valor"]) for item in dados_metodo]
        pesos = [float(item["peso"]) for item in dados_metodo]
        tempos = [float(item["tempo_ms"]) for item in dados_metodo]

        resumo.append({
            "metodo": metodo,
            "execucoes": len(dados_metodo),
            "melhor_valor": max(valores),
            "pior_valor": min(valores),
            "valor_medio": statistics.mean(valores),
            "peso_medio": statistics.mean(pesos),
            "tempo_medio_ms": statistics.mean(tempos),
        })

    return resumo


def main():
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)

    instancia = ler_instancia(CAMINHO_INSTANCIA)

    todos_resultados = []

    print("\nExecutando Heurística Gulosa...")
    resultado_guloso = executar_guloso(instancia)
    todos_resultados.append(resultado_guloso)

    print("\nExecutando Algoritmo Genético original...")
    resultados_ag_original = executar_ag(
        instancia=instancia,
        nome_metodo="AG Original",
        parametros=PARAMETROS_AG_ORIGINAL,
        num_execucoes=NUM_EXECUCOES,
    )
    todos_resultados.extend(resultados_ag_original)

    print("\nExecutando Algoritmo Genético otimizado...")
    resultados_ag_otimizado = executar_ag(
        instancia=instancia,
        nome_metodo="AG Otimizado",
        parametros=PARAMETROS_AG_OTIMIZADO,
        num_execucoes=NUM_EXECUCOES,
    )
    todos_resultados.extend(resultados_ag_otimizado)

    caminho_detalhado = os.path.join(PASTA_RESULTADOS, "resultados_detalhados.csv")
    salvar_csv(caminho_detalhado, todos_resultados)

    resumo = gerar_resumo(todos_resultados)
    caminho_resumo = os.path.join(PASTA_RESULTADOS, "resumo_comparativo.csv")
    salvar_csv(caminho_resumo, resumo)

    print("\n" + "=" * 60)
    print("RESULTADOS SALVOS")
    print("=" * 60)
    print(f"Arquivo detalhado: {caminho_detalhado}")
    print(f"Resumo comparativo: {caminho_resumo}")
    print("=" * 60)


if __name__ == "__main__":
    main()