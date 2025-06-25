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

# Import das regras específicas para a função brute_force_rule5
from einstein_rules import (
    r1,
    r2,
    r3,
    r4,
    r5,
    r6,
    r7,
    r8,
    r9,
    r10,
    r11,
    r12,
    r13,
    r14,
    r15,
)


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


def tournament_selection(
    population: List, fitness_values: List[int], tournament_size: int = 7
):
    """Seleção por torneio - mais agressiva para convergência rápida"""
    if len(population) < tournament_size:
        tournament_size = len(population)

    tournament_indices = random.sample(range(len(population)), tournament_size)
    best_idx = max(tournament_indices, key=lambda i: fitness_values[i])
    return population[best_idx]


def hybrid_selection(population: List, fitness_values: List[int], use_tournament=True):
    """Seleção híbrida: usa torneio para altos fitness, roleta para baixos"""
    max_fitness = max(fitness_values) if fitness_values else 0

    if use_tournament and max_fitness >= 12:
        # Torneio agressivo para alta convergência
        tournament_size = min(7, len(population))
        if max_fitness >= 14:
            tournament_size = min(3, len(population))  # Mais seletivo para 14→15
        return tournament_selection(population, fitness_values, tournament_size)
    else:
        # Roleta para diversidade
        return roulette_selection(population, fitness_values)


def smart_mutate(chrom, mutation_rate, fitness_val):
    """Mutação inteligente baseada no fitness atual"""
    if random.random() > mutation_rate:
        return chrom

    # Para fitness alto (13+), mutação mais focada
    if fitness_val >= 13:
        # Múltiplas tentativas pequenas
        for _ in range(3):
            if random.random() < 0.7:
                chrom = mutate(chrom, 0.3)
    else:
        # Mutação normal
        chrom = mutate(chrom, 1.0)

    return chrom


def directed_mutate(chrom, missing_rules):
    """Mutação dirigida para tentar satisfazer regras específicas"""
    if not missing_rules or random.random() > 0.3:
        return chrom

    # Foca nas regras mais críticas (vizinhança)
    critical_rules = {10, 11, 14, 15}  # Regras de vizinhança

    if any(rule in critical_rules for rule in missing_rules):
        # Mutação mais agressiva para regras de vizinhança
        for _ in range(2):
            i, j = random.sample(range(5), 2)
            if abs(i - j) == 1:  # Casas vizinhas
                col = random.randrange(5)
                chrom = chrom[:]
                c1, c2 = list(chrom[i]), list(chrom[j])
                c1[col], c2[col] = c2[col], c1[col]
                chrom[i], chrom[j] = tuple(c1), tuple(c2)
                break

    return chrom


def local_search(chrom, fitness_func, max_iterations=20):
    """Busca local para refinar soluções de alto fitness"""
    current = chrom
    current_fitness = fitness_func(current)

    for _ in range(max_iterations):
        # Gera vizinhos trocando atributos
        neighbors = []

        for i in range(5):
            for j in range(i + 1, 5):
                for attr in range(5):
                    neighbor = [list(casa) for casa in current]
                    neighbor[i][attr], neighbor[j][attr] = (
                        neighbor[j][attr],
                        neighbor[i][attr],
                    )
                    neighbors.append([tuple(casa) for casa in neighbor])

        # Avalia vizinhos
        best_neighbor = None
        best_neighbor_fitness = current_fitness

        for neighbor in neighbors:
            neighbor_fitness = fitness_func(neighbor)
            if neighbor_fitness > best_neighbor_fitness:
                best_neighbor = neighbor
                best_neighbor_fitness = neighbor_fitness

        if best_neighbor is not None:
            current = best_neighbor
            current_fitness = best_neighbor_fitness
        else:
            break  # Máximo local encontrado

    return current


def advanced_crossover(p1, p2, crossover_rate):
    """Crossover mais sofisticado que preserva boas características"""
    if random.random() > crossover_rate:
        return p1, p2

    # Crossover uniforme com probabilidade de herdar cada casa
    c1, c2 = [], []

    for i in range(5):
        if random.random() < 0.5:
            c1.append(p1[i])
            c2.append(p2[i])
        else:
            c1.append(p2[i])
            c2.append(p1[i])

    # Garantir que não há duplicatas nos atributos
    c1 = repair_chromosome(c1)
    c2 = repair_chromosome(c2)

    return c1, c2


