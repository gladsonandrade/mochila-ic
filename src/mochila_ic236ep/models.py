from dataclasses import dataclass
from typing import List

@dataclass
class Item:
    id: int
    peso: float
    valor: float
    
    @property
    def razao(self) -> float:
        """Razão valor/peso utilizada pela heurística gulosa."""
        return self.valor / self.peso if self.peso > 0 else 0

@dataclass
class InstanciaMochila:
    capacidade: float
    itens: List[Item]

    @property
    def num_itens(self) -> int:
        return len(self.itens)