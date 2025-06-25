"""
Algoritmo Genético para resolver o Desafio de Einstein
Disciplina: Inteligência Artificial
Prof. Tiago Bonini Borchartt
"""

import time
import random

from genetic_algorithm import (
    random_chrom,
    mutate,
    crossover,
    hybrid_selection,
    show_solution,
)
from einstein_rules import fitness

# Parâmetros otimizados
POPULATION_SIZE = 2500
CROSSOVER_RATE = 0.85
MUTATION_RATE = 0.20
SURVIVAL_RATE = 0.08
IMMIGRATION_RATE = 0.12


def main():
    """Algoritmo Genético otimizado com logs detalhados"""
    print("🧬 ALGORITMO GENÉTICO - DESAFIO DE EINSTEIN")
    print("=" * 70)
    print("🎯 OBJETIVO: Encontrar solução 15/15")
    print(
        f"📊 População: {POPULATION_SIZE} | Mutação: {MUTATION_RATE*100:.0f}% | Crossover: {CROSSOVER_RATE*100:.0f}%"
    )
    print("=" * 70)

    start_time = time.time()

    # População inicial
    POP = [random_chrom() for _ in range(POPULATION_SIZE)]

    generation = 0
    best_ever_fitness = 0
    generations_without_improvement = 0

    # Contadores para estatísticas
    generations_at_13 = 0
    generations_at_14 = 0
    best_ever_at_14_time = None

    print("📈 EVOLUÇÃO DETALHADA:")
    print("   Geração | Fitness | Diversidade | Tempo(s) | Status Detalhado")
    print("-" * 75)

    while True:
        # 1. AVALIAÇÃO
        fitness_values = [fitness(chrom) for chrom in POP]

        # Ordenar por fitness
        sorted_indices = sorted(
            range(len(POP)), key=lambda i: fitness_values[i], reverse=True
        )
        POP = [POP[i] for i in sorted_indices]
        fitness_values = [fitness_values[i] for i in sorted_indices]

        best_chrom = POP[0]
        best_fitness = fitness_values[0]
        avg_fitness = sum(fitness_values) / len(fitness_values)
        diversity = len(set(str(chrom) for chrom in POP))
        elapsed = time.time() - start_time

        # Atualizar contadores
        if best_fitness > best_ever_fitness:
            best_ever_fitness = best_fitness
            generations_without_improvement = 0

            if best_fitness == 14 and best_ever_at_14_time is None:
                best_ever_at_14_time = elapsed
                generations_at_14 = 0
        else:
            generations_without_improvement += 1

        # Contadores específicos
        if best_fitness == 13:
            generations_at_13 += 1
        elif best_fitness == 14:
            generations_at_14 += 1

        # LOG DETALHADO A CADA 50 GERAÇÕES OU MARCOS IMPORTANTES
        should_log = (
            generation % 50 == 0
            or generation < 20
            or best_fitness >= 13
            or generations_without_improvement % 100 == 0
        )

        if should_log:
            print(
                f"   {generation:7d} | {best_fitness:2d}/15   | {diversity:6d}/{POPULATION_SIZE} | {elapsed:6.1f}s | ",
                end="",
            )

            # Status detalhado baseado no fitness
            if best_fitness == 15:
                print("🎉 SOLUÇÃO ENCONTRADA!")
            elif best_fitness == 14:
                mutation_intensity = MUTATION_RATE * 3.0 * 100
                print(
                    f"🔥 SPRINT FINAL! Mutação {mutation_intensity:.0f}% (há {generations_at_14} gens)"
                )
            elif best_fitness == 13:
                print(
                    f"🎯 Convergindo bem (há {generations_at_13} gens) - Próximo: 14/15"
                )
            elif best_fitness >= 11:
                trend = (
                    "↗️ Subindo" if generations_without_improvement < 50 else "↔️ Estável"
                )
                print(f"📈 Boa evolução {trend} - Meta: 13/15")
            elif generations_without_improvement > 200:
                print("🔄 Buscando nova região do espaço")
            else:
                print(f"🌱 Explorando (média: {avg_fitness:.1f})")

        # 2. CRITÉRIO DE PARADA - SOLUÇÃO!
        if best_fitness == 15:
            print()
            print("🎉" * 20)
            print("           SOLUÇÃO 15/15 ENCONTRADA!")
            print("🎉" * 20)
            print(f"⏱️  Tempo total: {elapsed:.1f} segundos")
            print(f"🧬 Gerações: {generation:,}")
            if best_ever_at_14_time:
                time_14_to_15 = elapsed - best_ever_at_14_time
                print(
                    f"🚀 Tempo de 14→15: {time_14_to_15:.1f}s ({generations_at_14} gerações)"
                )
            break

        # 3. DIVERSIFICAÇÃO INTELIGENTE (sem restart agressivo)
        restart_threshold = 800 if best_fitness >= 14 else 400

        if generations_without_improvement > restart_threshold:
            elite_percent = 0.1 if best_fitness >= 14 else 0.05
            elite_size = int(POPULATION_SIZE * elite_percent)

            print(
                f"   {generation:7d} | {best_fitness:2d}/15   | {diversity:6d}/{POPULATION_SIZE} | {elapsed:6.1f}s | 🔄 Diversificação (elite: {elite_percent*100:.0f}%)"
            )

            POP = POP[:elite_size] + [
                random_chrom() for _ in range(POPULATION_SIZE - elite_size)
            ]
            generations_without_improvement = 0
            continue

        # 4. OPERAÇÕES GENÉTICAS OTIMIZADAS

        # Sobrevivência (elitismo)
        num_survivors = int(POPULATION_SIZE * SURVIVAL_RATE)
        survivors = POP[:num_survivors]

        # Reprodução com intensidade baseada no fitness
        offspring = []
        target_offspring = (
            POPULATION_SIZE - num_survivors - int(POPULATION_SIZE * IMMIGRATION_RATE)
        )

        while len(offspring) < target_offspring:
            # Seleção e mutação adaptativas
            if best_fitness >= 14:
                # FOCO EXTREMO para 14→15
                pool_size = min(25, len(POP))
                mutation_rate = MUTATION_RATE * 3.0  # 60% - exploração máxima
            elif best_fitness >= 13:
                # Foco moderado para 13→14
                pool_size = min(100, len(POP))
                mutation_rate = MUTATION_RATE * 2.0  # 40%
            else:
                # Exploração normal
                pool_size = min(300, len(POP))
                mutation_rate = MUTATION_RATE  # 20%

            # Seleção dos pais
            p1 = hybrid_selection(POP[:pool_size], fitness_values[:pool_size])
            p2 = hybrid_selection(POP[:pool_size], fitness_values[:pool_size])

            # Crossover e mutação
            c1, c2 = crossover(p1, p2, CROSSOVER_RATE)
            c1 = mutate(c1, mutation_rate)
            c2 = mutate(c2, mutation_rate)

            offspring.extend([c1, c2])

        # Imigração (diversidade)
        num_immigrants = int(POPULATION_SIZE * IMMIGRATION_RATE)
        immigrants = [random_chrom() for _ in range(num_immigrants)]

        # Nova geração
        POP = survivors + offspring[:target_offspring] + immigrants
        generation += 1

    # APRESENTAÇÃO DA SOLUÇÃO
    print("=" * 70)
    print("                      SOLUÇÃO FINAL")
    print("=" * 70)

    show_solution(best_chrom)

    # Resposta do desafio
    for idx, casa in enumerate(best_chrom, 1):
        if casa[4] == "Peixes":
            print(f"\n🐟 RESPOSTA DO DESAFIO: O {casa[1]} tem os Peixes! (Casa {idx})")
            break

    # Estatísticas finais
    print(f"\n📊 ESTATÍSTICAS COMPLETAS:")
    print(f"   🎯 Fitness final: 15/15 (perfeito!)")
    print(f"   🧬 Total de gerações: {generation:,}")
    print(f"   ⏱️  Tempo total: {elapsed:.1f} segundos")
    print(f"   📈 Gerações em fitness 13: {generations_at_13:,}")
    print(f"   🔥 Gerações em fitness 14: {generations_at_14:,}")
    if best_ever_at_14_time:
        print(f"   🚀 Tempo para chegar em 14/15: {best_ever_at_14_time:.1f}s")
        print(f"   ⚡ Tempo de 14→15: {elapsed - best_ever_at_14_time:.1f}s")

    print(f"\n✅ ALGORITMO GENÉTICO CONCLUÍDO COM SUCESSO!")


if __name__ == "__main__":
    main()
