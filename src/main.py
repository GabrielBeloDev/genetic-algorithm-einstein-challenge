"""
Algoritmo Genético para resolver o Desafio de Einstein
Disciplina: Inteligência Artificial
Prof. Tiago Bonini Borchartt

Este programa implementa um algoritmo genético para resolver o famoso
Desafio de Einstein, um quebra-cabeça lógico que envolve 5 casas,
5 nacionalidades, 5 bebidas, 5 cigarros e 5 animais.
"""

import time
import random
from typing import List, Tuple

# Importar módulos do projeto
from genetic_algorithm import (
    ATTRS,
    random_chrom,
    mutate,
    crossover,
    roulette_selection,
    show_solution,
)
from einstein_rules import RULES, fitness

# Parâmetros do Algoritmo Genético
POPULATION_SIZE = 800  # Tamanho da população
CROSSOVER_RATE = 0.80  # Taxa de crossover (80%)
MUTATION_RATE = 0.05  # Taxa de mutação (5%)
SURVIVAL_RATE = 0.10  # Taxa de sobrevivência (10% - elitismo)
IMMIGRATION_RATE = 0.05  # Taxa de imigração (5%)


def main():
    """Função principal que executa o algoritmo genético"""
    print("🧬 ALGORITMO GENÉTICO - DESAFIO DE EINSTEIN")
    print("=" * 60)
    print("📋 REQUISITOS IMPLEMENTADOS:")
    print("   ✅ Cromossomos representam soluções codificadas")
    print("   ✅ Função fitness baseada nas 15 regras")
    print("   ✅ Operações: sobrevivência, crossover, mutação, imigração")
    print("   ✅ Método da roleta para seleção")
    print("   ✅ Visualização genótipo/fenótipo")
    print("=" * 60)
    print("📊 PARÂMETROS CONFIGURADOS:")
    print(f"   • População: {POPULATION_SIZE} indivíduos")
    print(f"   • Taxa Crossover: {CROSSOVER_RATE*100:.0f}%")
    print(f"   • Taxa Mutação: {MUTATION_RATE*100:.0f}%")
    print(f"   • Taxa Sobrevivência: {SURVIVAL_RATE*100:.0f}%")
    print(f"   • Taxa Imigração: {IMMIGRATION_RATE*100:.0f}%")
    print("=" * 60)

    # ---- ALGORITMO GENÉTICO PRINCIPAL ----------------------------------------
    print("🎲 Gerando população inicial...")
    start_time = time.time()
    POP = [random_chrom() for _ in range(POPULATION_SIZE)]

    generation = 0
    print(f"✅ População inicial: {len(POP)} cromossomos gerados")
    print("\n🔍 Iniciando evolução...")

    while True:
        # 1. AVALIAÇÃO
        fitness_values = [fitness(chrom) for chrom in POP]

        # Ordenar por fitness (melhores primeiro)
        sorted_indices = sorted(
            range(len(POP)), key=lambda i: fitness_values[i], reverse=True
        )
        POP = [POP[i] for i in sorted_indices]
        fitness_values = [fitness_values[i] for i in sorted_indices]

        best = POP[0]
        best_fitness = fitness_values[0]
        avg_fitness = sum(fitness_values) / len(fitness_values)

        # Log de progresso
        if generation % 100 == 0 or best_fitness >= 14:
            elapsed = time.time() - start_time
            print(
                f"Geração {generation:4d} | Melhor: {best_fitness:2d}/15 | Média: {avg_fitness:4.1f} | Tempo: {elapsed:5.1f}s"
            )

        # 2. CRITÉRIO DE PARADA
        if best_fitness == 15:
            elapsed_time = time.time() - start_time
            print(f"\n🎉 SOLUÇÃO ENCONTRADA NA GERAÇÃO {generation}!")
            print(f"⏱️  Tempo total: {elapsed_time:.2f} segundos")
            break

        # 3. OPERAÇÕES GENÉTICAS

        # SOBREVIVÊNCIA (Elitismo)
        num_survivors = int(POPULATION_SIZE * SURVIVAL_RATE)
        survivors = POP[:num_survivors]

        # REPRODUÇÃO (Crossover + Mutação)
        offspring = []
        while len(offspring) < POPULATION_SIZE - num_survivors - int(
            POPULATION_SIZE * IMMIGRATION_RATE
        ):
            # Seleção por roleta
            p1 = roulette_selection(POP[:100], fitness_values[:100])  # Top 100
            p2 = roulette_selection(POP[:100], fitness_values[:100])

            # Crossover
            c1, c2 = crossover(p1, p2, CROSSOVER_RATE)

            # Mutação
            c1 = mutate(c1, MUTATION_RATE)
            c2 = mutate(c2, MUTATION_RATE)

            offspring.extend([c1, c2])

        # IMIGRAÇÃO
        num_immigrants = int(POPULATION_SIZE * IMMIGRATION_RATE)
        immigrants = [random_chrom() for _ in range(num_immigrants)]

        # Nova população
        POP = (
            survivors
            + offspring[: POPULATION_SIZE - num_survivors - num_immigrants]
            + immigrants
        )
        generation += 1

    # ---- APRESENTAÇÃO DA SOLUÇÃO FINAL ---------------------------------------
    show_solution(best)

    # Encontrar quem tem os peixes (resposta do desafio)
    for idx, casa in enumerate(best, 1):
        if casa[4] == "Peixes":
            print(f"\n🐟 RESPOSTA: O {casa[1]} (Casa {idx}) tem os Peixes!")
            break

    # Verificação das regras
    print(f"\n📋 VERIFICAÇÃO DAS 15 REGRAS:")
    regras_corretas = 0
    for i, rule in enumerate(RULES, 1):
        status = "✅" if rule(best) else "❌"
        if rule(best):
            regras_corretas += 1
        print(f"   Regra {i:2d}: {status}")

    print(f"\n🏆 RESULTADO FINAL:")
    print(f"   • Solução encontrada na geração: {generation}")
    print(f"   • Tempo de execução: {elapsed_time:.2f} segundos")
    print(f"   • Regras satisfeitas: {regras_corretas}/15")
    print(f"   • Algoritmo genético: SUCESSO! ✅")

    print(f"\n📚 DEMONSTRAÇÃO DOS REQUISITOS ATENDIDOS:")
    print(f"   ✅ Cromossomos codificados (5 casas × 5 atributos)")
    print(f"   ✅ Função fitness baseada nas 15 regras")
    print(f"   ✅ Sobrevivência: {SURVIVAL_RATE*100:.0f}% dos melhores")
    print(f"   ✅ Crossover: {CROSSOVER_RATE*100:.0f}% de taxa")
    print(f"   ✅ Mutação: {MUTATION_RATE*100:.0f}% de taxa")
    print(f"   ✅ Imigração: {IMMIGRATION_RATE*100:.0f}% novos indivíduos")
    print(f"   ✅ Método da roleta implementado")
    print(f"   ✅ População de {POPULATION_SIZE} indivíduos")
    print(f"   ✅ Visualização da solução")
    print(f"   ✅ Execução até encontrar solução")


if __name__ == "__main__":
    main()
