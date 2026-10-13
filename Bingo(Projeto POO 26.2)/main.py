import random
import time
from abc import ABC, abstractmethod


Title = ("Bingo da Familia Salamanca: ")

for i in Title:
    print(i, end='')
    time.sleep(0.2)


class Observer(ABC):
   @abstractmethod
   def update(self, number: int) -> None:
       pass
   time.sleep(2)


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

    def notificar(self, number: int) -> None:
        for obs in list(self.observador):
            obs.update(number)
            time.sleep(5)

    def sortear(self) -> int | None:
        if not self.balls:
            return None
        number = self.balls.pop()
        self.sorteados.append(number)
        print(f"\nNumero sorteado: {number}")
        self.notificar(number)
        return number


class Jogador(Observer):
    def __init__(self, name: str, qtd_numbers: int = 10, max: int = 75):
        self.name = name
        self.cartela = set(random.sample(range(1, max + 1), qtd_numbers))
        self.marcados: set[int] = set()
        time.sleep(2)


    @property
    def venceu(self) -> bool:
        return self.marcados == self.cartela
    time.sleep(2)

    def update(self, number: int) -> None:
        if number in self.cartela:
            self.marcados.add(number)
            faltam = len(self.cartela) - len(self.marcados)
            print(f"{self.name} marcou {number} (faltam {faltam})")
            time.sleep(2)


def jogar() -> None:
    sorteador = Sorteio()
    jogadores = [Jogador("Hector Salamanca"), Jogador("Tuco Salamanca"), Jogador("Lalo Salamanca")]
    time.sleep(2)

    for j in jogadores:
        sorteador.adicionar(j)
        print(f"Cartela de {j.name}: {sorted(j.cartela)}")
        time.sleep(2)

    while True:
        if sorteador.sortear() is None:
            print("Acabaram as bolas!")
            break
        vencedores = [j for j in jogadores if j.venceu]
        if vencedores:
            print("\nBINGO! Vencedor(es):", ", ".join(j.name for j in vencedores))
            time.sleep(2)
            break


if __name__ == "__main__":
    jogar()

