"""
Regras do Desafio de Einstein
Este módulo contém as 15 regras do desafio e funções auxiliares.
"""


# encontra os vizinhos de uma casa
def vizinhos(i: int) -> list[int]:
    return [j for j in (i - 1, i + 1) if 0 <= j < 5]


# ---- AS 15 REGRAS DO DESAFIO DE EINSTEIN --------------------------------
def r1(h):  # O Norueguês vive na primeira casa
    return h[0][1] == "Norueguês"


def r2(h):  # O Inglês vive na casa Vermelha
    return any(cor == "Vermelha" and nat == "Inglês" for cor, nat, *_ in h)


def r3(h):  # O Sueco tem Cachorros
    return any(nat == "Sueco" and animal == "Cachorros" for _, nat, _, _, animal in h)


def r4(h):  # O Dinamarquês bebe Chá
    return any(nat == "Dinamarquês" and bebida == "Chá" for _, nat, bebida, _, _ in h)


def r5(h):  # A casa Verde fica do lado esquerdo da casa Branca
    idx_verde = next((i for i, (cor, *_) in enumerate(h) if cor == "Verde"), -1)
    idx_branca = next((i for i, (cor, *_) in enumerate(h) if cor == "Branca"), -1)
    return idx_verde != -1 and idx_branca == idx_verde + 1


def r6(h):  # O homem que vive na casa Verde bebe Café
    return any(cor == "Verde" and bebida == "Café" for cor, _, bebida, _, _ in h)


def r7(h):  # O homem que fuma Pall Mall cria Pássaros
    return any(
        cigarro == "Pall Mall" and animal == "Pássaros"
        for _, _, _, cigarro, animal in h
    )


def r8(h):  # O homem que vive na casa Amarela fuma Dunhill
    return any(cor == "Amarela" and cigarro == "Dunhill" for cor, _, _, cigarro, _ in h)


def r9(h):  # O homem que vive na casa do meio bebe Leite
    return h[2][2] == "Leite"


def r10(h):  # O homem que fuma Blends vive ao lado do que tem Gatos
    for i, (_, _, _, cigarro, _) in enumerate(h):
        if cigarro == "Blends" and any(h[j][4] == "Gatos" for j in vizinhos(i)):
            return True
    return False


def r11(h):  # O homem que cria Cavalos vive ao lado do que fuma Dunhill
    for i, (_, _, _, _, animal) in enumerate(h):
        if animal == "Cavalos" and any(h[j][3] == "Dunhill" for j in vizinhos(i)):
            return True
    return False


def r12(h):  # O homem que fuma BlueMaster bebe Cerveja
    return any(
        cigarro == "BlueMaster" and bebida == "Cerveja"
        for _, _, bebida, cigarro, _ in h
    )


def r13(h):  # O Alemão fuma Prince
    return any(nat == "Alemão" and cigarro == "Prince" for _, nat, _, cigarro, _ in h)


def r14(h):  # O Norueguês vive ao lado da casa Azul
    idx_nor = next((i for i, (_, nat, *_) in enumerate(h) if nat == "Norueguês"), -1)
    return idx_nor != -1 and any(h[j][0] == "Azul" for j in vizinhos(idx_nor))


def r15(h):  # O homem que fuma Blends é vizinho do que bebe Água
    for i, (_, _, _, cigarro, _) in enumerate(h):
        if cigarro == "Blends" and any(h[j][2] == "Água" for j in vizinhos(i)):
            return True
    return False


REGRAS = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15]

# Pesos para regras críticas
PESOS_REGRAS = {
    0: 1.0,  # r1 - simples
    1: 1.0,  # r2 - simples
    2: 1.0,  # r3 - simples
    3: 1.0,  # r4 - simples
    4: 1.5,  # r5 - sequencial (crítica)
    5: 1.0,  # r6 - simples
    6: 1.0,  # r7 - simples
    7: 1.0,  # r8 - simples
    8: 1.0,  # r9 - simples (posição fixa)
    9: 2.0,  # r10 - vizinhança (crítica)
    10: 2.0,  # r11 - vizinhança (crítica)
    11: 1.0,  # r12 - simples
    12: 1.0,  # r13 - simples
    13: 2.0,  # r14 - vizinhança (crítica)
    14: 2.0,  # r15 - vizinhança (crítica)
}


# fitness simples para contagem de regras satisfeitas
def fitness(cromossomo):
    return sum(regra(cromossomo) for regra in REGRAS)


# fitness ponderado para regras críticas
def fitness_ponderado(cromossomo):

    total = 0.0
    for i, regra in enumerate(REGRAS):
        if regra(cromossomo):
            total += PESOS_REGRAS[i]
    return total


# retorna os índices das regras que não estão sendo satisfeitas
def obter_regras_faltantes(cromossomo):
    faltantes = []
    for i, regra in enumerate(REGRAS):
        if not regra(cromossomo):
            faltantes.append(i + 1)
    return faltantes


# relatório do fitness
def relatorio_detalhado_fitness(cromossomo):
    satisfeitas = []
    faltantes = []

    for i, regra in enumerate(REGRAS):
        if regra(cromossomo):
            satisfeitas.append(i + 1)
        else:
            faltantes.append(i + 1)

    return {
        "score": len(satisfeitas),
        "satisfied": satisfeitas,
        "missing": faltantes,
        "weighted_score": fitness_ponderado(cromossomo),
    }


# pontuação parcial para análise
def pontuacoes_parciais_fitness(cromossomo):
    # agrupa regras por tipo
    regras_simples = [0, 1, 2, 3, 5, 6, 7, 8, 11, 12]  # Regras simples
    regras_posicao = [0, 8]  # Regras de posição fixa
    regras_sequencia = [4]  # Regras sequenciais
    regras_vizinhanca = [9, 10, 13, 14]  # Regras de vizinhança

    pontuacoes = {}

    for categoria, indices_regras in [
        ("simples", regras_simples),
        ("posicao", regras_posicao),
        ("sequencia", regras_sequencia),
        ("vizinhanca", regras_vizinhanca),
    ]:
        satisfeitas = sum(1 for i in indices_regras if REGRAS[i](cromossomo))
        total = len(indices_regras)
        pontuacoes[categoria] = f"{satisfeitas}/{total}"

    return pontuacoes
