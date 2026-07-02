import csv
import os
import matplotlib.pyplot as plt


CAMINHO_RESUMO = "resultados/resumo_comparativo.csv"
PASTA_RESULTADOS = "resultados"


def ler_resumo(caminho_csv):
    dados = []

    with open(caminho_csv, mode="r", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            dados.append({
                "metodo": linha["metodo"],
                "execucoes": int(float(linha["execucoes"])),
                "melhor_valor": float(linha["melhor_valor"]),
                "pior_valor": float(linha["pior_valor"]),
                "valor_medio": float(linha["valor_medio"]),
                "peso_medio": float(linha["peso_medio"]),
                "tempo_medio_ms": float(linha["tempo_medio_ms"]),
            })

    return dados


def gerar_grafico_barras(labels, valores, titulo, ylabel, nome_arquivo):
    plt.figure(figsize=(8, 5))
    plt.bar(labels, valores)
    plt.title(titulo)
    plt.xlabel("Método")
    plt.ylabel(ylabel)
    plt.grid(axis="y", linestyle=":", alpha=0.7)

    caminho_saida = os.path.join(PASTA_RESULTADOS, nome_arquivo)
    plt.savefig(caminho_saida, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Gráfico salvo: {caminho_saida}")


def main():
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)

    dados = ler_resumo(CAMINHO_RESUMO)

    labels = [item["metodo"] for item in dados]

    valores_medios = [item["valor_medio"] for item in dados]
    melhores_valores = [item["melhor_valor"] for item in dados]
    tempos_medios = [item["tempo_medio_ms"] for item in dados]

    gerar_grafico_barras(
        labels=labels,
        valores=valores_medios,
        titulo="Valor Médio por Método",
        ylabel="Valor médio da mochila",
        nome_arquivo="valor_medio_por_metodo.png",
    )

    gerar_grafico_barras(
        labels=labels,
        valores=melhores_valores,
        titulo="Melhor Valor por Método",
        ylabel="Melhor valor encontrado",
        nome_arquivo="melhor_valor_por_metodo.png",
    )

    gerar_grafico_barras(
        labels=labels,
        valores=tempos_medios,
        titulo="Tempo Médio por Método",
        ylabel="Tempo médio (ms)",
        nome_arquivo="tempo_medio_por_metodo.png",
    )


if __name__ == "__main__":
    main()