def repair_chromosome(chrom):
    """Repara um cromossomo garantindo que não há atributos duplicados"""
    chrom = [list(casa) for casa in chrom]

    for attr_idx in range(5):
        # Coleta valores únicos para este atributo
        values = [chrom[i][attr_idx] for i in range(5)]
        available = list(ATTRS[ATTR_KEYS[attr_idx]])

        # Remove duplicatas mantendo ordem
        seen = set()
        unique_values = []
        for val in values:
            if val not in seen:
                unique_values.append(val)
                seen.add(val)
                if val in available:
                    available.remove(val)

        # Preenche valores faltantes
        while len(unique_values) < 5:
            unique_values.append(available.pop(0))

        # Aplica de volta
        for i in range(5):
            chrom[i][attr_idx] = unique_values[i]

    return [tuple(casa) for casa in chrom]


def create_elite_offspring(elite_population, fitness_values, fitness_func):
    """Cria descendentes de alta qualidade a partir da elite"""
    offspring = []

    # Pega os melhores indivíduos
    best_indices = sorted(
        range(len(elite_population)), key=lambda i: fitness_values[i], reverse=True
    )

    elite_size = min(10, len(best_indices))
    elite = [elite_population[i] for i in best_indices[:elite_size]]

    # Crossover entre elite + busca local
    for _ in range(20):
        p1, p2 = random.sample(elite, 2)
        c1, c2 = advanced_crossover(p1, p2, 0.9)

        # Aplica busca local se fitness alto
        if fitness_func(c1) >= 13:
            c1 = local_search(c1, fitness_func, 5)
        if fitness_func(c2) >= 13:
            c2 = local_search(c2, fitness_func, 5)

        offspring.extend([c1, c2])

    return offspring


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


def specialized_rule5_mutate(chrom):
    """Mutação especializada para regra 5: Verde do lado esquerdo da Branca"""
    if random.random() > 0.6:  # 60% chance de aplicar
        return chrom

    chrom = [list(casa) for casa in chrom]

    # Encontra posições atuais de Verde e Branca
    verde_pos = -1
    branca_pos = -1

    for i, casa in enumerate(chrom):
        if casa[0] == "Verde":
            verde_pos = i
        elif casa[0] == "Branca":
            branca_pos = i

    # Se ambas foram encontradas
    if verde_pos != -1 and branca_pos != -1:
        # Tenta colocar Verde-Branca em sequência
        target_positions = [(0, 1), (1, 2), (2, 3), (3, 4)]  # Pares válidos
        target_pair = random.choice(target_positions)
        verde_target, branca_target = target_pair

        # Move Verde para posição target
        if verde_pos != verde_target:
            chrom[verde_pos][0], chrom[verde_target][0] = (
                chrom[verde_target][0],
                chrom[verde_pos][0],
            )

        # Move Branca para posição target + 1
        if branca_pos != branca_target:
            chrom[branca_pos][0], chrom[branca_target][0] = (
                chrom[branca_target][0],
                chrom[branca_pos][0],
            )

    return [tuple(casa) for casa in chrom]


def debug_rule5_status(chrom):
    """Debug detalhado da regra 5"""
    cores = [casa[0] for casa in chrom]
    verde_pos = cores.index("Verde") if "Verde" in cores else -1
    branca_pos = cores.index("Branca") if "Branca" in cores else -1

    status = {
        "cores_sequence": cores,
        "verde_pos": verde_pos,
        "branca_pos": branca_pos,
        "is_valid": verde_pos != -1 and branca_pos == verde_pos + 1,
        "difference": (
            branca_pos - verde_pos if verde_pos != -1 and branca_pos != -1 else None
        ),
    }

    return status


def intensive_rule5_repair(population, fitness_func):
    """Repara intensivamente cromossomos focando na regra 5"""
    repaired = []

    for chrom in population[:50]:  # Pega os 50 melhores
        if fitness_func(chrom) == 14:  # Se tá no 14/15
            # Tenta múltiplas reparações
            best_repair = chrom
            best_fitness = fitness_func(chrom)

            for attempt in range(20):  # 20 tentativas
                candidate = specialized_rule5_mutate(chrom)
                candidate_fitness = fitness_func(candidate)

                if candidate_fitness > best_fitness:
                    best_repair = candidate
                    best_fitness = candidate_fitness

                if best_fitness == 15:  # Achou!
                    break

            repaired.append(best_repair)
        else:
            repaired.append(chrom)

    return repaired


