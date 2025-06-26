"""
Algoritmo Genético OTIMIZADO para resolver o Desafio de Einstein
Disciplina: Inteligência Artificial
Prof. Tiago Bonini Borchartt

VERSÃO 2.0
"""

import time
import random
import copy
from typing import List

from genetic_algorithm import (
    cromossomo_aleatorio,
    mutacao,
    cruzamento,
    selecao_hibrida,
    selecao_torneio,
    mutacao_inteligente,
    mutacao_dirigida,
    busca_local,
    cruzamento_avancado,
    criar_descendentes_elite,
    mutacao_especializada_regra5,
    debug_status_regra5,
    reparacao_intensiva_regra5,
    forca_bruta_regra5,
    analisar_cromossomo_detalhado,
    debug_regra_especifica,
    imprimir_cromossomo_visual,
    analise_profunda_populacao,
    mostrar_solucao,
    correcao_controlada_regra5,
    solucionador_emergencia_regra5,
    ultra_debug_falha_mutacao,
    analisar_estagnacao_populacao,
    explosao_diversidade,
    forcar_variacoes_regra_especifica,
)
from einstein_rules import (
    fitness,
    fitness_ponderado,
    obter_regras_faltantes,
    relatorio_detalhado_fitness,
    pontuacoes_parciais_fitness,
)

# CONFIG DO ALGORITMO GENÉTICO
TAMANHO_POPULACAO_BASE = 3000
TAXA_CRUZAMENTO_BASE = 0.85
TAXA_MUTACAO_BASE = 0.15
TAMANHO_MAXIMO_POPULACAO = 5000


