import time

from src.mochila_ic236ep.utils import ler_instancia
from src.mochila_ic236ep.metaheuristics import AlgoritmoGenetico


CAMINHO_INSTANCIA = "src/mochila_ic236ep/instancia_grande.txt"


def validar_ag_otimizado(num_execucoes=30):
    instancia = ler_instancia(CAMINHO_INSTANCIA)

    resultados = []
    tempos = []

    for i in range(num_execucoes):
        inicio = time.perf_counter()

        ag = AlgoritmoGenetico(
            instancia=instancia,
            tam_populacao=110,
            geracoes=250,
            tx_mutacao=0.04912570414720041,
            tx_crossover=0.8185280449452739,
            torneio_k=6
        )

        solucao, valor, peso, historico = ag.executar()

        tempo_ms = (time.perf_counter() - inicio) * 1000

        resultados.append(valor)
        tempos.append(tempo_ms)

        print(f"Execução {i + 1}: valor={valor}, peso={peso}, tempo={tempo_ms:.4f} ms")

    print("\n" + "=" * 60)
    print("VALIDAÇÃO DO AG OTIMIZADO")
    print("=" * 60)
    print(f"Execuções: {num_execucoes}")
    print(f"Melhor valor: {max(resultados)}")
    print(f"Pior valor: {min(resultados)}")
    print(f"Valor médio: {sum(resultados) / len(resultados):.2f}")
    print(f"Tempo médio: {sum(tempos) / len(tempos):.4f} ms")
    print("=" * 60)


if __name__ == "__main__":
    validar_ag_otimizado(num_execucoes=30)