def brute_force_rule5(chrom, fitness_func):
    """Força bruta específica para resolver regra 5: tenta todas posições Verde-Branca"""
    if fitness_func(chrom) != 14:
        return chrom

    # Verifica se é a regra 5 que está faltando
    missing = [
        i
        for i, rule in enumerate(
            [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15]
        )
        if not rule(chrom)
    ]
    if len(missing) != 1 or missing[0] != 4:  # Regra 5 é índice 4
        return chrom

    best_candidate = chrom
    best_fitness = fitness_func(chrom)

    # Tenta todas as 4 posições possíveis para Verde-Branca
    valid_positions = [(0, 1), (1, 2), (2, 3), (3, 4)]

    for verde_pos, branca_pos in valid_positions:
        candidate = [list(casa) for casa in chrom]

        # Salva cores originais nessas posições
        original_verde = candidate[verde_pos][0]
        original_branca = candidate[branca_pos][0]

        # Encontra onde estão Verde e Branca atualmente
        current_verde_pos = -1
        current_branca_pos = -1
        for i, casa in enumerate(candidate):
            if casa[0] == "Verde":
                current_verde_pos = i
            elif casa[0] == "Branca":
                current_branca_pos = i

        if current_verde_pos != -1 and current_branca_pos != -1:
            # Faz as trocas
            # 1. Move Verde para verde_pos
            if current_verde_pos != verde_pos:
                candidate[current_verde_pos][0] = original_verde
                candidate[verde_pos][0] = "Verde"

            # 2. Move Branca para branca_pos
            if current_branca_pos != branca_pos and current_branca_pos != verde_pos:
                candidate[current_branca_pos][0] = original_branca
                candidate[branca_pos][0] = "Branca"
            elif current_branca_pos == verde_pos:  # Branca estava onde Verde vai
                candidate[branca_pos][0] = "Branca"

            # Converte de volta
            candidate_tuple = [tuple(casa) for casa in candidate]
            candidate_fitness = fitness_func(candidate_tuple)

            if candidate_fitness > best_fitness:
                best_candidate = candidate_tuple
                best_fitness = candidate_fitness

            if best_fitness == 15:  # Achou a solução!
                break

    return best_candidate


def analyze_chromosome_detailed(chrom, fitness_func):
    """Análise super detalhada de um cromossomo"""
    from einstein_rules import RULES, get_missing_rules, detailed_fitness_report

    analysis = {
        "chromosome": chrom,
        "fitness": fitness_func(chrom),
        "missing_rules": get_missing_rules(chrom),
        "rule_details": {},
        "attribute_conflicts": {},
        "position_analysis": {},
    }

    # Analisa cada regra individualmente
    for i, rule in enumerate(RULES):
        rule_name = f"R{i+1}"
        is_satisfied = rule(chrom)
        analysis["rule_details"][rule_name] = {
            "satisfied": is_satisfied,
            "description": get_rule_description(i + 1),
        }

    # Analisa conflitos por atributo
    for attr_idx, attr_name in enumerate(
        ["cor", "nacional", "bebida", "cigarro", "animal"]
    ):
        values = [chrom[i][attr_idx] for i in range(5)]
        analysis["attribute_conflicts"][attr_name] = {
            "values": values,
            "duplicates": len(values) != len(set(values)),
            "unique_count": len(set(values)),
        }

    # Análise posicional
    for i, casa in enumerate(chrom):
        analysis["position_analysis"][f"Casa_{i+1}"] = {
            "cor": casa[0],
            "nacional": casa[1],
            "bebida": casa[2],
            "cigarro": casa[3],
            "animal": casa[4],
        }

    return analysis


def get_rule_description(rule_num):
    """Retorna descrição da regra"""
    descriptions = {
        1: "Norueguês vive na primeira casa",
        2: "Inglês vive na casa Vermelha",
        3: "Sueco tem Cachorros",
        4: "Dinamarquês bebe Chá",
        5: "Casa Verde fica do lado esquerdo da casa Branca",
        6: "Homem da casa Verde bebe Café",
        7: "Homem que fuma Pall Mall cria Pássaros",
        8: "Homem da casa Amarela fuma Dunhill",
        9: "Homem da casa do meio bebe Leite",
        10: "Homem que fuma Blends vive ao lado do que tem Gatos",
        11: "Homem que cria Cavalos vive ao lado do que fuma Dunhill",
        12: "Homem que fuma BlueMaster bebe Cerveja",
        13: "Alemão fuma Prince",
        14: "Norueguês vive ao lado da casa Azul",
        15: "Homem que fuma Blends é vizinho do que bebe Água",
    }
    return descriptions.get(rule_num, f"Regra {rule_num}")


