"""
Algoritmo Genético para resolver o Desafio de Einstein
Disciplina: Inteligência Artificial
Prof. Tiago Bonini Borchartt

Este programa implementa um algoritmo genético para resolver o famoso
Desafio de Einstein, um quebra-cabeça lógico que envolve 5 casas,
5 nacionalidades, 5 bebidas, 5 cigarros e 5 animais.
"""

import random

# Definição dos atributos possíveis para cada casa
ATTRS = {
    "cor": ["Amarela", "Azul", "Branca", "Verde", "Vermelha"],
    "nacional": ["Norueguês", "Dinamarquês", "Inglês", "Sueco", "Alemão"],
    "bebida": ["Água", "Chá", "Café", "Cerveja", "Leite"],
    "cigarro": ["Dunhill", "Blends", "BlueMaster", "Pall Mall", "Prince"],
    "animal": ["Gatos", "Cavalos", "Pássaros", "Peixes", "Cachorros"],
}
ATTR_KEYS = list(ATTRS)


def random_chrom():
    """Gera um cromossomo aleatório representando uma configuração das 5 casas."""
    cols = [random.sample(ATTRS[k], 5) for k in ATTR_KEYS]
    return list(zip(*cols))


def mutate(chrom):
    """
    Operação de mutação: troca atributos entre duas casas com probabilidade de 5%.
    """
    if random.random() > 0.05:  # Taxa de mutação: 5%
        return chrom
    i, j = random.sample(range(5), 2)  # Seleciona duas casas aleatórias
    col = random.randrange(5)  # Seleciona um atributo aleatório
    chrom = chrom[:]  # Cria uma cópia
    c1, c2 = list(chrom[i]), list(chrom[j])
    c1[col], c2[col] = c2[col], c1[col]  # Troca o atributo entre as casas
    chrom[i], chrom[j] = tuple(c1), tuple(c2)
    return chrom


def crossover(p1, p2):
    """
    Operação de crossover: combina dois pais para gerar dois filhos.
    Taxa de crossover: 80%
    """
    if random.random() > 0.8:
        return p1, p2
    point = random.randint(1, 4)  # Ponto de corte aleatório
    return p1[:point] + p2[point:], p2[:point] + p1[point:]


# ---- Avaliação --------------------------------------------------------------
def fitness(chrom):
    return sum(r(chrom) for r in RULES)


# ---------- utilitário ------------
def vizinhos(i: int) -> list[int]:
    """Índices das casas vizinhas válidas (à esquerda e à direita)."""
    return [j for j in (i - 1, i + 1) if 0 <= j < 5]


# ---------- regras 1‒15 -----------
def r1(h):  # 1. Norueguês vive na 1ª casa.
    return h[0][1] == "Norueguês"


def r2(h):  # 2. Inglês vive na casa Vermelha.
    return any(cor == "Vermelha" and nat == "Inglês" for cor, nat, *_ in h)


def r3(h):  # 3. Sueco tem Cachorros.
    return any(nat == "Sueco" and animal == "Cachorros" for _, nat, _, _, animal in h)


def r4(h):  # 4. Dinamarquês bebe Chá.
    return any(nat == "Dinamarquês" and bebida == "Chá" for _, nat, bebida, _, _ in h)


def r5(h):  # 5. Casa Verde fica imediatamente à esquerda da Branca.
    idx_verde = next((i for i, (cor, *_) in enumerate(h) if cor == "Verde"), -1)
    idx_branca = next((i for i, (cor, *_) in enumerate(h) if cor == "Branca"), -1)
    return idx_verde != -1 and idx_branca == idx_verde + 1


def r6(h):  # 6. Morador da casa Verde bebe Café.
    return any(cor == "Verde" and bebida == "Café" for cor, _, bebida, _, _ in h)


