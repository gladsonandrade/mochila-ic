import time
import optuna

from src.mochila_ic236ep.utils import ler_instancia
from src.mochila_ic236ep.metaheuristics import AlgoritmoGenetico


CAMINHO_INSTANCIA = "src/mochila_ic236ep/instancia_grande.txt"


def objective(trial):
    """
    Função objetivo do Optuna.

    Cada trial testa uma combinação diferente de parâmetros
    para o Algoritmo Genético.
    """

    tam_populacao = trial.suggest_int("tam_populacao", 20, 120, step=10)
    geracoes = trial.suggest_int("geracoes", 50, 250, step=25)
    tx_mutacao = trial.suggest_float("tx_mutacao", 0.01, 0.20)
    tx_crossover = trial.suggest_float("tx_crossover", 0.60, 0.95)
    torneio_k = trial.suggest_int("torneio_k", 2, 6)

    instancia = ler_instancia(CAMINHO_INSTANCIA)

    inicio = time.perf_counter()

    ag = AlgoritmoGenetico(
        instancia=instancia,
        tam_populacao=tam_populacao,
        geracoes=geracoes,
        tx_mutacao=tx_mutacao,
        tx_crossover=tx_crossover,
        torneio_k=torneio_k
    )

    _, valor, peso, _ = ag.executar()

    tempo_ms = (time.perf_counter() - inicio) * 1000

    trial.set_user_attr("valor", valor)
    trial.set_user_attr("peso", peso)
    trial.set_user_attr("tempo_ms", tempo_ms)

    return valor


def executar_otimizacao(n_trials=50):
    """
    Executa a otimização dos hiperparâmetros do Algoritmo Genético.
    """

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials)

    print("\n" + "=" * 60)
    print("MELHORES PARÂMETROS ENCONTRADOS")
    print("=" * 60)

    for parametro, valor in study.best_params.items():
        print(f"{parametro}: {valor}")

    print("\nMelhor valor encontrado:", study.best_value)

    melhor_trial = study.best_trial

    print("Peso da melhor solução:", melhor_trial.user_attrs["peso"])
    print(f"Tempo da melhor execução: {melhor_trial.user_attrs['tempo_ms']:.4f} ms")
    print("=" * 60)


if __name__ == "__main__":
    executar_otimizacao(n_trials=50)