def debug_specific_rule(chrom, rule_num):
    """Debug específico para uma regra"""
    from einstein_rules import RULES

    if rule_num < 1 or rule_num > 15:
        return "Regra inválida"

    rule = RULES[rule_num - 1]
    is_satisfied = rule(chrom)

    debug_info = {
        "rule_number": rule_num,
        "description": get_rule_description(rule_num),
        "satisfied": is_satisfied,
        "detailed_analysis": {},
    }

    # Análises específicas por regra
    if rule_num == 1:  # Norueguês na primeira casa
        debug_info["detailed_analysis"] = {
            "primeira_casa_nacional": chrom[0][1],
            "is_noruegues": chrom[0][1] == "Norueguês",
        }

    elif rule_num == 2:  # Inglês na casa vermelha
        ingles_pos = next(
            (i for i, casa in enumerate(chrom) if casa[1] == "Inglês"), -1
        )
        vermelha_pos = next(
            (i for i, casa in enumerate(chrom) if casa[0] == "Vermelha"), -1
        )
        debug_info["detailed_analysis"] = {
            "ingles_posicao": ingles_pos,
            "vermelha_posicao": vermelha_pos,
            "mesmo_local": ingles_pos == vermelha_pos and ingles_pos != -1,
        }

    elif rule_num == 5:  # Verde-Branca sequencial
        verde_pos = next((i for i, casa in enumerate(chrom) if casa[0] == "Verde"), -1)
        branca_pos = next(
            (i for i, casa in enumerate(chrom) if casa[0] == "Branca"), -1
        )
        debug_info["detailed_analysis"] = {
            "verde_posicao": verde_pos,
            "branca_posicao": branca_pos,
            "diferenca": (
                branca_pos - verde_pos if verde_pos != -1 and branca_pos != -1 else None
            ),
            "sequencial_correto": verde_pos != -1 and branca_pos == verde_pos + 1,
        }

    elif rule_num == 8:  # Amarela-Dunhill
        amarela_pos = next(
            (i for i, casa in enumerate(chrom) if casa[0] == "Amarela"), -1
        )
        dunhill_pos = next(
            (i for i, casa in enumerate(chrom) if casa[3] == "Dunhill"), -1
        )
        debug_info["detailed_analysis"] = {
            "amarela_posicao": amarela_pos,
            "dunhill_posicao": dunhill_pos,
            "mesmo_local": amarela_pos == dunhill_pos and amarela_pos != -1,
        }

    elif rule_num == 14:  # Norueguês-Azul vizinhos
        noruegues_pos = next(
            (i for i, casa in enumerate(chrom) if casa[1] == "Norueguês"), -1
        )
        azul_pos = next((i for i, casa in enumerate(chrom) if casa[0] == "Azul"), -1)
        sao_vizinhos = False
        if noruegues_pos != -1 and azul_pos != -1:
            sao_vizinhos = abs(noruegues_pos - azul_pos) == 1

        debug_info["detailed_analysis"] = {
            "noruegues_posicao": noruegues_pos,
            "azul_posicao": azul_pos,
            "diferenca": (
                abs(noruegues_pos - azul_pos)
                if noruegues_pos != -1 and azul_pos != -1
                else None
            ),
            "sao_vizinhos": sao_vizinhos,
        }

    return debug_info


def print_chromosome_visual(chrom):
    """Imprime cromossomo de forma visual para debug"""
    print("\n🏠 CONFIGURAÇÃO ATUAL:")
    print("Casa | Cor        | Nacionalidade | Bebida   | Cigarro      | Animal")
    print("-" * 70)
    for i, casa in enumerate(chrom, 1):
        cor, nacionalidade, bebida, cigarro, animal = casa
        print(
            f"  {i}  | {cor:10} | {nacionalidade:12} | {bebida:8} | {cigarro:12} | {animal}"
        )
    print("-" * 70)


def deep_population_analysis(population, fitness_func, top_n=5):
    """Análise profunda da população"""
    print(f"\n🔬 ANÁLISE PROFUNDA DA POPULAÇÃO (Top {top_n}):")
    print("=" * 80)

    # Ordena por fitness
    pop_with_fitness = [(chrom, fitness_func(chrom)) for chrom in population]
    pop_with_fitness.sort(key=lambda x: x[1], reverse=True)

    for i, (chrom, fit) in enumerate(pop_with_fitness[:top_n]):
        print(f"\n🏆 INDIVÍDUO #{i+1} - FITNESS: {fit}/15")
        print_chromosome_visual(chrom)

        if fit == 14:  # Análise especial para fitness 14
            missing = []
            from einstein_rules import RULES

            for rule_idx, rule in enumerate(RULES):
                if not rule(chrom):
                    missing.append(rule_idx + 1)

            print(f"❌ REGRA FALTANTE: {missing[0]}")
            debug_info = debug_specific_rule(chrom, missing[0])
            print(f"📋 {debug_info['description']}")
            print(f"🔍 Análise: {debug_info['detailed_analysis']}")

        print("-" * 80)


