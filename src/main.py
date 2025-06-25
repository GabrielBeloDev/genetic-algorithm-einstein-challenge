"""
Algoritmo Genético OTIMIZADO para resolver o Desafio de Einstein
Disciplina: Inteligência Artificial
Prof. Tiago Bonini Borchartt

VERSÃO OTIMIZADA COM ESTRATÉGIAS AVANÇADAS
"""

import time
import random
import copy

from genetic_algorithm import (
    random_chrom,
    mutate,
    crossover,
    hybrid_selection,
    tournament_selection,
    smart_mutate,
    directed_mutate,
    local_search,
    advanced_crossover,
    create_elite_offspring,
    specialized_rule5_mutate,
    debug_rule5_status,
    intensive_rule5_repair,
    brute_force_rule5,
    analyze_chromosome_detailed,
    debug_specific_rule,
    print_chromosome_visual,
    deep_population_analysis,
    show_solution,
    controlled_rule5_fix,
    emergency_rule5_solver,
    ultra_debug_mutation_failure,
    analyze_population_stagnation,
    diversity_explosion,
    force_rule_specific_variations,
)
from einstein_rules import (
    fitness,
    weighted_fitness,
    get_missing_rules,
    detailed_fitness_report,
    partial_fitness_scores,
)

# Parâmetros otimizados dinamicamente
BASE_POPULATION_SIZE = 3000
MAX_POPULATION_SIZE = 5000
BASE_CROSSOVER_RATE = 0.90
BASE_MUTATION_RATE = 0.15
SURVIVAL_RATE = 0.10
IMMIGRATION_RATE = 0.15


