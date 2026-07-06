from typing import Dict, List, Tuple

from src.mochila_ic236ep.heuristics import heuristica_gulosa
from src.mochila_ic236ep.metaheuristics import AlgoritmoGenetico
from src.mochila_ic236ep.models import InstanciaMochila


class AlgoritmoMemetico(AlgoritmoGenetico):
    """
    Algoritmo Memético para o Problema da Mochila 0-1.

    Esta abordagem combina a Heurística Gulosa com o Algoritmo Genético.
    A solução gerada pelo guloso é inserida como um indivíduo inicial forte
    dentro da população inicial do AG.
    """

    def __init__(
        self,
        instancia: InstanciaMochila,
        tam_populacao: int = 110,
        geracoes: int = 250,
        tx_mutacao: float = 0.04912570414720041,
        tx_crossover: float = 0.8185280449452739,
        torneio_k: int = 6,
    ):
        super().__init__(
            instancia=instancia,
            tam_populacao=tam_populacao,
            geracoes=geracoes,
            tx_mutacao=tx_mutacao,
            tx_crossover=tx_crossover,
            torneio_k=torneio_k,
        )

    def gerar_populacao_inicial(self) -> List[List[int]]:
        """
        Cria a população inicial do Algoritmo Memético.

        O primeiro indivíduo é a solução da Heurística Gulosa.
        Os demais indivíduos são gerados aleatoriamente.
        """
        solucao_gulosa, _, _ = heuristica_gulosa(self.instancia)

        populacao = [solucao_gulosa[:]]

        while len(populacao) < self.tam_populacao:
            populacao.append(self.criar_individuo())

        return populacao

    def executar(self) -> Tuple[List[int], float, float, Dict[str, List[float]]]:
        """
        Executa o Algoritmo Memético.

        Mantém a mesma estrutura de retorno do Algoritmo Genético:
        solução, valor, peso e histórico.
        """
        populacao = self.gerar_populacao_inicial()

        melhor_individuo = None
        melhor_fitness = -1
        melhor_peso = 0

        historico = {
            "melhor": [],
            "media": [],
        }

        for _ in range(self.geracoes):
            avaliacoes = [self.calcular_fitness(ind) for ind in populacao]
            fitnesses = [av[0] for av in avaliacoes]
            pesos = [av[1] for av in avaliacoes]

            for i, fit in enumerate(fitnesses):
                if fit > melhor_fitness and pesos[i] <= self.instancia.capacidade:
                    melhor_fitness = fit
                    melhor_peso = pesos[i]
                    melhor_individuo = populacao[i][:]

            historico["melhor"].append(max(fitnesses))
            historico["media"].append(sum(fitnesses) / self.tam_populacao)

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