def controlled_rule5_fix(chrom, fitness_func):
    """Quebra controlada: temporariamente quebra outras regras para resolver R5"""
    if fitness_func(chrom) != 14:
        return chrom

    # Verifica se é exatamente a regra 5 que falta
    from einstein_rules import RULES

    missing = [i for i, rule in enumerate(RULES) if not rule(chrom)]
    if len(missing) != 1 or missing[0] != 4:  # R5 é índice 4
        return chrom

    best_candidate = chrom
    best_fitness = 14

    # Tenta todas as configurações Verde-Branca possíveis
    valid_pairs = [(0, 1), (1, 2), (2, 3), (3, 4)]

    for verde_target, branca_target in valid_pairs:
        # Cria uma cópia editável
        candidate = [list(casa) for casa in chrom]

        # FORÇA Verde e Branca nas posições corretas
        # Primeiro, encontra onde estão atualmente
        verde_atual = next(i for i, casa in enumerate(candidate) if casa[0] == "Verde")
        branca_atual = next(
            i for i, casa in enumerate(candidate) if casa[0] == "Branca"
        )

        # ESTRATÉGIA 1: Troca direta de cores
        if verde_atual != verde_target:
            # Troca Verde com a cor na posição target
            cor_target = candidate[verde_target][0]
            candidate[verde_atual][0] = cor_target
            candidate[verde_target][0] = "Verde"

        if branca_atual != branca_target and branca_atual != verde_target:
            # Troca Branca com a cor na posição target
            cor_target = candidate[branca_target][0]
            candidate[branca_atual][0] = cor_target
            candidate[branca_target][0] = "Branca"
        elif branca_atual == verde_target:
            # Caso especial: Branca estava onde Verde foi
            candidate[branca_target][0] = "Branca"

        # Converte de volta e testa
        candidate_tuple = [tuple(casa) for casa in candidate]
        candidate_fitness = fitness_func(candidate_tuple)

        if candidate_fitness > best_fitness:
            best_candidate = candidate_tuple
            best_fitness = candidate_fitness

        if candidate_fitness == 15:
            return candidate_tuple

        # ESTRATÉGIA 2: Troca atributos completos entre casas
        candidate2 = [list(casa) for casa in chrom]

        # Salva as casas originais
        casa_verde = list(candidate2[verde_atual])
        casa_branca = list(candidate2[branca_atual])
        casa_target_verde = list(candidate2[verde_target])
        casa_target_branca = list(candidate2[branca_target])

        # Força Verde na posição target mantendo outros atributos da casa target
        candidate2[verde_target] = casa_verde[:]
        candidate2[verde_target][0] = "Verde"  # Força cor Verde

        # Força Branca na posição target mantendo outros atributos da casa target
        if branca_target != verde_target:
            candidate2[branca_target] = casa_branca[:]
            candidate2[branca_target][0] = "Branca"  # Força cor Branca

            # Redistribui as casas originais
            candidate2[verde_atual] = casa_target_verde[:]
            candidate2[branca_atual] = casa_target_branca[:]
        else:
            # Caso especial quando verde_target == branca_target (impossível mas safe)
            continue

        # Testa estratégia 2
        candidate2_tuple = [tuple(casa) for casa in candidate2]
        candidate2_fitness = fitness_func(candidate2_tuple)

        if candidate2_fitness > best_fitness:
            best_candidate = candidate2_tuple
            best_fitness = candidate2_fitness

        if candidate2_fitness == 15:
            return candidate2_tuple

    return best_candidate


def emergency_rule5_solver(population, fitness_func):
    """Solucionador de emergência para regra 5 - força a solução"""
    solutions = []

    for chrom in population[:100]:  # Testa os 100 melhores
        if fitness_func(chrom) == 14:
            # Tenta quebra controlada
            fixed = controlled_rule5_fix(chrom, fitness_func)
            solutions.append(fixed)

            if fitness_func(fixed) == 15:
                return [fixed]  # ACHOU!

    return solutions


