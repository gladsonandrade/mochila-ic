import time
import matplotlib.pyplot as plt
from src.mochila_ic236ep.utils import ler_instancia
from src.mochila_ic236ep.heuristics import heuristica_gulosa
from src.mochila_ic236ep.metaheuristics import AlgoritmoGenetico

def executar_comparativo(caminho_arquivo: str = "src/mochila_ic236ep/instancia_media.txt"):
    print(f"--- Lendo instância: {caminho_arquivo} ---")
    instancia = ler_instancia(caminho_arquivo)
    
    # 1. Executar e medir Heurística Gulosa
    inicio_gulosa = time.perf_counter()
    sol_gulosa, val_gulosa, peso_gulosa = heuristica_gulosa(instancia)
    tempo_gulosa = (time.perf_counter() - inicio_gulosa) * 1000  # em ms
    
    # 2. Executar e medir Algoritmo Genético
    inicio_ag = time.perf_counter()
    ag = AlgoritmoGenetico(instancia, tam_populacao=50, geracoes=100)
    sol_ag, val_ag, peso_ag, historico_ag = ag.executar()
    tempo_ag = (time.perf_counter() - inicio_ag) * 1000  # em ms
    
    # 3. Imprimir Tabela Comparativa no Terminal
    print("\n" + "="*50)
    print(f"{'MÉTRICA':<20} | {'GULOSA':<12} | {'GENÉTICO':<12}")
    print("="*50)
    print(f"{'Valor Alcançado':<20} | {val_gulosa:<12} | {val_ag:<12}")
    print(f"{'Peso Utilizado':<20} | {peso_gulosa:<12} | {peso_ag:<12}")
    print(f"{'Tempo (ms)':<20} | {tempo_gulosa:<12.4f} | {tempo_ag:<12.4f}")
    print("="*50)
    
    # 4. Plotar e Salvar o Gráfico de Convergência para o Artigo
    plt.figure(figsize=(8, 5))
    plt.plot(historico_ag['melhor'], label='Melhor Indivíduo (Fitness)', color='green', linewidth=2)
    plt.plot(historico_ag['media'], label='Média da População', color='orange', linestyle='--')
    plt.title("Curva de Convergência do Algoritmo Genético")
    plt.xlabel("Gerações")
    plt.ylabel("Valor (Fitness)")
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
    
    # Salva a imagem na pasta principal para subirmos no Overleaf
    plt.savefig("grafico_convergencia.jpg", dpi=300, bbox_inches='tight')
    print("\nSucesso! O gráfico 'grafico_convergencia.jpg' foi salvo na pasta.")
    plt.show()

if __name__ == "__main__":
    # Apontando para o nosso arquivo de teste dentro da pasta src
    executar_comparativo("src/mochila_ic236ep/instancia_grande.txt")