class AlgoritmoGeneticoAvancado:

    def __init__(self):
        self.tamanho_populacao = TAMANHO_POPULACAO_BASE
        self.taxa_cruzamento = TAXA_CRUZAMENTO_BASE
        self.taxa_mutacao = TAXA_MUTACAO_BASE

        self.geracoes_sem_melhoria = 0
        self.melhor_fitness_atual = 0
        self.geracoes_no_fitness_14 = 0
        self.geracoes_no_fitness_13 = 0

        self.historico_fitness = []
        self.historico_diversidade = []

    # adaptação dinâmica dos parâmetros do algoritmo baseada no progresso
    # estrategia: intensificação vs diversificação // para alto fitness: intensificação (busca local intensiva)
    # para fitness médio: equilíbrio //  para baixo fitness: diversificação (exploração ampla)
    def adaptar_parametros(self, melhor_fitness, diversidade):

        # fase de intensificação quando chega nos 14
        if melhor_fitness >= 14:
            self.tamanho_populacao = min(
                TAMANHO_MAXIMO_POPULACAO, self.tamanho_populacao + 100
            )
            self.taxa_mutacao = 0.4  # mutação intensiva para escape de ótimos locais
            self.taxa_cruzamento = 0.95

        elif melhor_fitness >= 13:
            self.tamanho_populacao = min(
                4000, self.tamanho_populacao + 50
            )  # fase de convergência guiada // solucao de alta qualidade
            self.taxa_mutacao = 0.25
            self.taxa_cruzamento = 0.90

        elif melhor_fitness >= 11:
            self.taxa_mutacao = (
                0.20  # fase de exploração moderada: balance exploração-explotação
            )
            self.taxa_cruzamento = 0.85

        else:
            self.taxa_mutacao = (
                0.15  # fase de exploração ampla: busca por regiões promissoras
            )
            self.taxa_cruzamento = 0.80

        # ajuste baseado na diversidade populacional
        if diversidade < self.tamanho_populacao * 0.3:  # baixa diversidade detectada
            self.taxa_mutacao *= 1.5  # aumenta mutação para recuperar diversidade

    # criacao de populacao inicial com estratégias diversificada
    # 70% população aleatória (exploração) // estratégia 1: população aleatória para exploração ampla
    # 20% população com heurísticas (satisfaz regras fáceis) // estratégia 2: população com heurísticas aplicadas
    # 10% população híbrida
    def criar_populacao_especializada(self, tamanho):
        populacao = []
        individuos_aleatorios = int(tamanho * 0.7)
        populacao.extend([cromossomo_aleatorio() for _ in range(individuos_aleatorios)])

        individuos_heuristicos = int(tamanho * 0.2)
        for _ in range(individuos_heuristicos):
            cromossomo = cromossomo_aleatorio()
            # Aplica heurística: Regra 1 (Norueguês na primeira casa)
            casas = [list(casa) for casa in cromossomo]
            for i, casa in enumerate(casas):
                if casa[1] == "Norueguês":
                    casas[0][1], casas[i][1] = casas[i][1], casas[0][1]
                    break

            casas[2][2] = "Leite"

            cromossomo = [tuple(casa) for casa in casas]
            populacao.append(cromossomo)

        restantes = tamanho - len(populacao)
        populacao.extend([cromossomo_aleatorio() for _ in range(restantes)])

        return populacao

    def executar(self):
        print("=" * 80)
        print("🧬 ALGORITMO GENÉTICO PARA O DESAFIO LÓGICO DE EINSTEIN")
        print("=" * 80)
        print("OBJETIVO: Resolver o puzzle de satisfação de 15 restrições")
        print("METODOLOGIA: Algoritmo Genético com Estratégias Adaptativas")
        print("LIMITE COMPUTACIONAL: 1000 gerações")
        print("CRITÉRIO DE SUCESSO: Fitness = 15/15 (todas as regras satisfeitas)")
        print("=" * 80)

        tempo_inicio = time.time()
        LIMITE_GERACOES = 1000

        print("\n🚀 FASE 1: INICIALIZAÇÃO DA POPULAÇÃO DIVERSIFICADA")
        populacao = self.criar_populacao_especializada(self.tamanho_populacao)
        print(f"   População inicial criada: {len(populacao)} indivíduos")

        geracao = 0
        melhor_fitness_global = 0
        melhor_cromossomo_global = None
        tempo_atingiu_14 = None

        print("\n📊 EVOLUÇÃO DO ALGORITMO:")
        print(
            "   Geração | Fitness | Tamanho Pop | Diversidade | Tempo | Status Evolutivo"
        )
        print("-" * 85)

        while True:
            geracao += 1

            if geracao > LIMITE_GERACOES:
                tempo_total = time.time() - tempo_inicio
                print(
                    f"\n⏰ EXPERIMENTO CONCLUÍDO: {LIMITE_GERACOES} gerações executadas"
                )
                print(f"   Melhor fitness encontrada: {melhor_fitness_global}/15")
                print(f"   Tempo computacional total: {tempo_total:.1f} segundos")
                print(f"   Eficiência: {tempo_total/geracao:.3f}s por geração")

                if melhor_fitness_global == 14:
                    regras_faltantes = obter_regras_faltantes(melhor_cromossomo_global)
                    print(
                        f"   Análise final: Faltou satisfazer apenas a Regra {regras_faltantes[0]}"
                    )
                    print("\nCONFIGURAÇÃO FINAL:")
                    imprimir_cromossomo_visual(melhor_cromossomo_global)

                return melhor_cromossomo_global, melhor_fitness_global

            valores_fitness = [fitness(cromossomo) for cromossomo in populacao]

            # ordenação por fitness (seleção por ranking)
            indices_ordenados = sorted(
                range(len(populacao)), key=lambda i: valores_fitness[i], reverse=True
            )
            populacao = [populacao[i] for i in indices_ordenados]
            valores_fitness = [valores_fitness[i] for i in indices_ordenados]

            # análise estatística da geração atual
            melhor_cromossomo = populacao[0]
            melhor_fitness = valores_fitness[0]
            fitness_media = sum(valores_fitness) / len(valores_fitness)
            diversidade_populacional = len(
                set(str(cromossomo) for cromossomo in populacao)
            )
            percentual_diversidade = (diversidade_populacional / len(populacao)) * 100
            tempo_decorrido = time.time() - tempo_inicio

            # att do histórico acadêmico
            self.historico_fitness.append(melhor_fitness)
            self.historico_diversidade.append(percentual_diversidade)

            # controle de progresso evolutivo
            if melhor_fitness > melhor_fitness_global:
                melhor_fitness_global = melhor_fitness
                melhor_cromossomo_global = copy.deepcopy(melhor_cromossomo)
                self.geracoes_sem_melhoria = 0

                if melhor_fitness == 14 and tempo_atingiu_14 is None:
                    tempo_atingiu_14 = tempo_decorrido
                    self.geracoes_no_fitness_14 = 0
                    print(
                        f"\n🎯 MARCO : Fitness 14/15 atingido em {tempo_decorrido:.1f}s!"
                    )
            else:
                self.geracoes_sem_melhoria += 1

            # contador para o debug
            if melhor_fitness == 13:
                self.geracoes_no_fitness_13 += 1
            elif melhor_fitness == 14:
                self.geracoes_no_fitness_14 += 1

            self.adaptar_parametros(melhor_fitness, diversidade_populacional)

            if melhor_fitness == 15:
                tempo_total = time.time() - tempo_inicio
                print(f"\n" + "🎉" * 20)
                print("✅ SOLUÇÃO ÓTIMA ENCONTRADA!")
                print("🎉" * 20)
                print("=" * 80)
                print("🏆 RESULTADO : Problema de Satisfação de Restrições RESOLVIDO")
                print("=" * 80)

                print(f"\n📈 MÉTRICAS DE PERFORMANCE COMPUTACIONAL:")
                print(f"   • Tempo de convergência: {tempo_total:.2f} segundos")
                print(f"   • Gerações necessárias: {geracao:,}")
                print(
                    f"   • Eficiência computacional: {tempo_total/geracao:.3f}s por geração"
                )
                print(f"   • Tamanho final da população: {len(populacao):,} indivíduos")
                print(f"   • Diversidade final: {percentual_diversidade:.1f}%")
                print(f"   • Taxa de mutação final: {self.taxa_mutacao*100:.1f}%")
                print(f"   • Taxa de cruzamento final: {self.taxa_cruzamento*100:.1f}%")

                if tempo_atingiu_14:
                    print(f"   • Tempo para atingir 14/15: {tempo_atingiu_14:.2f}s")
                    print(
                        f"   • Tempo para otimização final (14→15): {tempo_total - tempo_atingiu_14:.2f}s"
                    )
                    print(
                        f"   • Eficiência da fase final: {((tempo_total - tempo_atingiu_14)/1):.2f}s"
                    )

                print(f"\n🏠 CONFIGURAÇÃO DA SOLUÇÃO ENCONTRADA:")
                print("=" * 80)
                print("✨ Todas as 15 regras do Desafio de Einstein foram satisfeitas!")
                print("=" * 80)

                print(f"\n📋 TABELA COMPLETA DA SOLUÇÃO:")
                print("┌" + "─" * 78 + "┐")
                print(
                    "│"
                    + "CASA │ COR       │ NACIONALIDADE │ BEBIDA  │ CIGARRO    │ ANIMAL    │".center(
                        78
                    )
                    + "│"
                )
                print("├" + "─" * 78 + "┤")

                for i, casa in enumerate(melhor_cromossomo, 1):
                    cor, nacionalidade, bebida, cigarro, animal = casa
                    linha = f"│ {i:2d}   │ {cor:9s} │ {nacionalidade:13s} │ {bebida:7s} │ {cigarro:10s} │ {animal:9s} │"
                    print(linha)

                print("└" + "─" * 78 + "┘")

                print(f"\n✅ VERIFICAÇÃO DETALHADA DAS 15 REGRAS:")
                print("=" * 80)

                regras_descricoes = [
                    "R1: O Norueguês vive na primeira casa",
                    "R2: O Inglês vive na casa Vermelha",
                    "R3: O Sueco tem Cachorros",
                    "R4: O Dinamarquês bebe Chá",
                    "R5: A casa Verde fica do lado esquerdo da casa Branca",
                    "R6: O homem que vive na casa Verde bebe Café",
                    "R7: O homem que fuma Pall Mall cria Pássaros",
                    "R8: O homem que vive na casa Amarela fuma Dunhill",
                    "R9: O homem que vive na casa do meio bebe Leite",
                    "R10: O homem que fuma Blends vive ao lado do que tem Gatos",
                    "R11: O homem que cria Cavalos vive ao lado do que fuma Dunhill",
                    "R12: O homem que fuma BlueMaster bebe Cerveja",
                    "R13: O Alemão fuma Prince",
                    "R14: O Norueguês vive ao lado da casa Azul",
                    "R15: O homem que fuma Blends é vizinho do que bebe Água",
                ]

                from einstein_rules import REGRAS

                for i, (regra, descricao) in enumerate(zip(REGRAS, regras_descricoes)):
                    status = (
                        "✅ SATISFEITA"
                        if regra(melhor_cromossomo)
                        else "❌ NÃO SATISFEITA"
                    )
                    print(f"{descricao:55s} {status}")

                # RESPOSTA
                print(f"\n🐟 RESPOSTA AO DESAFIO LÓGICO DE EINSTEIN:")
                print("=" * 50)
                for posicao, casa in enumerate(melhor_cromossomo, 1):
                    if casa[4] == "Peixes":
                        print(f"🎯 RESPOSTA FINAL: O {casa[1]} possui os Peixes!")
                        print(f"   → Localização: Casa {posicao}")
                        print(f"   → Características completas da casa:")
                        print(f"     • Cor: {casa[0]}")
                        print(f"     • Nacionalidade: {casa[1]}")
                        print(f"     • Bebida: {casa[2]}")
                        print(f"     • Cigarro: {casa[3]}")
                        print(f"     • Animal: {casa[4]}")
                        break

                print(f"\n🔬 ANÁLISE DETALHADA:")
                print("=" * 50)

                relatorio_detalhado = relatorio_detalhado_fitness(melhor_cromossomo)
                pontuacoes_parciais = pontuacoes_parciais_fitness(melhor_cromossomo)

                print(
                    f"   • Fitness total alcançado: {relatorio_detalhado['score']}/15 (100%)"
                )
                print(
                    f"   • Fitness ponderado: {relatorio_detalhado['weighted_score']:.1f}"
                )
                print(f"   • Regras satisfeitas: {relatorio_detalhado['satisfied']}")
                print(f"   • Análise por categorias:")

                categorias_nomes = {
                    "simples": "Regras Simples (atribuição direta)",
                    "posicao": "Regras de Posição (localização fixa)",
                    "sequencia": "Regras Sequenciais (ordem específica)",
                    "vizinhanca": "Regras de Vizinhança (adjacência)",
                }

                for categoria, pontuacao in pontuacoes_parciais.items():
                    nome_categoria = categorias_nomes.get(categoria, categoria)
                    print(f"     → {nome_categoria}: {pontuacao}")

                print(f"\n📈 HISTÓRICO DE EVOLUÇÃO DO ALGORITMO:")
                print("=" * 50)

                fitness_marcos = {}
                for i, fitness_hist in enumerate(self.historico_fitness):
                    if fitness_hist not in fitness_marcos:
                        fitness_marcos[fitness_hist] = i + 1

                print(f"   • Marcos de fitness atingidos:")
                for fitness_val in sorted(fitness_marcos.keys()):
                    geracao_marco = fitness_marcos[fitness_val]
                    percentual = (fitness_val / 15) * 100
                    print(
                        f"     → Fitness {fitness_val:2d}/15 ({percentual:5.1f}%): Geração {geracao_marco:4d}"
                    )

                print(f"\n🧠 ESTRATÉGIAS DE ALGORITMO GENÉTICO UTILIZADAS:")
                print("=" * 50)
                print(f"   • Seleção Híbrida: Combinação de torneio e roleta")
                print(f"   • Mutação Inteligente: Adaptativa baseada no fitness")
                print(f"   • Cruzamento Avançado: Uniforme com reparo automático")
                print(f"   • Busca Local: Hill-climbing para refinamento")
                print(
                    f"   • Adaptação Paramétrica: Taxas dinâmicas baseadas no progresso"
                )
                print(
                    f"   • Diversificação: Explosão populacional para escape de ótimos locais"
                )
                print(f"   • Elite Preservation: Preservação dos melhores indivíduos")
                print(
                    f"   • Mutação Dirigida: Foco em regras específicas não satisfeitas"
                )

                print("=" * 80)

                return melhor_cromossomo, 15

            # Logging
            deve_registrar_log = (
                geracao % 25 == 0
                or geracao < 50
                or melhor_fitness >= 13
                or self.geracoes_sem_melhoria % 200 == 0
            )

            if deve_registrar_log:
                print(
                    f"   {geracao:7d} | {melhor_fitness:2d}/15   | {len(populacao):6d} | {percentual_diversidade:8.1f}% | {tempo_decorrido:6.1f}s | ",
                    end="",
                )

                # Status evolutivo
                if melhor_fitness == 15:
                    print("SOLUÇÃO ÓTIMA ENCONTRADA!")
                elif melhor_fitness == 14:
                    regras_faltantes = obter_regras_faltantes(melhor_cromossomo)

                    if geracao % 10 == 0 or self.geracoes_no_fitness_14 == 1:
                        regra_faltante = regras_faltantes[0]
                        analise_regra = debug_regra_especifica(
                            melhor_cromossomo, regra_faltante
                        )

                        print(f"Refinamento: Regra {regra_faltante} pendente")
                        print(f"    Descrição: {analise_regra['description']}")
                        print(f"    Análise: {analise_regra['detailed_analysis']}")

                        if (
                            self.geracoes_no_fitness_14 % 50 == 0
                            and self.geracoes_no_fitness_14 > 0
                        ):
                            print(
                                f"\nANÁLISE: Estagnação detectada na Regra {regra_faltante} ({self.geracoes_no_fitness_14} gerações)"
                            )
                            analise_profunda_populacao(populacao[:10], fitness, 3)
                    else:
                        regra_faltante = regras_faltantes[0]
                        print(
                            f"Otimização local: R{regra_faltante} | Parâmetros: Mut={self.taxa_mutacao*100:.0f}% | Pop={len(populacao)}"
                        )

                elif melhor_fitness == 13:
                    regras_faltantes = obter_regras_faltantes(melhor_cromossomo)
                    print(
                        f"Convergência intermediária: {len(regras_faltantes)} regras pendentes ({self.geracoes_no_fitness_13} gerações)"
                    )
                elif melhor_fitness >= 11:
                    tendencia = (
                        "Progresso positivo"
                        if self.geracoes_sem_melhoria < 100
                        else "Estabilização"
                    )
                    print(
                        f"Exploração: {tendencia} | Mutação={self.taxa_mutacao*100:.0f}%"
                    )
                else:
                    print(
                        f"Busca inicial | Mutação={self.taxa_mutacao*100:.0f}% | Fitness média={fitness_media:.1f}"
                    )

            if melhor_fitness == 14:
                regras_faltantes = obter_regras_faltantes(melhor_cromossomo)
                regra_pendente = regras_faltantes[0] if regras_faltantes else None

                if regra_pendente:
                    # análise de convergência prematura
                    if geracao % 25 == 0:
                        print(f"\nANÁLISE DE CONVERGÊNCIA:")
                        print(f"   Regra pendente: {regra_pendente}")
                        regra_debug = debug_regra_especifica(
                            melhor_cromossomo, regra_pendente
                        )
                        print(f"   {regra_debug['description']}")
                        print(f"   {regra_debug['detailed_analysis']}")
                        imprimir_cromossomo_visual(melhor_cromossomo)

                    if self.geracoes_no_fitness_14 > 20:  # busca dirigida
                        print(
                            f"   {geracao:7d} | {melhor_fitness:2d}/15   | {len(populacao):6d} | {percentual_diversidade:3.0f}% | {tempo_decorrido:6.1f}s | Busca dirigida (Regra {regra_pendente})"
                        )

                        # mutação dirigida na elite
                        for i in range(min(50, len(populacao))):
                            if fitness(populacao[i]) == 14:
                                regras_falt = obter_regras_faltantes(populacao[i])
                                if regras_falt:
                                    populacao[i] = mutacao_dirigida(
                                        populacao[i], regras_falt
                                    )

                    elif self.geracoes_no_fitness_14 > 50:
                        print(
                            f"   {geracao:7d} | {melhor_fitness:2d}/15   | {len(populacao):6d} | {percentual_diversidade:3.0f}% | {tempo_decorrido:6.1f}s | Busca local intensiva (Regra {regra_pendente})"
                        )

                        for i in range(min(30, len(populacao))):
                            if fitness(populacao[i]) == 14:
                                candidato_melhorado = busca_local(
                                    populacao[i], fitness, 30
                                )
                                if fitness(candidato_melhorado) > fitness(populacao[i]):
                                    populacao[i] = candidato_melhorado

                    elif self.geracoes_no_fitness_14 > 100:
                        print(
                            f"   {geracao:7d} | {melhor_fitness:2d}/15   | {len(populacao):6d} | {percentual_diversidade:3.0f}% | {tempo_decorrido:6.1f}s | Estratégia de escape de ótimo local"
                        )

                        versoes_especializadas = (
                            forca_bruta_regra5(melhor_cromossomo, fitness)
                            if regra_pendente == 5
                            else []
                        )

                        if versoes_especializadas:
                            populacao.extend(versoes_especializadas[:50])

            if geracao % 50 == 0:
                print(f"\nANÁLISE POPULACIONAL DETALHADA - GERAÇÃO {geracao}")
                print(f"   Tamanho da população: {len(populacao)} indivíduos")
                print(
                    f"   Diversidade genética: {diversidade_populacional}/{len(populacao)} = {percentual_diversidade:.1f}%"
                )
                print(
                    f"   Indivíduos de alta fitness (14/15): {sum(1 for f in valores_fitness if f == 14)}"
                )
                print(
                    f"   Indivíduos de fitness intermediária (13/15): {sum(1 for f in valores_fitness if f == 13)}"
                )
                print(
                    f"   Indivíduos de baixa fitness (<13): {sum(1 for f in valores_fitness if f < 13)}"
                )

                # análise de convergência prematura
                solucoes_14 = [
                    cromossomo for cromossomo in populacao if fitness(cromossomo) == 14
                ]
                if solucoes_14:
                    regras_faltantes_distribuicao = {}
                    for cromossomo in solucoes_14[:100]:
                        regras_faltantes = obter_regras_faltantes(cromossomo)
                        if regras_faltantes:
                            regra_num = regras_faltantes[0]
                            regras_faltantes_distribuicao[regra_num] = (
                                regras_faltantes_distribuicao.get(regra_num, 0) + 1
                            )

                    configuracoes_unicas = set(
                        str(cromossomo) for cromossomo in solucoes_14[:100]
                    )
                    print(
                        f"   Configurações únicas (14/15): {len(configuracoes_unicas)}"
                    )
                    print(
                        f"   Distribuição de regras pendentes: {regras_faltantes_distribuicao}"
                    )

                    # detecção de convergência prematura
                    if len(configuracoes_unicas) < 10:
                        print(f"   ALERTA ACADÊMICO: Convergência prematura detectada!")
                        print(
                            f"   Interpretação: População convergiu para soluções similares"
                        )

                        # teste de força bruta
                        if melhor_fitness == 14:
                            print(f"\nEXPERIMENTO: Teste de otimalidade local")
                            melhor_14 = max(solucoes_14, key=fitness)
                            imprimir_cromossomo_visual(melhor_14)

                            print(f"Testando configurações alternativas para escape:")
                            candidato_teste = [list(casa) for casa in melhor_14]

                            # teste sistemático das 4 configurações Verde-Branca
                            for pos_verde, pos_branca in [
                                (0, 1),
                                (1, 2),
                                (2, 3),
                                (3, 4),
                            ]:
                                copia_teste = [list(casa) for casa in candidato_teste]

                                copia_teste[pos_verde][0] = "Verde"
                                copia_teste[pos_branca][0] = "Branca"

                                outras_cores = ["Amarela", "Azul", "Vermelha"]
                                posicoes_restantes = [
                                    i
                                    for i in range(5)
                                    if i != pos_verde and i != pos_branca
                                ]

                                for i, pos in enumerate(posicoes_restantes[:3]):
                                    if i < len(outras_cores):
                                        copia_teste[pos][0] = outras_cores[i]

                                fitness_teste = fitness(
                                    [tuple(casa) for casa in copia_teste]
                                )
                                print(
                                    f"      Configuração Verde:{pos_verde+1}->Branca:{pos_branca+1} = Fitness {fitness_teste}/15"
                                )

                                if fitness_teste == 15:
                                    print(f"\nDESCOBERTA: Solução ótima identificada!")
                                    return [tuple(casa) for casa in copia_teste], 15

                    convergencia_detectada = analisar_estagnacao_populacao(
                        populacao[:100], fitness
                    )

                    if convergencia_detectada:
                        print(f"\nAPLICANDO ESTRATÉGIA DE DIVERSIFICAÇÃO")
                        print(
                            f"   Justificativa: Escape de ótimo local via perturbação"
                        )
                        print(f"   Metodologia: Explosão de diversidade guiada")

                        populacao = explosao_diversidade(
                            melhor_cromossomo, len(populacao), fitness
                        )

                        if regra_pendente:
                            variacoes_especializadas = (
                                forcar_variacoes_regra_especifica(
                                    melhor_cromossomo, regra_pendente, 200
                                )
                            )
                            populacao.extend(variacoes_especializadas)

                        valores_fitness = [
                            fitness(cromossomo) for cromossomo in populacao
                        ]
                        melhor_fitness = max(valores_fitness)
                        melhor_cromossomo = populacao[
                            valores_fitness.index(melhor_fitness)
                        ]

                        if regra_pendente == 5:
                            self.geracoes_no_fitness_14 = 0
                            self.geracoes_sem_melhoria = 0

                        print(
                            f"   Diversificação concluída: Nova fitness máxima = {melhor_fitness}/15"
                        )

                # Debug para casos extremos
                if melhor_fitness == 14 and self.geracoes_no_fitness_14 > 0:
                    if self.geracoes_no_fitness_14 % 100 == 0:
                        print(
                            f"\nANÁLISE APROFUNDADA - Estagnação de {self.geracoes_no_fitness_14} gerações"
                        )
                        ultra_debug_falha_mutacao(
                            melhor_cromossomo, fitness, regra_pendente, 500
                        )

            if self.geracoes_sem_melhoria > 1000:
                if melhor_fitness >= 14:
                    elite_preservada = int(len(populacao) * 0.15)  # 15% elite
                    print(
                        f"   {geracao:7d} | {melhor_fitness:2d}/15   | {len(populacao):6d} | {percentual_diversidade:3.0f}% | {tempo_decorrido:6.1f}s | Diversificação conservadora (preserva 15% elite)"
                    )
                else:
                    elite_preservada = int(len(populacao) * 0.08)  # 8% elite
                    print(
                        f"   {geracao:7d} | {melhor_fitness:2d}/15   | {len(populacao):6d} | {percentual_diversidade:3.0f}% | {tempo_decorrido:6.1f}s | Diversificação agressiva (preserva 8% elite)"
                    )

                populacao = populacao[
                    :elite_preservada
                ] + self.criar_populacao_especializada(
                    len(populacao) - elite_preservada
                )
                self.geracoes_sem_melhoria = 0
                continue

            taxa_sobrevivencia = 0.10
            numero_sobreviventes = int(len(populacao) * taxa_sobrevivencia)
            elite_sobrevivente = populacao[:numero_sobreviventes]

            if melhor_fitness >= 13:
                elite_para_refinamento = populacao[: min(5, len(populacao))]
                elite_refinada = []
                for cromossomo in elite_para_refinamento:
                    if fitness(cromossomo) >= 13:
                        cromossomo_melhorado = busca_local(cromossomo, fitness, 15)
                        elite_refinada.append(cromossomo_melhorado)
                    else:
                        elite_refinada.append(cromossomo)
                elite_sobrevivente[: len(elite_refinada)] = elite_refinada

            descendentes = []
            taxa_imigracao = 0.15
            numero_descendentes = (
                len(populacao)
                - numero_sobreviventes
                - int(len(populacao) * taxa_imigracao)
            )

            if melhor_fitness >= 13:
                descendentes_elite_count = int(numero_descendentes * 0.2)
                descendentes_elite = criar_descendentes_elite(
                    populacao[:20], valores_fitness[:20], fitness
                )[:descendentes_elite_count]
                descendentes.extend(descendentes_elite)

            # reprodução principal via seleção e crossover
            while len(descendentes) < numero_descendentes:
                # seleção adaptativa de pais
                if melhor_fitness >= 14:
                    # seleção por torneio restrita (busca local intensiva)
                    pai1 = selecao_torneio(populacao[:10], valores_fitness[:10], 3)
                    pai2 = selecao_torneio(populacao[:10], valores_fitness[:10], 3)
                elif melhor_fitness >= 13:
                    # seleção por torneio moderada
                    pai1 = selecao_torneio(populacao[:50], valores_fitness[:50], 5)
                    pai2 = selecao_torneio(populacao[:50], valores_fitness[:50], 5)
                else:
                    # seleção híbrida (exploração ampla)
                    pai1 = selecao_hibrida(populacao[:200], valores_fitness[:200])
                    pai2 = selecao_hibrida(populacao[:200], valores_fitness[:200])

                if melhor_fitness >= 13:
                    filho1, filho2 = cruzamento_avancado(
                        pai1, pai2, self.taxa_cruzamento
                    )
                else:
                    filho1, filho2 = cruzamento(pai1, pai2, self.taxa_cruzamento)

                regras_faltantes_f1 = obter_regras_faltantes(filho1)
                regras_faltantes_f2 = obter_regras_faltantes(filho2)

                filho1 = mutacao_inteligente(filho1, self.taxa_mutacao, fitness(filho1))
                filho2 = mutacao_inteligente(filho2, self.taxa_mutacao, fitness(filho2))

                if melhor_fitness >= 12:
                    filho1 = mutacao_dirigida(filho1, regras_faltantes_f1)
                    filho2 = mutacao_dirigida(filho2, regras_faltantes_f2)

                descendentes.extend([filho1, filho2])

            numero_imigrantes = int(len(populacao) * taxa_imigracao)
            imigrantes = self.criar_populacao_especializada(numero_imigrantes)

            populacao = (
                elite_sobrevivente + descendentes[:numero_descendentes] + imigrantes
            )

            if len(populacao) > self.tamanho_populacao:
                populacao = populacao[: self.tamanho_populacao]

    def _apresentar_resultados_finais(
        self,
        melhor_cromossomo,
        melhor_fitness,
        geracoes_executadas,
        tempo_inicio,
        tempo_14,
    ):
        print("\n" + "=" * 80)
        print("                    📊 RELATÓRIO FINAL DE RESULTADOS")
        print("=" * 80)

        mostrar_solucao(melhor_cromossomo)

        relatorio_detalhado = relatorio_detalhado_fitness(melhor_cromossomo)
        pontuacoes_parciais = pontuacoes_parciais_fitness(melhor_cromossomo)

        print(f"\n🔬 ANÁLISE DOS RESULTADOS:")
        print(f"   Regras de satisfação cumpridas: {relatorio_detalhado['satisfied']}")
        if relatorio_detalhado["missing"]:
            print(
                f"   Regras pendentes de satisfação: {relatorio_detalhado['missing']}"
            )
        print(f"   Análise por categorias de restrições:")
        for categoria, pontuacao in pontuacoes_parciais.items():
            print(f"      • {categoria.capitalize()}: {pontuacao}")

        print(f"\n🐟 RESPOSTA AO DESAFIO LÓGICO DE EINSTEIN:")
        for posicao, casa in enumerate(melhor_cromossomo, 1):
            if casa[4] == "Peixes":
                print(f"   🎯 Conclusão: O {casa[1]} possui os Peixes (Casa {posicao})")
                break

        tempo_total = time.time() - tempo_inicio
        print(f"\n⚡ MÉTRICAS DE PERFORMANCE COMPUTACIONAL:")
        print(f"   Fitness final alcançado: {melhor_fitness}/15")
        print(f"   Total de gerações evolutivas: {geracoes_executadas:,}")
        print(f"   Tempo computacional total: {tempo_total:.2f} segundos")
        print(f"   Eficiência por geração: {tempo_total/geracoes_executadas:.4f}s")
        print(f"   Tamanho final da população: {self.tamanho_populacao:,} indivíduos")

        if tempo_14:
            print(f"   Tempo para atingir 14/15: {tempo_14:.2f}s")
            if melhor_fitness == 15:
                print(
                    f"   Tempo para otimização final (14->15): {tempo_total - tempo_14:.2f}s"
                )

        print(f"\n🏁 EXPERIMENTO COMPUTACIONAL CONCLUÍDO")
        print("=" * 80)


def main():
    print("🎓 DISCIPLINA: Inteligência Artificial")
    print("👨‍🏫 PROFESSOR: Tiago Bonini Borchartt")
    print("📚 TRABALHO: Resolução do Desafio de Einstein via Algoritmos Genéticos")
    print("-" * 80)

    algoritmo_genetico = AlgoritmoGeneticoAvancado()
    solucao_final, fitness_final = algoritmo_genetico.executar()

    print(f"\n🏆 RESULTADO FINAL:")
    if fitness_final == 15:
        print(f"   ✅ EXCELENTE: Solução ótima encontrada!")
        print(f"   Todas as 15 restrições foram satisfeitas com sucesso")
    elif fitness_final == 14:
        print(f"   🎯 MUITO BOM: Solução quase-ótima encontrada!")
        print(f"   14 de 15 restrições satisfeitas (93.3% de sucesso)")
    else:
        print(f"   📈 RESULTADO: Solução parcial com fitness {fitness_final}/15")
        print(
            f"   {fitness_final} restrições satisfeitas ({(fitness_final/15)*100:.1f}% de sucesso)"
        )


if __name__ == "__main__":
    main()