def r7(h):  # 7. Quem fuma Pall Mall cria Pássaros.
    return any(
        cigarro == "Pall Mall" and animal == "Pássaros"
        for _, _, _, cigarro, animal in h
    )


def r8(h):  # 8. Casa Amarela → Dunhill.
    return any(cor == "Amarela" and cigarro == "Dunhill" for cor, _, _, cigarro, _ in h)


def r9(h):  # 9. Casa do meio bebe Leite.
    return h[2][2] == "Leite"


def r10(h):  # 10. Fuma Blends ↔ vizinho que tem Gatos.
    for i, (_, _, _, cigarro, _) in enumerate(h):
        if cigarro == "Blends" and any(h[j][4] == "Gatos" for j in vizinhos(i)):
            return True
    return False


def r11(h):  # 11. Tem Cavalos ↔ vizinho que fuma Dunhill.
    for i, (_, _, _, _, animal) in enumerate(h):
        if animal == "Cavalos" and any(h[j][3] == "Dunhill" for j in vizinhos(i)):
            return True
    return False


def r12(h):  # 12. Fuma BlueMaster → bebe Cerveja.
    return any(
        cigarro == "BlueMaster" and bebida == "Cerveja"
        for _, _, bebida, cigarro, _ in h
    )


def r13(h):  # 13. Alemão fuma Prince.
    return any(nat == "Alemão" and cigarro == "Prince" for _, nat, _, cigarro, _ in h)


def r14(h):  # 14. Norueguês ↔ vizinho da casa Azul.
    idx_nor = next((i for i, (_, nat, *_) in enumerate(h) if nat == "Norueguês"), -1)
    return idx_nor != -1 and any(h[j][0] == "Azul" for j in vizinhos(idx_nor))


def r15(h):  # 15. Fuma Blends ↔ vizinho que bebe Água.
    for i, (_, _, _, cigarro, _) in enumerate(h):
        if cigarro == "Blends" and any(h[j][2] == "Água" for j in vizinhos(i)):
            return True
    return False


RULES = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15]

# Algoritmo Genético para resolver o Desafio de Einstein
print("🧬 Iniciando Algoritmo Genético para o Desafio de Einstein...")

POP = [random_chrom() for _ in range(500)]
print(f"População inicial: {len(POP)} indivíduos")
print("Procurando solução...\n")

generation = 0
while True:
    POP.sort(key=fitness, reverse=True)
    best = POP[0]
    best_fitness = fitness(best)

    # Mostrar progresso a cada 100 gerações
    if generation % 100 == 0:
        print(f"Geração {generation}: Melhor fitness = {best_fitness}/15")

    if best_fitness == 15:
        break
    nxt = POP[:2]
    fsum = sum(fitness(c) for c in POP)
    pick = lambda: random.choices(POP, weights=[fitness(c) for c in POP])[0]
    while len(nxt) < 500:
        p1, p2 = pick(), pick()
        c1, c2 = crossover(p1, p2)
        nxt.extend([mutate(c1), mutate(c2)])
    for _ in range(2):
        nxt[random.randrange(500)] = random_chrom()
    POP, generation = nxt[:500], generation + 1

print(f"Solução encontrada na geração {generation}:")
print(f"Fitness: {fitness(best)}/15 regras satisfeitas\n")

# Formatação melhorada da solução
print("=" * 80)
print("                    SOLUÇÃO DO DESAFIO DE EINSTEIN")
print("=" * 80)
for idx, casa in enumerate(best, 1):
    cor, nacionalidade, bebida, cigarro, animal = casa
    print(
        f"Casa {idx}: {cor:10} | {nacionalidade:12} | {bebida:8} | {cigarro:12} | {animal}"
    )
print("=" * 80)

# Verificar quem tem peixes (a resposta do desafio)
for idx, casa in enumerate(best, 1):
    if casa[4] == "Peixes":
        print(f"\n🐟 Resposta: O {casa[1]} (Casa {idx}) tem Peixes!")
        break
