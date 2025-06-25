"""
Algoritmo Genético para o Desafio de Einstein
Este módulo contém as funções do algoritmo genético.
"""

import random
from typing import List, Tuple

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


def mutate(chrom, mutation_rate):
    """Operação de mutação: troca atributos entre duas casas aleatórias"""
    if random.random() > mutation_rate:
        return chrom

    i, j = random.sample(range(5), 2)  # Duas casas aleatórias
    col = random.randrange(5)  # Um atributo aleatório
    chrom = chrom[:]  # Copia
    c1, c2 = list(chrom[i]), list(chrom[j])
    c1[col], c2[col] = c2[col], c1[col]  # Troca
    chrom[i], chrom[j] = tuple(c1), tuple(c2)
    return chrom


def crossover(p1, p2, crossover_rate):
    """Operação de crossover: combina dois pais em um ponto aleatório"""
    if random.random() > crossover_rate:
        return p1, p2
    point = random.randint(1, 4)
    return p1[:point] + p2[point:], p2[:point] + p1[point:]


def roulette_selection(population: List, fitness_values: List[int]):
    """Método da roleta para seleção de pais (REQUISITO OBRIGATÓRIO)"""
    total_fitness = sum(fitness_values)
    if total_fitness == 0:
        return random.choice(population)

    r = random.uniform(0, total_fitness)
    cumulative = 0
    for i, fitness_val in enumerate(fitness_values):
        cumulative += fitness_val
        if cumulative >= r:
            return population[i]
    return population[-1]


def hybrid_selection(population: List, fitness_values: List[int], use_tournament=True):
    """Seleção híbrida: usa torneio para altos fitness, roleta para baixos"""
    if use_tournament and max(fitness_values) >= 12:
        # Torneio para cromossomos com alta fitness
        tournament_size = 5
        tournament_indices = random.sample(
            range(len(population)), min(tournament_size, len(population))
        )
        best_idx = max(tournament_indices, key=lambda i: fitness_values[i])
        return population[best_idx]
    else:
        # Roleta para diversidade
        return roulette_selection(population, fitness_values)


def show_solution(chrom):
    """Mostra a solução de forma clara para apresentação"""
    print("\n" + "=" * 70)
    print("                    SOLUÇÃO ENCONTRADA")
    print("=" * 70)
    print("Casa | Cor        | Nacionalidade | Bebida   | Cigarro      | Animal")
    print("-" * 70)
    for i, casa in enumerate(chrom, 1):
        cor, nacionalidade, bebida, cigarro, animal = casa
        print(
            f"  {i}  | {cor:10} | {nacionalidade:12} | {bebida:8} | {cigarro:12} | {animal}"
        )
    print("=" * 70)
