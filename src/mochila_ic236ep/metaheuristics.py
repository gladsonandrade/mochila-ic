import random
from typing import List, Tuple, Dict
from src.mochila_ic236ep.models import InstanciaMochila

class AlgoritmoGenetico:
    def __init__(self, instancia: InstanciaMochila, tam_populacao: int = 50, 
                 geracoes: int = 100, tx_mutacao: float = 0.05, 
                 tx_crossover: float = 0.8, torneio_k: int = 3):
        self.instancia = instancia
        self.tam_populacao = tam_populacao
        self.geracoes = geracoes
        self.tx_mutacao = tx_mutacao
        self.tx_crossover = tx_crossover
        self.torneio_k = torneio_k

    def calcular_fitness(self, individuo: List[int]) -> Tuple[float, float]:
        """Calcula o valor e penaliza se ultrapassar a capacidade da mochila."""
        peso_total = sum(self.instancia.itens[i].peso * individuo[i] for i in range(self.instancia.num_itens))
        valor_total = sum(self.instancia.itens[i].valor * individuo[i] for i in range(self.instancia.num_itens))
        
        if peso_total > self.instancia.capacidade:
            # Penalização severa: Excesso de peso * 10 vezes a maior razão dos itens
            excesso = peso_total - self.instancia.capacidade
            taxa_penalizacao = max(item.razao for item in self.instancia.itens) * 10
            fitness = valor_total - (excesso * taxa_penalizacao)
            return max(0, fitness), peso_total
            
        return valor_total, peso_total

    def criar_individuo(self) -> List[int]:
        """Cria um vetor binário aleatório (cromossomo)."""
        return [random.choice([0, 1]) for _ in range(self.instancia.num_itens)]

    def selecao_torneio(self, populacao: List[List[int]], fitnesses: List[float]) -> List[int]:
        """Escolhe K indivíduos e retorna o melhor deles."""
        selecionados = random.sample(range(self.tam_populacao), self.torneio_k)
        melhor_idx = max(selecionados, key=lambda idx: fitnesses[idx])
        return populacao[melhor_idx]

    def crossover(self, pai1: List[int], pai2: List[int]) -> Tuple[List[int], List[int]]:
        """Cruzamento de 1 ponto de corte."""
        if random.random() < self.tx_crossover:
            ponto = random.randint(1, self.instancia.num_itens - 1)
            filho1 = pai1[:ponto] + pai2[ponto:]
            filho2 = pai2[:ponto] + pai1[ponto:]
            return filho1, filho2
        return pai1[:], pai2[:]

    def mutacao(self, individuo: List[int]) -> List[int]:
        """Inverte os bits com base na taxa de mutação (Bit Flip)."""
        return [1 - gene if random.random() < self.tx_mutacao else gene for gene in individuo]

    def executar(self) -> Tuple[List[int], float, float, Dict[str, List[float]]]:
        populacao = [self.criar_individuo() for _ in range(self.tam_populacao)]
        
        melhor_individuo = None
        melhor_fitness = -1
        melhor_peso = 0
        historico = {'melhor': [], 'media': []} # Para os gráficos do artigo

        for _ in range(self.geracoes):
            avaliacoes = [self.calcular_fitness(ind) for ind in populacao]
            fitnesses = [av[0] for av in avaliacoes]
            pesos = [av[1] for av in avaliacoes]

            # Encontrar o melhor da geração atual (que seja válido)
            for i, fit in enumerate(fitnesses):
                if fit > melhor_fitness and pesos[i] <= self.instancia.capacidade:
                    melhor_fitness = fit
                    melhor_peso = pesos[i]
                    melhor_individuo = populacao[i][:]

            historico['melhor'].append(max(fitnesses))
            historico['media'].append(sum(fitnesses) / self.tam_populacao)

            # Nova geração com Elitismo (garante que o melhor não se perca)
            nova_populacao = []
            if melhor_individuo:
                nova_populacao.append(melhor_individuo[:])

            while len(nova_populacao) < self.tam_populacao:
                pai1 = self.selecao_torneio(populacao, fitnesses)
                pai2 = self.selecao_torneio(populacao, fitnesses)
                filho1, filho2 = self.crossover(pai1, pai2)
                nova_populacao.append(self.mutacao(filho1))
                if len(nova_populacao) < self.tam_populacao:
                    nova_populacao.append(self.mutacao(filho2))

            populacao = nova_populacao

        return melhor_individuo, melhor_fitness, melhor_peso, historico

# Teste Rápido
if __name__ == "__main__":
    from utils import ler_instancia
    
    # ATENÇÃO: Ajuste o caminho se necessário (como fizemos antes)
    instancia_teste = ler_instancia("src/mochila_ic236ep/teste.txt") 
    
    ag = AlgoritmoGenetico(instancia_teste, tam_populacao=20, geracoes=50)
    sol_ag, val_ag, peso_ag, hist_ag = ag.executar()
    
    print("--- Resultado do Algoritmo Genético ---")
    print(f"Vetor Solução: {sol_ag}")
    print(f"Valor Total Alcançado: {val_ag}")
    print(f"Peso Utilizado: {peso_ag} / {instancia_teste.capacidade}")