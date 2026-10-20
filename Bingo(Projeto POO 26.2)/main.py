import random
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class Marcacao:
    jogador: str
    numero: int
    faltam: int

@dataclass
class Rodada:
    numero: int
    marcacoes: list[Marcacao]

class Observer(ABC):
   @abstractmethod
   def update(self, number: int) -> Marcacao | None:
       pass


class Sorteio():
    def __init__(self, max: int = 100):
        self.observador:list[Observer] = []
        self.balls = list(range(1, max + 1))
        random.shuffle(self.balls)
        self.sorteados: list[int] = []

    def adicionar(self, observer:Observer) -> None:
        if observer not in self.observador:
            self.observador.append(observer)

    def remover(self, observer:Observer) -> None:
        if observer in self.observador:
            self.observador.remove(observer)

    def notificar(self, number: int) -> list[Marcacao]:
        resultados = (obs.update(number) for obs in list(self.observador))
        return [r for r in resultados if r is not None]

    def sortear(self) -> Rodada | None:
        if not self.balls:
            return None
        number = self.balls.pop()
        self.sorteados.append(number)
        self.notificar(number)
        return Rodada(number, self.notificar(number))


class Jogador(Observer):
    def __init__(self, name: str, qtd_numbers: int = 10, max: int = 75):
        self.name = name
        self.cartela = set(random.sample(range(1, max + 1), qtd_numbers))
        self.marcados: set[int] = set()

    @property
    def venceu(self) -> bool:
        return self.marcados == self.cartela

    def update(self, number: int) -> Marcacao | None:
        if number in self.cartela:
            self.marcados.add(number)
            faltam = len(self.cartela) - len(self.marcados)
            return Marcacao(self.name, number, faltam)


def jogar() -> None:
    sorteador = Sorteio()
    jogadores = [Jogador("Arlindo Lúcio da Silva"), Jogador("Maria da Costa Gonçalves"), Jogador("Geraldo Rodrigues de Souza")]

    for j in jogadores:
        sorteador.adicionar(j)

    for c in "Bingo: ":
        print(c, end='', flush=True)
        time.sleep(0.2)
    print()
    time.sleep(1)

    print("Cartelas dos jogadores: ")
    time.sleep(1)
    for j in jogadores:
        print(f"Cartela de {j.name}: {sorted(j.cartela)}")
        time.sleep(1)

    while True:
        rodada = sorteador.sortear()
        if rodada is None:
            print("Acabaram as bolas!")
            break

        print(f"\nNumero sorteado: {rodada.numero}")
        time.sleep(2)
        for m in rodada.marcacoes:
            print(f"{m.jogador} marcou {m.numero} faltam {m.faltam}")
            time.sleep(2)

        vencedores = [j for j in jogadores if j.venceu]
        if vencedores:
            print("\nBINGO! Vencedor(es):", ", ".join(j.name for j in vencedores))
            break


if __name__ == "__main__":
    jogar()

