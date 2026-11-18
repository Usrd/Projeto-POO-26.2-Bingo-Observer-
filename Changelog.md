1. Problemas encontrados
1. Responsabilidade Única (SRP)
.Sorteio administra as bolas, os observadores e as notificações.
.jogar() controla o andamento do jogo e também apresenta todas as informações no
terminal.
.A apresentação pode ser separada das regras do bingo.
2. Aberto/Fechado (OCP)
O sorteio está diretamente relacionado à implementação da lista de bolas. Se futuramente
quisermos utilizar outra fonte de números, será necessário modificar a classe.
3. Substituição de Liskov (LSP)
Não encontrei uma violação direta. O jogador implementa Observer e fornece o método
update() esperado. Esse princípio deve ser preservado.
4. Segregação de Interfaces (ISP)
A interface Observer está adequada: exige somente o comportamento necessário para
receber notificações. Não precisa ser dividida.
5. Inversão de Dependência (DIP)
A classe Sorteio não recebe uma abstração para fornecer os números. Isso dificulta substituir
a forma de sorteio e testar o comportamento isoladamente.
Também encontrei dois problemas de funcionamento:
.notificar() é chamado duas vezes em sortear().
.A urna utiliza números de 1 a 100, mas os jogadores recebem cartelas com números de
1 a 75. Isso deixa 25 números impossíveis de serem marcados.

2. Refatoração realizada
Principais mudanças:
.Separei a apresentação do terminal da lógica do jogo.
.Criei FonteNumeros para permitir diferentes implementações de sorteio.
.Criei Urna para concentrar a responsabilidade de fornecer números.
.Fiz Sorteio receber a fonte de números pelo construtor.
.Corrigi a notificação duplicada.
.Padronizei o limite numérico da urna e das cartelas.
.Adicionei validações para impedir cartelas com quantidades inválidas.
.Tornei Marcacao e Rodada imutáveis com frozen=True.
.Mantive o padrão Observer.

4. Relação entre as alterações e o SOLID
Alteração Princípio Justificativa
Separação de JogoBingo
e ApresentadorConsole
SRP
Cada classe passou a ter uma
responsabilidade específica.
Criação de Urna e
FonteNumeros
SRP e OCP
A geração dos números foi separada e
novas fontes podem ser adicionadas sem
modificar Sorteio.
Injeção de FonteNumeros
em Sorteio
DIP
A classe passou a depender de uma
abstração, não de uma implementação
específica.
Manutenção do contrato
Observer
ISP
A interface continua exigindo apenas o
método necessário.
Implementação de
FonteNumeros por Urna
LSP
A implementação concreta respeita o
contrato definido pela abstração.
Imutabilidade de Marcacao
e Rodada
Boa prática
complementar
Evita alterações acidentais nos dados das
rodadas.