class AdvancedGeneticAlgorithm:
    def __init__(self):
        self.population_size = BASE_POPULATION_SIZE
        self.crossover_rate = BASE_CROSSOVER_RATE
        self.mutation_rate = BASE_MUTATION_RATE

        # Controle adaptativo
        self.generations_without_improvement = 0
        self.current_best_fitness = 0
        self.generations_at_14 = 0
        self.generations_at_13 = 0

        # Estatísticas
        self.fitness_history = []
        self.diversity_history = []

    def adapt_parameters(self, best_fitness, diversity):
        """Adapta parâmetros baseado no progresso atual"""

        if best_fitness >= 14:
            # MODO SPRINT FINAL - máxima intensidade
            self.population_size = min(MAX_POPULATION_SIZE, self.population_size + 100)
            self.mutation_rate = 0.4  # 40% - exploração máxima
            self.crossover_rate = 0.95

        elif best_fitness >= 13:
            # MODO CONVERGÊNCIA FOCADA
            self.population_size = min(4000, self.population_size + 50)
            self.mutation_rate = 0.25  # 25%
            self.crossover_rate = 0.90

        elif best_fitness >= 11:
            # MODO EXPLORAÇÃO MODERADA
            self.mutation_rate = 0.20
            self.crossover_rate = 0.85

        else:
            # MODO EXPLORAÇÃO AMPLA
            self.mutation_rate = 0.15
            self.crossover_rate = 0.80

        # Ajuste baseado na diversidade
        if diversity < self.population_size * 0.3:  # Baixa diversidade
            self.mutation_rate *= 1.5

    def create_specialized_population(self, size):
        """Cria população com diferentes estratégias"""
        population = []

        # 70% população aleatória
        random_count = int(size * 0.7)
        population.extend([random_chrom() for _ in range(random_count)])

        # 20% população com regras fixas satisfeitas
        fixed_count = int(size * 0.2)
        for _ in range(fixed_count):
            chrom = random_chrom()
            # Força algumas regras fáceis
            # Regra 1: Norueguês na primeira casa
            houses = [list(house) for house in chrom]
            for i, house in enumerate(houses):
                if house[1] == "Norueguês":
                    houses[0][1], houses[i][1] = houses[i][1], houses[0][1]
                    break

            # Regra 9: Leite na casa do meio
            houses[2][2] = "Leite"

            chrom = [tuple(house) for house in houses]
            population.append(chrom)

        # 10% população restante aleatória
        remaining = size - len(population)
        population.extend([random_chrom() for _ in range(remaining)])

        return population

    def run(self):
        """Executa o algoritmo genético otimizado"""
        print("🧬 ALGORITMO GENÉTICO OTIMIZADO - DESAFIO DE EINSTEIN")
        print("=" * 80)
        print("🎯 OBJETIVO: Encontrar solução 15/15")
        print("🚀 ESTRATÉGIAS: Busca Local + Seleção Híbrida + Mutação Dirigida")
        print("🔄 LIMITE: 500 gerações para debug")
        print("=" * 80)

        start_time = time.time()
        MAX_GENERATIONS = 500  # LIMITE PARA DEBUG

        # População inicial especializada
        POP = self.create_specialized_population(self.population_size)

        generation = 0
        best_ever_fitness = 0
        best_ever_chromosome = None
        time_at_14 = None

        print("📈 EVOLUÇÃO DETALHADA:")
        print(
            "   Geração | Fitness | Pop.Size | Div% | Tempo(s) | Status & Estratégias"
        )
        print("-" * 85)

        while True:
            generation += 1

            # CRITÉRIO DE PARADA - LIMITE DE GERAÇÕES PARA DEBUG
            if generation > MAX_GENERATIONS:
                elapsed = time.time() - start_time
                print(f"\n⏰ LIMITE DE GERAÇÕES ATINGIDO: {MAX_GENERATIONS}")
                print(f"   🏆 Melhor fitness: {best_ever_fitness}/15")
                print(f"   ⏱️ Tempo total: {elapsed:.1f}s")
                print(f"   📊 Média: {elapsed/generation:.3f}s por geração")

                if best_ever_fitness == 14:
                    missing = get_missing_rules(best_ever_chromosome)
                    print(f"   🎯 Faltou apenas: Regra {missing[0]}")
                    print_chromosome_visual(best_ever_chromosome)

                return best_ever_chromosome, best_ever_fitness

            # 1. AVALIAÇÃO COMPLETA
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
            diversity_percent = (diversity / len(POP)) * 100
            elapsed = time.time() - start_time

            # Atualizar estatísticas
            self.fitness_history.append(best_fitness)
            self.diversity_history.append(diversity_percent)

            # Controle de progresso
            if best_fitness > best_ever_fitness:
                best_ever_fitness = best_fitness
                best_ever_chromosome = copy.deepcopy(best_chrom)
                self.generations_without_improvement = 0

                if best_fitness == 14 and time_at_14 is None:
                    time_at_14 = elapsed
                    self.generations_at_14 = 0
            else:
                self.generations_without_improvement += 1

            if best_fitness == 13:
                self.generations_at_13 += 1
            elif best_fitness == 14:
                self.generations_at_14 += 1

            self.adapt_parameters(best_fitness, diversity)

            # LOG DETALHADO
            should_log = (
                generation % 25 == 0
                or generation < 50
                or best_fitness >= 13
                or self.generations_without_improvement % 200 == 0
            )

            if should_log:
                print(
                    f"   {generation:7d} | {best_fitness:2d}/15   | {len(POP):6d} | {diversity_percent:3.0f}% | {elapsed:6.1f}s | ",
                    end="",
                )

                # Status detalhado com estratégias ativas
                if best_fitness == 15:
                    print("🎉 SOLUÇÃO PERFEITA ENCONTRADA!")
                elif best_fitness == 14:
                    missing = get_missing_rules(best_chrom)

                    # DEBUG MEGA DETALHADO
                    if (
                        generation % 10 == 0 or self.generations_at_14 == 1
                    ):  # A cada 10 gerações ou primeira vez no 14
                        missing_rule = missing[0]
                        rule_debug = debug_specific_rule(best_chrom, missing_rule)

                        print(
                            f"🔥 R{missing_rule} TRAVADO: {rule_debug['description']}"
                        )
                        print(f"    🔍 Debug: {rule_debug['detailed_analysis']}")

                        # Se ficar muito tempo preso, faz análise completa
                        if (
                            self.generations_at_14 % 50 == 0
                            and self.generations_at_14 > 0
                        ):
                            print(
                                f"\n⚠️  ANÁLISE COMPLETA - PRESO EM R{missing_rule} há {self.generations_at_14} gerações!"
                            )
                            deep_population_analysis(POP[:10], fitness, 3)
                    else:
                        missing_rule = missing[0]
                        print(
                            f"🔥 R{missing_rule} PRESO há {self.generations_at_14} gens | Mut:{self.mutation_rate*100:.0f}% | Pop:{len(POP)}"
                        )

                elif best_fitness == 13:
                    missing = get_missing_rules(best_chrom)
                    print(
                        f"🎯 Foco 13→14! Faltam: {missing} (há {self.generations_at_13} gens)"
                    )
                elif best_fitness >= 11:
                    trend = "↗️" if self.generations_without_improvement < 100 else "↔️"
                    print(f"📈 Evolução {trend} | Mut:{self.mutation_rate*100:.0f}%")
                else:
                    print(
                        f"🌱 Exploração | Mut:{self.mutation_rate*100:.0f}% | Avg:{avg_fitness:.1f}"
                    )

            # 2. CRITÉRIO DE PARADA - SOLUÇÃO ENCONTRADA!
            if best_fitness == 15:
                print()
                print("🎉" * 25)
                print("                SOLUÇÃO 15/15 ENCONTRADA!")
                print("🎉" * 25)
                break

            # 3. ESTRATÉGIAS DE DIVERSIFICAÇÃO
            if self.generations_without_improvement > 1000:
                if best_fitness >= 14:
                    # Para fitness 14, diversificação suave
                    elite_size = int(len(POP) * 0.15)  # 15% elite
                    print(
                        f"   {generation:7d} | {best_fitness:2d}/15   | {len(POP):6d} | {diversity_percent:3.0f}% | {elapsed:6.1f}s | 🔄 Diversif. Suave (15% elite)"
                    )
                else:
                    # Para fitness menor, diversificação mais agressiva
                    elite_size = int(len(POP) * 0.08)  # 8% elite
                    print(
                        f"   {generation:7d} | {best_fitness:2d}/15   | {len(POP):6d} | {diversity_percent:3.0f}% | {elapsed:6.1f}s | 🔄 Diversif. Agressiva (8% elite)"
                    )

                POP = POP[:elite_size] + self.create_specialized_population(
                    len(POP) - elite_size
                )
                self.generations_without_improvement = 0
                continue

            # 4. OPERAÇÕES GENÉTICAS AVANÇADAS

            # Elite (sobrevivência)
            num_survivors = int(len(POP) * SURVIVAL_RATE)
            survivors = POP[:num_survivors]

            # ESTRATÉGIA ESPECIAL PARA QUALQUER REGRA NO 14/15
            if best_fitness == 14:
                missing_rule_num = (
                    get_missing_rules(best_chrom)[0]
                    if get_missing_rules(best_chrom)
                    else None
                )

                if missing_rule_num:
                    # Log detalhado a cada 20 gerações
                    if generation % 20 == 0:
                        print(f"\n🎯 FOCO NA REGRA {missing_rule_num}:")
                        rule_debug = debug_specific_rule(best_chrom, missing_rule_num)
                        print(f"   📋 {rule_debug['description']}")
                        print(f"   🔍 {rule_debug['detailed_analysis']}")
                        print_chromosome_visual(best_chrom)

                    # DEBUG SUPER DETALHADO - POPULAÇÃO E DIVERSIDADE
                    if generation % 50 == 0:  # A cada 50 gerações em vez de 25
                        print(f"\n🔬 DEBUG SUPER DETALHADO - GERAÇÃO {generation}")
                        print(f"   📊 População: {len(POP)} indivíduos")
                        print(
                            f"   🎯 Diversidade: {diversity}/{len(POP)} = {diversity_percent:.1f}%"
                        )
                        print(
                            f"   🏆 Fitness 14: {sum(1 for f in fitness_values if f == 14)} indivíduos"
                        )
                        print(
                            f"   📈 Fitness 13: {sum(1 for f in fitness_values if f == 13)} indivíduos"
                        )
                        print(
                            f"   📉 Fitness <13: {sum(1 for f in fitness_values if f < 13)} indivíduos"
                        )

                        # Analisa se existem diferentes configurações ou todas são iguais
                        solutions_14 = [chrom for chrom in POP if fitness(chrom) == 14]
                        if solutions_14:
                            # Análise das regras faltantes
                            missing_rules = {}
                            for chrom in solutions_14[:100]:  # Pega 100 amostras
                                missing = get_missing_rules(chrom)
                                if missing:
                                    rule_num = missing[0]
                                    missing_rules[rule_num] = (
                                        missing_rules.get(rule_num, 0) + 1
                                    )

                            unique_configs = set(
                                str(chrom) for chrom in solutions_14[:100]
                            )
                            print(
                                f"   🧬 Configurações únicas (14/15): {len(unique_configs)}"
                            )
                            print(f"   🎲 Regras faltantes: {missing_rules}")

                            if len(unique_configs) < 10:
                                print(
                                    f"   ⚠️  PROBLEMA: Muito pouca diversidade nas soluções 14/15!"
                                )
                                print(
                                    f"   🔄 População convergiu para poucas configurações similares"
                                )

                                # ANÁLISE CRÍTICA: Por que não consegue sair da configuração atual?
                                print(f"\n🚨 ANÁLISE CRÍTICA - CONFIGURAÇÃO TRAVADA:")
                                best_14 = max(solutions_14, key=fitness)
                                print_chromosome_visual(best_14)

                                # Testa FORÇA BRUTA: o que acontece se quebrarmos TODAS as outras regras?
                                print(f"🔬 TESTE FORÇA BRUTA - QUEBRAR OUTRAS REGRAS:")
                                test_candidate = [list(casa) for casa in best_14]

                                # FORÇA Verde-Branca sequencial nas 4 posições possíveis
                                for verde_pos, branca_pos in [
                                    (0, 1),
                                    (1, 2),
                                    (2, 3),
                                    (3, 4),
                                ]:
                                    # Cria teste focado
                                    test_copy = [list(casa) for casa in test_candidate]

                                    # FORÇA cores nas posições
                                    cores_originais = [casa[0] for casa in test_copy]
                                    test_copy[verde_pos][0] = "Verde"
                                    test_copy[branca_pos][0] = "Branca"

                                    # Redistribui outras cores
                                    outras_cores = [
                                        c
                                        for c in ["Amarela", "Azul", "Vermelha"]
                                        if (verde_pos != 0 or c != "Verde")
                                        and (branca_pos != 4 or c != "Branca")
                                    ]
                                    outras_posicoes = [
                                        i
                                        for i in range(5)
                                        if i != verde_pos and i != branca_pos
                                    ]

                                    for i, pos in enumerate(
                                        outras_posicoes[: len(outras_cores)]
                                    ):
                                        if i < len(outras_cores):
                                            test_copy[pos][0] = outras_cores[i]

                                    test_fitness = fitness(
                                        [tuple(casa) for casa in test_copy]
                                    )
                                    print(
                                        f"      Verde:{verde_pos+1}->Branca:{branca_pos+1} = Fitness {test_fitness}/15"
                                    )

                                    if test_fitness == 15:
                                        print(
                                            f"   🎉 SOLUÇÃO ENCONTRADA! Aplicando configuração..."
                                        )
                                        return [tuple(casa) for casa in test_copy]

                        # Executa análise de estagnação se necessário
                        is_stagnated = analyze_population_stagnation(POP[:100], fitness)

                        if is_stagnated:
                            print(f"   🚨 POPULAÇÃO ESTAGNADA DETECTADA!")
                            print(f"   💥 Ativando EXPLOSÃO DE DIVERSIDADE")
                            print(f"   📊 População atual: {len(POP)} indivíduos")
                            print(
                                f"   🎯 Fitness preso: {best_fitness}/15 (Regra {missing_rule_num})"
                            )

                            # FORÇA EXPLOSÃO DE DIVERSIDADE
                            print(f"\n🔥 FASE 1: EXPLOSÃO GERAL")
                            POP = diversity_explosion(best_chrom, len(POP), fitness)

                            # FORÇA VARIAÇÕES ESPECÍFICAS DA REGRA PROBLEMÁTICA
                            print(f"\n🔥 FASE 2: VARIAÇÕES ESPECÍFICAS")
                            specific_variations = force_rule_specific_variations(
                                best_chrom, missing_rule_num, 200
                            )
                            POP.extend(specific_variations)

                            print(f"\n🔥 FASE 3: RECOMPUTAÇÃO")
                            print(
                                f"   🧮 Calculando fitness para {len(POP)} indivíduos..."
                            )

                            # Recomputa fitness para nova população
                            fitness_values = [fitness(chrom) for chrom in POP]
                            best_fitness = max(fitness_values)
                            best_chrom = POP[fitness_values.index(best_fitness)]

                            # Nova análise
                            new_dist = {}
                            for f in fitness_values:
                                new_dist[f] = new_dist.get(f, 0) + 1

                            print(f"   📊 Nova distribuição:")
                            for f in sorted(new_dist.keys(), reverse=True):
                                if f >= 13:
                                    count = new_dist[f]
                                    percentage = (count / len(POP)) * 100
                                    print(
                                        f"      {f:2d}/15: {count:4d} ({percentage:4.1f}%)"
                                    )

                            print(f"   🏆 Novo melhor fitness: {best_fitness}/15")

                            # Reset contadores se houve explosão
                            if missing_rule_num:
                                if missing_rule_num == 5:
                                    self.generations_at_14 = 0
                                    self.generations_without_improvement = 0
                                    print(f"   🔄 Contadores resetados")

                            print(f"   ✅ Explosão concluída! Continuando evolução...")

                    # DEBUG DE MUTAÇÃO E CROSSOVER
                    if generation % 30 == 0:
                        print(f"\n🧬 DEBUG OPERAÇÕES GENÉTICAS:")
                        print(
                            f"   🎲 Taxa de mutação atual: {self.mutation_rate*100:.1f}%"
                        )
                        print(
                            f"   💞 Taxa de crossover: {self.crossover_rate*100:.1f}%"
                        )
                        print(f"   👥 Tamanho da população: {len(POP)}")
                        print(
                            f"   🏆 Elite sobrevivente: {int(len(POP) * SURVIVAL_RATE)}"
                        )
                        print(f"   🆕 Imigrantes: {int(len(POP) * IMMIGRATION_RATE)}")

                        # Teste de efetividade das operações
                        test_chrom = best_chrom
                        original_fitness = fitness(test_chrom)

                        # Testa mutação
                        mutated = smart_mutate(
                            test_chrom, self.mutation_rate, original_fitness
                        )
                        mutated_fitness = fitness(mutated)

                        # Testa mutação dirigida
                        directed = directed_mutate(test_chrom, [missing_rule_num])
                        directed_fitness = fitness(directed)

                        print(
                            f"   🧪 Teste mutação: {original_fitness} → {mutated_fitness}"
                        )
                        print(
                            f"   🎯 Teste dirigida: {original_fitness} → {directed_fitness}"
                        )

                        if (
                            mutated_fitness == original_fitness
                            and directed_fitness == original_fitness
                        ):
                            print(
                                f"   ⚠️  PROBLEMA: Mutações não estão alterando fitness!"
                            )

                    # Estratégias escalantes baseadas no tempo preso
                    if self.generations_at_14 > 100:  # Muito preso
                        # FORÇA BRUTA TOTAL - tenta todas as combinações da regra faltante
                        print(
                            f"   {generation:7d} | {best_fitness:2d}/15   | {len(POP):6d} | {diversity_percent:3.0f}% | {elapsed:6.1f}s | 💥 FORÇA BRUTA TOTAL R{missing_rule_num}"
                        )

                        # Substitui parte da população com versões especializadas
                        specialized_pop = []
                        for _ in range(50):
                            candidate = best_chrom
                            # Faz 20 mutações focadas
                            for _ in range(20):
                                candidate = smart_mutate(candidate, 0.8, 14)
                            specialized_pop.append(candidate)

                        survivors[: len(specialized_pop)] = specialized_pop

                    elif self.generations_at_14 > 50:  # Preso moderadamente
                        # Reparo intensivo + mutação dirigida
                        print(
                            f"   {generation:7d} | {best_fitness:2d}/15   | {len(POP):6d} | {diversity_percent:3.0f}% | {elapsed:6.1f}s | 🔧 REPARO INTENSIVO R{missing_rule_num}"
                        )

                        repaired_pop = []
                        for chrom in POP[:30]:
                            if fitness(chrom) == 14:
                                best_repair = chrom
                                best_fit = 14

                                # 30 tentativas de reparo
                                for _ in range(30):
                                    candidate = smart_mutate(chrom, 0.6, 14)
                                    candidate = directed_mutate(
                                        candidate, [missing_rule_num]
                                    )
                                    cand_fit = fitness(candidate)

                                    if cand_fit > best_fit:
                                        best_repair = candidate
                                        best_fit = cand_fit

                                    if best_fit == 15:
                                        break

                                repaired_pop.append(best_repair)

                        if repaired_pop:
                            survivors[: len(repaired_pop)] = repaired_pop

                    elif self.generations_at_14 > 20:  # Início do problema
                        print(
                            f"   {generation:7d} | {best_fitness:2d}/15   | {len(POP):6d} | {diversity_percent:3.0f}% | {elapsed:6.1f}s | 🎯 FOCO DIRIGIDO R{missing_rule_num}"
                        )

            # Aplicar busca local na elite de alto fitness
            if best_fitness >= 13:
                elite_for_local = POP[: min(5, len(POP))]
                improved_elite = []
                for chrom in elite_for_local:
                    if fitness(chrom) >= 13:
                        improved = local_search(chrom, fitness, 15)
                        improved_elite.append(improved)
                    else:
                        improved_elite.append(chrom)
                survivors[: len(improved_elite)] = improved_elite

            # Reprodução com múltiplas estratégias
            offspring = []
            target_offspring = (
                len(POP) - num_survivors - int(len(POP) * IMMIGRATION_RATE)
            )

            # Offspring de elite (20%)
            if best_fitness >= 13:
                elite_offspring_count = int(target_offspring * 0.2)
                elite_offspring = create_elite_offspring(
                    POP[:20], fitness_values[:20], fitness
                )[:elite_offspring_count]
                offspring.extend(elite_offspring)

            # Offspring normal
            while len(offspring) < target_offspring:
                # Seleção adaptativa
                if best_fitness >= 14:
                    # Torneio pequeno e agressivo
                    p1 = tournament_selection(POP[:10], fitness_values[:10], 3)
                    p2 = tournament_selection(POP[:10], fitness_values[:10], 3)
                elif best_fitness >= 13:
                    # Torneio moderado
                    p1 = tournament_selection(POP[:50], fitness_values[:50], 5)
                    p2 = tournament_selection(POP[:50], fitness_values[:50], 5)
                else:
                    # Seleção híbrida normal
                    p1 = hybrid_selection(POP[:200], fitness_values[:200])
                    p2 = hybrid_selection(POP[:200], fitness_values[:200])

                # Crossover avançado
                if best_fitness >= 13:
                    c1, c2 = advanced_crossover(p1, p2, self.crossover_rate)
                else:
                    c1, c2 = crossover(p1, p2, self.crossover_rate)

                # Mutação inteligente
                missing_rules_1 = get_missing_rules(c1)
                missing_rules_2 = get_missing_rules(c2)

                c1 = smart_mutate(c1, self.mutation_rate, fitness(c1))
                c2 = smart_mutate(c2, self.mutation_rate, fitness(c2))

                # Mutação dirigida para alta fitness
                if best_fitness >= 12:
                    c1 = directed_mutate(c1, missing_rules_1)
                    c2 = directed_mutate(c2, missing_rules_2)

                offspring.extend([c1, c2])

            # Imigração especializada
            num_immigrants = int(len(POP) * IMMIGRATION_RATE)
            immigrants = self.create_specialized_population(num_immigrants)

            # Nova geração
            POP = survivors + offspring[:target_offspring] + immigrants

            # Manter tamanho da população controlado
            if len(POP) > self.population_size:
                POP = POP[: self.population_size]

        # APRESENTAÇÃO FINAL DA SOLUÇÃO
        print("=" * 80)
        print("                      SOLUÇÃO FINAL DETALHADA")
        print("=" * 80)

        show_solution(best_ever_chromosome)

        # Análise detalhada
        report = detailed_fitness_report(best_ever_chromosome)
        partial_scores = partial_fitness_scores(best_ever_chromosome)

        print(f"\n📊 ANÁLISE DETALHADA:")
        print(f"   ✅ Regras satisfeitas: {report['satisfied']}")
        if report["missing"]:
            print(f"   ❌ Regras faltantes: {report['missing']}")
        print(f"   📈 Pontuação por categoria:")
        for category, score in partial_scores.items():
            print(f"      {category.capitalize()}: {score}")

        # Resposta do desafio
        for idx, casa in enumerate(best_ever_chromosome, 1):
            if casa[4] == "Peixes":
                print(
                    f"\n🐟 RESPOSTA DO DESAFIO: O {casa[1]} tem os Peixes! (Casa {idx})"
                )
                break

        # Estatísticas finais
        final_time = time.time() - start_time
        print(f"\n📊 ESTATÍSTICAS FINAIS:")
        print(f"   🎯 Fitness final: {best_ever_fitness}/15")
        print(f"   🧬 Total de gerações: {generation:,}")
        print(f"   ⏱️  Tempo total: {final_time:.1f} segundos")
        print(f"   👥 População final: {len(POP):,} indivíduos")
        if time_at_14:
            print(f"   🚀 Tempo para chegar em 14/15: {time_at_14:.1f}s")
            print(f"   ⚡ Tempo de 14→15: {final_time - time_at_14:.1f}s")
        print(f"   📈 Taxa de diversidade final: {diversity_percent:.1f}%")

        print(f"\n✅ ALGORITMO GENÉTICO OTIMIZADO CONCLUÍDO!")

        return best_ever_chromosome, best_ever_fitness


def main():
    """Função principal"""
    ga = AdvancedGeneticAlgorithm()
    solution, fitness_score = ga.run()

    if fitness_score == 15:
        print("\n🎊 PARABÉNS! Solução perfeita encontrada!")
    else:
        print(f"\n⚠️ Melhor solução encontrada: {fitness_score}/15")


if __name__ == "__main__":
    main()