def ultra_debug_mutation_failure(chrom, fitness_func, missing_rule_num, num_tests=100):
    """Debug ultra-específico: por que as mutações não resolvem a última regra?"""
    print(f"\n🔬 ULTRA DEBUG - REGRA {missing_rule_num} TRAVADA")

    original_fitness = fitness_func(chrom)
    print(f"   📊 Fitness original: {original_fitness}/15")

    # Testa diferentes tipos de mutação
    results = {
        "smart_mutate_low": 0,
        "smart_mutate_high": 0,
        "directed_mutate": 0,
        "normal_mutate": 0,
        "local_search": 0,
        "fitness_improved": 0,
        "fitness_same": 0,
        "fitness_worse": 0,
    }

    best_found = chrom
    best_fitness = original_fitness

    for i in range(num_tests):
        # Teste 1: Smart mutate baixa taxa
        candidate1 = smart_mutate(chrom, 0.2, original_fitness)
        fit1 = fitness_func(candidate1)
        if fit1 != original_fitness:
            results["smart_mutate_low"] += 1

        # Teste 2: Smart mutate alta taxa
        candidate2 = smart_mutate(chrom, 0.8, original_fitness)
        fit2 = fitness_func(candidate2)
        if fit2 != original_fitness:
            results["smart_mutate_high"] += 1

        # Teste 3: Directed mutate
        candidate3 = directed_mutate(chrom, [missing_rule_num])
        fit3 = fitness_func(candidate3)
        if fit3 != original_fitness:
            results["directed_mutate"] += 1

        # Teste 4: Mutação normal
        candidate4 = mutate(chrom, 0.5)
        fit4 = fitness_func(candidate4)
        if fit4 != original_fitness:
            results["normal_mutate"] += 1

        # Teste 5: Local search
        candidate5 = local_search(chrom, fitness_func, 5)
        fit5 = fitness_func(candidate5)
        if fit5 != original_fitness:
            results["local_search"] += 1

        # Análise geral dos resultados
        all_fits = [fit1, fit2, fit3, fit4, fit5]
        for f in all_fits:
            if f > original_fitness:
                results["fitness_improved"] += 1
                if f > best_fitness:
                    best_fitness = f
                    # Encontra qual candidato foi o melhor
                    if f == fit1:
                        best_found = candidate1
                    elif f == fit2:
                        best_found = candidate2
                    elif f == fit3:
                        best_found = candidate3
                    elif f == fit4:
                        best_found = candidate4
                    elif f == fit5:
                        best_found = candidate5
            elif f == original_fitness:
                results["fitness_same"] += 1
            else:
                results["fitness_worse"] += 1

    print(f"   📈 Resultados de {num_tests} testes:")
    print(f"      🎲 Smart mutate baixa: {results['smart_mutate_low']} alterações")
    print(f"      🎲 Smart mutate alta: {results['smart_mutate_high']} alterações")
    print(f"      🎯 Directed mutate: {results['directed_mutate']} alterações")
    print(f"      🔄 Normal mutate: {results['normal_mutate']} alterações")
    print(f"      🔍 Local search: {results['local_search']} alterações")
    print(f"   📊 Fitness changes:")
    print(f"      ✅ Melhorou: {results['fitness_improved']}")
    print(f"      ↔️ Igual: {results['fitness_same']}")
    print(f"      ❌ Piorou: {results['fitness_worse']}")
    print(f"   🏆 Melhor encontrado: {best_fitness}/15")

    if best_fitness == 15:
        print(f"   🎉 SOLUÇÃO ENCONTRADA NO DEBUG!")
        return best_found
    elif best_fitness > original_fitness:
        print(f"   📈 Melhoria encontrada: {original_fitness} → {best_fitness}")
        return best_found
    else:
        print(f"   ⚠️ Nenhuma melhoria em {num_tests} tentativas!")

        # Debug específico da regra problemática
        print(f"\n   🔍 ANÁLISE ESPECÍFICA DA REGRA {missing_rule_num}:")
        rule_debug = debug_specific_rule(chrom, missing_rule_num)
        print(f"      📋 {rule_debug['description']}")
        print(f"      🔍 {rule_debug['detailed_analysis']}")

        # Análise de "proteção" - que outras regras impedem mudanças
        print(
            f"\n   🛡️ ANÁLISE DE PROTEÇÃO - Regras que podem estar 'protegendo' a configuração:"
        )
        from einstein_rules import RULES

        for i, rule in enumerate(RULES):
            if (
                rule(chrom) and i != missing_rule_num - 1
            ):  # Regras satisfeitas (exceto a faltante)
                rule_desc = get_rule_description(i + 1)
                print(f"      ✅ R{i+1}: {rule_desc}")

        return chrom


