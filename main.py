import os
import random
import time

import matplotlib.pyplot as plt

from src.mochila_ic236ep.utils import ler_instancia
from src.mochila_ic236ep.heuristics import heuristica_gulosa
from src.mochila_ic236ep.metaheuristics import AlgoritmoGenetico
from src.mochila_ic236ep.memetic import AlgoritmoMemetico


CAMINHO_INSTANCIA = "src/mochila_ic236ep/instancia_grande.txt"
PASTA_RESULTADOS = "resultados"


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

    solucao, valor, peso = heuristica_gulosa(instancia)

    tempo_ms = (time.perf_counter() - inicio) * 1000

    return solucao, valor, peso, tempo_ms


def executar_ag(instancia, parametros, semente=0):
    random.seed(semente)

    inicio = time.perf_counter()

    ag = AlgoritmoGenetico(
        instancia=instancia,
        tam_populacao=parametros["tam_populacao"],
        geracoes=parametros["geracoes"],
        tx_mutacao=parametros["tx_mutacao"],
        tx_crossover=parametros["tx_crossover"],
        torneio_k=parametros["torneio_k"],
    )

    solucao, valor, peso, historico = ag.executar()

    tempo_ms = (time.perf_counter() - inicio) * 1000

    return solucao, valor, peso, tempo_ms, historico


def executar_memetico(instancia, parametros, semente=0):
    random.seed(semente)

    inicio = time.perf_counter()

    memetico = AlgoritmoMemetico(
        instancia=instancia,
        tam_populacao=parametros["tam_populacao"],
        geracoes=parametros["geracoes"],
        tx_mutacao=parametros["tx_mutacao"],
        tx_crossover=parametros["tx_crossover"],
        torneio_k=parametros["torneio_k"],
    )

    solucao, valor, peso, historico = memetico.executar()

    tempo_ms = (time.perf_counter() - inicio) * 1000

    return solucao, valor, peso, tempo_ms, historico


def imprimir_tabela(resultados):
    print("\n" + "=" * 80)
    print("COMPARATIVO DOS MÉTODOS")
    print("=" * 80)
    print(f"{'Método':<20} | {'Valor':<12} | {'Peso':<12} | {'Tempo (ms)':<12}")
    print("-" * 80)

    for resultado in resultados:
        print(
            f"{resultado['metodo']:<20} | "
            f"{resultado['valor']:<12.2f} | "
            f"{resultado['peso']:<12.2f} | "
            f"{resultado['tempo_ms']:<12.4f}"
        )

    print("=" * 80)


def gerar_grafico_convergencia(
    historico_original,
    historico_otimizado,
    historico_memetico
):
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)

    plt.figure(figsize=(8, 5))

    plt.plot(
        historico_original["melhor"],
        label="AG Original",
        linewidth=2
    )

    plt.plot(
        historico_otimizado["melhor"],
        label="AG Otimizado",
        linewidth=2
    )

    plt.plot(
        historico_memetico["melhor"],
        label="Memético",
        linewidth=2
    )

    plt.title("Curva de Convergência dos Métodos Evolutivos")
    plt.xlabel("Geração")
    plt.ylabel("Melhor fitness")
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.7)

    caminho_saida = os.path.join(
        PASTA_RESULTADOS,
        "convergencia_ag_vs_memetico.png"
    )

    plt.savefig(caminho_saida, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\nGráfico salvo em: {caminho_saida}")


def executar_comparativo():
    print(f"Lendo instância: {CAMINHO_INSTANCIA}")

    instancia = ler_instancia(CAMINHO_INSTANCIA)

    print("\nExecutando Heurística Gulosa...")
    _, val_guloso, peso_guloso, tempo_guloso = executar_guloso(instancia)

    print("Executando Algoritmo Genético Original...")
    _, val_ag_original, peso_ag_original, tempo_ag_original, hist_ag_original = executar_ag(
        instancia,
        PARAMETROS_AG_ORIGINAL,
        semente=0
    )

    print("Executando Algoritmo Genético Otimizado...")
    _, val_ag_otimizado, peso_ag_otimizado, tempo_ag_otimizado, hist_ag_otimizado = executar_ag(
        instancia,
        PARAMETROS_AG_OTIMIZADO,
        semente=0
    )

    print("Executando Algoritmo Memético...")
    _, val_memetico, peso_memetico, tempo_memetico, hist_memetico = executar_memetico(
        instancia,
        PARAMETROS_AG_OTIMIZADO,
        semente=0
    )

    resultados = [
        {
            "metodo": "Guloso",
            "valor": val_guloso,
            "peso": peso_guloso,
            "tempo_ms": tempo_guloso,
        },
        {
            "metodo": "AG Original",
            "valor": val_ag_original,
            "peso": peso_ag_original,
            "tempo_ms": tempo_ag_original,
        },
        {
            "metodo": "AG Otimizado",
            "valor": val_ag_otimizado,
            "peso": peso_ag_otimizado,
            "tempo_ms": tempo_ag_otimizado,
        },
        {
            "metodo": "Memético",
            "valor": val_memetico,
            "peso": peso_memetico,
            "tempo_ms": tempo_memetico,
        },
    ]

    imprimir_tabela(resultados)

    gerar_grafico_convergencia(
        historico_original=hist_ag_original,
        historico_otimizado=hist_ag_otimizado,
        historico_memetico=hist_memetico
    )


if __name__ == "__main__":
    executar_comparativo()