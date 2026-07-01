from src.mochila_ic236ep.models import InstanciaMochila
from typing import List, Tuple

def heuristica_gulosa(instancia: InstanciaMochila) -> Tuple[List[int], float, float]:
    """
    Resolve o Problema da Mochila utilizando uma abordagem gulosa.
    Ordena os itens pela razão valor/peso de forma decrescente.
    """
    # Ordenar os itens pela razão (maior rácio primeiro)
    itens_ordenados = sorted(instancia.itens, key=lambda x: x.razao, reverse=True)
    
    # Inicializar a solução (vetor de zeros) e os contadores
    solucao = [0] * instancia.num_itens
    peso_total = 0.0
    valor_total = 0.0
    
    for item in itens_ordenados:
        # Verifica se o item ainda cabe na mochila
        if peso_total + item.peso <= instancia.capacidade:
            solucao[item.id] = 1 # 1 significa que o item foi selecionado
            peso_total += item.peso
            valor_total += item.valor
            
    return solucao, valor_total, peso_total

# Teste rápido
if __name__ == "__main__":
    from utils import ler_instancia
    
    # Vamos ler o nosso ficheiro de teste
    instancia_teste = ler_instancia("src/mochila_ic236ep/teste.txt")
    sol, valor, peso = heuristica_gulosa(instancia_teste)
    
    print("--- Resultado da Heurística Gulosa ---")
    print(f"Vetor Solução (1=Selecionado, 0=Ficou de fora): {sol}")
    print(f"Valor Total Alcançado: {valor}")
    print(f"Peso Utilizado: {peso} / {instancia_teste.capacidade}")