def analyze_population_stagnation(population, fitness_func):
    """Analisa se a população está estagnada (todos muito similares)"""
    print(f"\n🔬 ANÁLISE DE ESTAGNAÇÃO DA POPULAÇÃO")

    # Conta fitness distribution
    fitness_dist = {}
    for chrom in population:
        f = fitness_func(chrom)
        fitness_dist[f] = fitness_dist.get(f, 0) + 1

    print(f"   📊 Distribuição de fitness:")
    for f in sorted(fitness_dist.keys(), reverse=True):
        count = fitness_dist[f]
        percentage = (count / len(population)) * 100
        print(f"      {f:2d}/15: {count:4d} indivíduos ({percentage:5.1f}%)")

    # Analisa diversidade real nas soluções 14/15
    solutions_14 = [chrom for chrom in population if fitness_func(chrom) == 14]
    if solutions_14:
        print(f"\n   🎯 Análise das {len(solutions_14)} soluções 14/15:")

        # Diferentes regras faltantes
        missing_rules = {}
        from einstein_rules import get_missing_rules  # Import aqui

        for chrom in solutions_14:
            missing = get_missing_rules(chrom)[0]
            missing_rules[missing] = missing_rules.get(missing, 0) + 1

        print(f"      🎲 Regras faltantes: {missing_rules}")

        # Diversidade real (configurações únicas)
        unique_configs = set(str(chrom) for chrom in solutions_14)
        diversity_percentage = (len(unique_configs) / len(solutions_14)) * 100
        print(
            f"      🧬 Configurações únicas: {len(unique_configs)}/{len(solutions_14)} ({diversity_percentage:.1f}%)"
        )

        if diversity_percentage < 10:
            print(f"      ⚠️ PROBLEMA CRÍTICO: População 14/15 altamente convergente!")
            print(f"      🔄 Todas as soluções são praticamente idênticas")
            return True  # Estagnada

    return False  # Não estagnada


def diversity_explosion(best_chrom, population_size, fitness_func):
    """EXPLOSÃO DE DIVERSIDADE: Força variações massivas da melhor solução"""
    print(f"\n💥 EXECUTANDO EXPLOSÃO DE DIVERSIDADE")
    print(f"   🎯 Base: melhor cromossomo atual")
    print(f"   🧬 Gerando {population_size} variações forçadas")

    new_population = []
    base_fitness = fitness_func(best_chrom)

    # Mantém o melhor
    new_population.append(best_chrom)
    print(f"   ✅ Mantendo melhor: fitness {base_fitness}")

    # Estratégia 1: Mutações progressivamente mais agressivas (30%)
    aggressive_count = int(population_size * 0.3)
    print(f"   🎲 Criando {aggressive_count} mutações agressivas...")
    for i in range(aggressive_count):
        candidate = best_chrom

        # Intensidade cresce com o índice
        intensity = 1 + (i / aggressive_count) * 4  # 1x a 5x

        for _ in range(int(intensity)):
            candidate = mutate(candidate, 0.8)  # 80% chance de mutação

        new_population.append(candidate)

    # Estratégia 2: Permutações forçadas de atributos específicos (40%)
    permutation_count = int(population_size * 0.4)
    print(f"   🔄 Criando {permutation_count} permutações forçadas...")
    for i in range(permutation_count):
        candidate = [list(casa) for casa in best_chrom]

        # Força permutações em atributos específicos
        attr_idx = i % 5  # Cicla entre os 5 atributos

        # Embaralha completamente um atributo
        values = [candidate[j][attr_idx] for j in range(5)]
        random.shuffle(values)
        for j in range(5):
            candidate[j][attr_idx] = values[j]

        new_population.append([tuple(casa) for casa in candidate])

    # Estratégia 3: Hibridização com soluções aleatórias (20%)
    hybrid_count = int(population_size * 0.2)
    print(f"   🧬 Criando {hybrid_count} hibridizações...")
    for i in range(hybrid_count):
        # Cria solução aleatória
        random_solution = random_chrom()

        # Hibridiza: algumas casas do melhor, outras aleatórias
        hybrid = []
        for j in range(5):
            if random.random() < 0.6:  # 60% do melhor
                hybrid.append(best_chrom[j])
            else:  # 40% aleatório
                hybrid.append(random_solution[j])

        new_population.append(hybrid)

    # Estratégia 4: Soluções completamente aleatórias (10%)
    random_count = population_size - len(new_population)
    print(f"   🎲 Criando {random_count} soluções aleatórias...")
    for i in range(random_count):
        new_population.append(random_chrom())

    # Análise da diversidade criada
    unique_configs = set(str(chrom) for chrom in new_population)
    diversity_percentage = (len(unique_configs) / len(new_population)) * 100

    print(
        f"   📊 Diversidade resultante: {len(unique_configs)}/{len(new_population)} ({diversity_percentage:.1f}%)"
    )

    # Conta quantos têm fitness alto
    fitness_distribution = {}
    for chrom in new_population:
        f = fitness_func(chrom)
        fitness_distribution[f] = fitness_distribution.get(f, 0) + 1

    print(f"   🏆 Distribuição de fitness:")
    for f in sorted(fitness_distribution.keys(), reverse=True):
        count = fitness_distribution[f]
        percentage = (count / len(new_population)) * 100
        if f >= 13:  # Só mostra fitness alto
            print(f"      {f:2d}/15: {count:3d} ({percentage:4.1f}%)")

    high_fitness_count = sum(
        count for f, count in fitness_distribution.items() if f >= 13
    )
    print(f"   ✨ Total 13+: {high_fitness_count}/{len(new_population)}")

    return new_population


