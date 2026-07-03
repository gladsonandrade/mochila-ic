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

    ordem = {
        "Guloso": 0,
        "AG Original": 1,
        "AG Otimizado": 2,
    }

    return sorted(dados, key=lambda item: ordem.get(item["metodo"], 99))


def formatar_numero(valor):
    if valor >= 100:
        return f"{valor:.2f}"
    if valor >= 1:
        return f"{valor:.4f}"
    return f"{valor:.5f}"


def adicionar_rotulos(barras, valores):
    for barra, valor in zip(barras, valores):
        altura = barra.get_height()

        plt.text(
            barra.get_x() + barra.get_width() / 2,
            altura,
            formatar_numero(valor),
            ha="center",
            va="bottom",
            fontsize=9
        )


def gerar_grafico_valor(labels, valores, titulo, ylabel, nome_arquivo):
    plt.figure(figsize=(8, 5))

    barras = plt.bar(labels, valores)
    adicionar_rotulos(barras, valores)

    menor = min(valores)
    maior = max(valores)
    margem = max((maior - menor) * 0.4, 2)

    plt.ylim(menor - margem, maior + margem)

    plt.title(titulo)
    plt.xlabel("Método")
    plt.ylabel(ylabel)
    plt.grid(axis="y", linestyle=":", alpha=0.7)

    caminho_saida = os.path.join(PASTA_RESULTADOS, nome_arquivo)
    plt.savefig(caminho_saida, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Gráfico salvo: {caminho_saida}")


def gerar_grafico_tempo(labels, valores, titulo, ylabel, nome_arquivo):
    plt.figure(figsize=(8, 5))

    barras = plt.bar(labels, valores)
    adicionar_rotulos(barras, valores)

    plt.yscale("log")

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

    gerar_grafico_valor(
        labels=labels,
        valores=valores_medios,
        titulo="Valor Médio por Método",
        ylabel="Valor médio da mochila",
        nome_arquivo="valor_medio_por_metodo.png",
    )

    gerar_grafico_valor(
        labels=labels,
        valores=melhores_valores,
        titulo="Melhor Valor por Método",
        ylabel="Melhor valor encontrado",
        nome_arquivo="melhor_valor_por_metodo.png",
    )

    gerar_grafico_tempo(
        labels=labels,
        valores=tempos_medios,
        titulo="Tempo Médio por Método",
        ylabel="Tempo médio (ms) - escala logarítmica",
        nome_arquivo="tempo_medio_por_metodo.png",
    )


if __name__ == "__main__":
    main()