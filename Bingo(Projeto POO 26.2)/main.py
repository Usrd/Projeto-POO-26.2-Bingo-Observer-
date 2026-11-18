import random
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Marcacao:
    jogador: str
    numero: int
    faltam: int


@dataclass(frozen=True)
class Rodada:
    numero: int
    marcacoes: tuple[Marcacao, ...]


class Observer(ABC):

    @abstractmethod
    def update(self, number: int) -> Marcacao | None:
        pass


class FonteNumeros(ABC):

    @abstractmethod
    def sortear_numero(self) -> int | None:
        pass


class Urna(FonteNumeros):

    def __init__(self, quantidade: int = 100):
        if quantidade < 1:
            raise ValueError("A quantidade de números deve ser positiva.")

        self._bolas = list(range(1, quantidade + 1))
        random.shuffle(self._bolas)

    def sortear_numero(self) -> int | None:
        if not self._bolas:
            return None
        return self._bolas.pop()


class Sorteio:

    def __init__(self, fonte: FonteNumeros):
        self._fonte = fonte
        self._observadores: list[Observer] = []

    def adicionar(self, observador: Observer) -> None:
        if observador not in self._observadores:
            self._observadores.append(observador)

    def remover(self, observador: Observer) -> None:
        if observador in self._observadores:
            self._observadores.remove(observador)

    def _notificar(self, numero: int) -> tuple[Marcacao, ...]:
        marcacoes = []
        for observador in tuple(self._observadores):
            marcacao = observador.update(numero)
            if marcacao is not None:
                marcacoes.append(marcacao)
        return tuple(marcacoes)

    def sortear(self) -> Rodada | None:
        numero = self._fonte.sortear_numero()
        if numero is None:
            return None

        marcacoes = self._notificar(numero)
        return Rodada(numero, marcacoes)


class Jogador(Observer):

    def __init__(
        self,
        nome: str,
        quantidade_numeros: int = 10,
        numero_maximo: int = 100,
    ):
        if numero_maximo < 1:
            raise ValueError("O número máximo deve ser positivo.")
        if not 1 <= quantidade_numeros <= numero_maximo:
            raise ValueError(
                "A quantidade de números da cartela deve estar entre "
                "1 e o número máximo."
            )

        self.nome = nome
        self.cartela = set(
            random.sample(range(1, numero_maximo + 1), quantidade_numeros)
        )
        self.marcados: set[int] = set()

    @property
    def venceu(self) -> bool:
        return self.marcados == self.cartela

    def update(self, number: int) -> Marcacao | None:
        if number not in self.cartela or number in self.marcados:
            return None

        self.marcados.add(number)
        faltam = len(self.cartela) - len(self.marcados)
        return Marcacao(self.nome, number, faltam)


class Apresentador(ABC):

    @abstractmethod
    def mostrar_inicio(self) -> None:
        pass

    @abstractmethod
    def mostrar_cartelas(self, jogadores: list[Jogador]) -> None:
        pass

    @abstractmethod
    def mostrar_rodada(self, rodada: Rodada) -> None:
        pass

    @abstractmethod
    def mostrar_vencedores(self, vencedores: list[Jogador]) -> None:
        pass

    @abstractmethod
    def mostrar_fim(self) -> None:
        pass


class ApresentadorConsole(Apresentador):

    def mostrar_inicio(self) -> None:
        for caractere in "Bingo: ":
            print(caractere, end="", flush=True)
            time.sleep(0.2)
        print()
        time.sleep(1)

    def mostrar_cartelas(self, jogadores: list[Jogador]) -> None:
        print("Cartelas dos jogadores:")
        time.sleep(1)
        for jogador in jogadores:
            print(f"Cartela de {jogador.nome}: {sorted(jogador.cartela)}")
            time.sleep(1)

    def mostrar_rodada(self, rodada: Rodada) -> None:
        print(f"\nNúmero sorteado: {rodada.numero}")
        time.sleep(2)
        for marcacao in rodada.marcacoes:
            print(
                f"{marcacao.jogador} marcou {marcacao.numero}; "
                f"faltam {marcacao.faltam}"
            )
            time.sleep(2)

    def mostrar_vencedores(self, vencedores: list[Jogador]) -> None:
        nomes = ", ".join(jogador.nome for jogador in vencedores)
        print(f"\nBINGO! Vencedor(es): {nomes}")

    def mostrar_fim(self) -> None:
        print("Acabaram as bolas!")


class JogoBingo:

    def __init__(
        self,
        sorteio: Sorteio,
        jogadores: list[Jogador],
        apresentador: Apresentador,
    ):
        self._sorteio = sorteio
        self._jogadores = jogadores
        self._apresentador = apresentador

        for jogador in self._jogadores:
            self._sorteio.adicionar(jogador)

    def jogar(self) -> None:
        self._apresentador.mostrar_inicio()
        self._apresentador.mostrar_cartelas(self._jogadores)

        while True:
            rodada = self._sorteio.sortear()
            if rodada is None:
                self._apresentador.mostrar_fim()
                return

            self._apresentador.mostrar_rodada(rodada)
            vencedores = [
                jogador for jogador in self._jogadores if jogador.venceu
            ]

            if vencedores:
                self._apresentador.mostrar_vencedores(vencedores)
                return


def main() -> None:
    numero_maximo = 100
    jogadores = [
        Jogador("Arlindo Lúcio da Silva", numero_maximo=numero_maximo),
        Jogador("Maria da Costa Gonçalves", numero_maximo=numero_maximo),
        Jogador("Geraldo Rodrigues de Souza", numero_maximo=numero_maximo),
    ]

    urna = Urna(numero_maximo)
    sorteio = Sorteio(urna)
    apresentador = ApresentadorConsole()

    jogo = JogoBingo(sorteio, jogadores, apresentador)
    jogo.jogar()


if __name__ == "__main__":
    main()