def force_rule_specific_variations(best_chrom, missing_rule, num_variations=100):
    """Força variações específicas para resolver uma regra problemática"""
    print(f"\n🎯 FORÇA VARIAÇÕES ESPECÍFICAS - REGRA {missing_rule}")

    variations = []

    if missing_rule == 2:  # Inglês na casa Vermelha
        print(f"   🔄 Gerando {num_variations} variações focadas em R2")

        for i in range(num_variations):
            candidate = [list(casa) for casa in best_chrom]

            # Encontra posições atuais
            ingles_pos = next(
                j for j, casa in enumerate(candidate) if casa[1] == "Inglês"
            )
            vermelha_pos = next(
                j for j, casa in enumerate(candidate) if casa[0] == "Vermelha"
            )

            # Estratégia A: Move Inglês para casa Vermelha (50%)
            if i < num_variations // 2:
                # Troca nacionalidades
                candidate[ingles_pos][1], candidate[vermelha_pos][1] = (
                    candidate[vermelha_pos][1],
                    candidate[ingles_pos][1],
                )

            # Estratégia B: Move Vermelha para casa do Inglês (50%)
            else:
                # Troca cores
                candidate[ingles_pos][0], candidate[vermelha_pos][0] = (
                    candidate[vermelha_pos][0],
                    candidate[ingles_pos][0],
                )

            variations.append([tuple(casa) for casa in candidate])

    elif missing_rule == 5:  # Verde-Branca sequencial
        print(f"   🔄 Gerando {num_variations} variações focadas em R5")

        valid_positions = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
        ]  # Posições válidas para Verde-Branca

        for i in range(num_variations):
            candidate = [list(casa) for casa in best_chrom]

            # Escolhe posição alvo
            verde_target, branca_target = valid_positions[i % len(valid_positions)]

            # Força Verde e Branca nas posições corretas
            verde_atual = next(
                j for j, casa in enumerate(candidate) if casa[0] == "Verde"
            )
            branca_atual = next(
                j for j, casa in enumerate(candidate) if casa[0] == "Branca"
            )

            # Swap cores
            candidate[verde_atual][0], candidate[verde_target][0] = (
                candidate[verde_target][0],
                candidate[verde_atual][0],
            )
            candidate[branca_atual][0], candidate[branca_target][0] = (
                candidate[branca_target][0],
                candidate[branca_atual][0],
            )

            variations.append([tuple(casa) for casa in candidate])

    elif missing_rule == 8:  # Amarela-Dunhill
        print(f"   🔄 Gerando {num_variations} variações focadas em R8")

        for i in range(num_variations):
            candidate = [list(casa) for casa in best_chrom]

            # Encontra posições
            amarela_pos = next(
                j for j, casa in enumerate(candidate) if casa[0] == "Amarela"
            )
            dunhill_pos = next(
                j for j, casa in enumerate(candidate) if casa[3] == "Dunhill"
            )

            # Estratégia A: Move Dunhill para casa Amarela
            if i < num_variations // 2:
                candidate[amarela_pos][3], candidate[dunhill_pos][3] = (
                    candidate[dunhill_pos][3],
                    candidate[amarela_pos][3],
                )
            # Estratégia B: Move Amarela para casa Dunhill
            else:
                candidate[amarela_pos][0], candidate[dunhill_pos][0] = (
                    candidate[dunhill_pos][0],
                    candidate[amarela_pos][0],
                )

            variations.append([tuple(casa) for casa in candidate])

    return variations
