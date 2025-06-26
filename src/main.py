"""
Algoritmo Genético OTIMIZADO para resolver o Desafio de Einstein
Disciplina: Inteligência Artificial
Prof. Tiago Bonini Borchartt

VERSÃO ACADÊMICA COM ESTRATÉGIAS AVANÇADAS
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

# === CONFIGURAÇÕES DO ALGORITMO GENÉTICO ===
TAMANHO_POPULACAO_BASE = 3000
TAXA_CRUZAMENTO_BASE = 0.85
TAXA_MUTACAO_BASE = 0.15
TAMANHO_MAXIMO_POPULACAO = 5000


class AlgoritmoGeneticoAvancado:
    """
    Algoritmo Genético Avançado para resolver o Desafio de Einstein.

    Implementa estratégias adaptativas incluindo:
    - Seleção híbrida (torneio + roleta)
    - Mutação dirigida para regras específicas
    - Busca local para refinamento
    - Controle adaptativo de parâmetros
    - Diversificação populacional dinâmica
    """

    def __init__(self):
        # Parâmetros principais do algoritmo
        self.tamanho_populacao = TAMANHO_POPULACAO_BASE
        self.taxa_cruzamento = TAXA_CRUZAMENTO_BASE
        self.taxa_mutacao = TAXA_MUTACAO_BASE

        # Controle de progresso e adaptação
        self.geracoes_sem_melhoria = 0
        self.melhor_fitness_atual = 0
        self.geracoes_no_fitness_14 = 0
        self.geracoes_no_fitness_13 = 0

        # Histórico para análise acadêmica
        self.historico_fitness = []
        self.historico_diversidade = []

    def adaptar_parametros(self, melhor_fitness, diversidade):
        """
        Adaptação dinâmica dos parâmetros do algoritmo baseada no progresso.

        Estratégia acadêmica: Intensificação vs Diversificação
        - Alto fitness (14-15): Intensificação (busca local intensiva)
        - Médio fitness (11-13): Equilíbrio
        - Baixo fitness (<11): Diversificação (exploração ampla)
        """

        if melhor_fitness >= 14:
            # Fase de intensificação: busca refinada na região promissora
            self.tamanho_populacao = min(
                TAMANHO_MAXIMO_POPULACAO, self.tamanho_populacao + 100
            )
            self.taxa_mutacao = 0.4  # Mutação intensiva para escape de ótimos locais
            self.taxa_cruzamento = 0.95

        elif melhor_fitness >= 13:
            # Fase de convergência guiada: foco nas soluções de alta qualidade
            self.tamanho_populacao = min(4000, self.tamanho_populacao + 50)
            self.taxa_mutacao = 0.25
            self.taxa_cruzamento = 0.90

        elif melhor_fitness >= 11:
            # Fase de exploração moderada: balance exploração-explotação
            self.taxa_mutacao = 0.20
            self.taxa_cruzamento = 0.85

        else:
            # Fase de exploração ampla: busca por regiões promissoras
            self.taxa_mutacao = 0.15
            self.taxa_cruzamento = 0.80

        # Ajuste baseado na diversidade populacional
        if diversidade < self.tamanho_populacao * 0.3:  # Baixa diversidade detectada
            self.taxa_mutacao *= 1.5  # Aumenta mutação para recuperar diversidade

    def criar_populacao_especializada(self, tamanho):
        """
        Criação de população inicial com estratégias diversificadas.

        Metodologia acadêmica:
        - 70% população aleatória (exploração)
        - 20% população com heurísticas (satisfaz regras fáceis)
        - 10% população híbrida
        """
        populacao = []

        # Estratégia 1: População aleatória para exploração ampla
        individuos_aleatorios = int(tamanho * 0.7)
        populacao.extend([cromossomo_aleatorio() for _ in range(individuos_aleatorios)])

        # Estratégia 2: População com heurísticas aplicadas
        individuos_heuristicos = int(tamanho * 0.2)
        for _ in range(individuos_heuristicos):
            cromossomo = cromossomo_aleatorio()
            # Aplica heurística: Regra 1 (Norueguês na primeira casa)
            casas = [list(casa) for casa in cromossomo]
            for i, casa in enumerate(casas):
                if casa[1] == "Norueguês":
                    casas[0][1], casas[i][1] = casas[i][1], casas[0][1]
                    break

            # Aplica heurística: Regra 9 (Leite na casa central)
            casas[2][2] = "Leite"

            cromossomo = [tuple(casa) for casa in casas]
            populacao.append(cromossomo)

        # Estratégia 3: Completa com população aleatória
        restantes = tamanho - len(populacao)
        populacao.extend([cromossomo_aleatorio() for _ in range(restantes)])

        return populacao

    def executar(self):
        """
        Execução principal do Algoritmo Genético Avançado.

        Processo acadêmico estruturado:
        1. Inicialização da população
        2. Avaliação de fitness
        3. Seleção de pais
        4. Operadores genéticos (crossover + mutação)
        5. Substituição geracional
        6. Análise de convergência
        """
        print("=" * 80)
        print("🧬 ALGORITMO GENÉTICO PARA O DESAFIO LÓGICO DE EINSTEIN")
        print("=" * 80)
        print("OBJETIVO: Resolver o puzzle de satisfação de 15 restrições")
        print("METODOLOGIA: Algoritmo Genético com Estratégias Adaptativas")
        print("LIMITE COMPUTACIONAL: 1000 gerações")
        print("CRITÉRIO DE SUCESSO: Fitness = 15/15 (todas as regras satisfeitas)")
        print("=" * 80)

        tempo_inicio = time.time()
        LIMITE_GERACOES = 1000  # Limite acadêmico para análise

        # Fase 1: Inicialização da população
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

        # === LOOP EVOLUTIVO PRINCIPAL ===
        while True:
            geracao += 1

            # Critério de parada: limite computacional
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

            # Fase 2: Avaliação da população
            valores_fitness = [fitness(cromossomo) for cromossomo in populacao]

            # Ordenação por fitness (seleção por ranking)
            indices_ordenados = sorted(
                range(len(populacao)), key=lambda i: valores_fitness[i], reverse=True
            )
            populacao = [populacao[i] for i in indices_ordenados]
            valores_fitness = [valores_fitness[i] for i in indices_ordenados]

            # Análise estatística da geração atual
            melhor_cromossomo = populacao[0]
            melhor_fitness = valores_fitness[0]
            fitness_media = sum(valores_fitness) / len(valores_fitness)
            diversidade_populacional = len(
                set(str(cromossomo) for cromossomo in populacao)
            )
            percentual_diversidade = (diversidade_populacional / len(populacao)) * 100
            tempo_decorrido = time.time() - tempo_inicio

            # Atualização do histórico acadêmico
            self.historico_fitness.append(melhor_fitness)
            self.historico_diversidade.append(percentual_diversidade)

            # Controle de progresso evolutivo
            if melhor_fitness > melhor_fitness_global:
                melhor_fitness_global = melhor_fitness
                melhor_cromossomo_global = copy.deepcopy(melhor_cromossomo)
                self.geracoes_sem_melhoria = 0

                if melhor_fitness == 14 and tempo_atingiu_14 is None:
                    tempo_atingiu_14 = tempo_decorrido
                    self.geracoes_no_fitness_14 = 0
                    print(
                        f"\n🎯 MARCO CIENTÍFICO: Fitness 14/15 atingido em {tempo_decorrido:.1f}s!"
                    )
            else:
                self.geracoes_sem_melhoria += 1

            # Contadores específicos para análise
            if melhor_fitness == 13:
                self.geracoes_no_fitness_13 += 1
            elif melhor_fitness == 14:
                self.geracoes_no_fitness_14 += 1

            # Adaptação dinâmica dos parâmetros
            self.adaptar_parametros(melhor_fitness, diversidade_populacional)

            # === CRITÉRIO DE PARADA: SOLUÇÃO ÓTIMA ENCONTRADA ===
            if melhor_fitness == 15:
                tempo_total = time.time() - tempo_inicio
                print(f"\n" + "🎉" * 20)
                print("✅ SOLUÇÃO ÓTIMA ENCONTRADA!")
                print("🎉" * 20)
                print("=" * 80)
                print(
                    "🏆 RESULTADO CIENTÍFICO: Problema de Satisfação de Restrições RESOLVIDO"
                )
                print("=" * 80)

                # === MÉTRICAS DE PERFORMANCE ===
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

                # === CONFIGURAÇÃO SOLUÇÃO COMPLETA ===
                print(f"\n🏠 CONFIGURAÇÃO DA SOLUÇÃO ENCONTRADA:")
                print("=" * 80)
                print("✨ Todas as 15 regras do Desafio de Einstein foram satisfeitas!")
                print("=" * 80)

                # Tabela formatada da solução
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

                # === VERIFICAÇÃO DETALHADA DAS 15 REGRAS ===
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

                # === RESPOSTA AO DESAFIO ===
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

                # === ANÁLISE CIENTÍFICA DETALHADA ===
                print(f"\n🔬 ANÁLISE CIENTÍFICA DETALHADA:")
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

                # === EVOLUÇÃO DO ALGORITMO ===
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

                # === ESTRATÉGIAS UTILIZADAS ===
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

            # Logging acadêmico detalhado
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

                # Status evolutivo acadêmico
                if melhor_fitness == 15:
                    print("SOLUÇÃO ÓTIMA ENCONTRADA!")
                elif melhor_fitness == 14:
                    regras_faltantes = obter_regras_faltantes(melhor_cromossomo)

                    # Análise detalhada quando próximo da solução
                    if geracao % 10 == 0 or self.geracoes_no_fitness_14 == 1:
                        regra_faltante = regras_faltantes[0]
                        analise_regra = debug_regra_especifica(
                            melhor_cromossomo, regra_faltante
                        )

                        print(f"Refinamento: Regra {regra_faltante} pendente")
                        print(f"    Descrição: {analise_regra['description']}")
                        print(f"    Análise: {analise_regra['detailed_analysis']}")

                        # Análise aprofundada em marcos específicos
                        if (
                            self.geracoes_no_fitness_14 % 50 == 0
                            and self.geracoes_no_fitness_14 > 0
                        ):
                            print(
                                f"\nANÁLISE CIENTÍFICA: Estagnação detectada na Regra {regra_faltante} ({self.geracoes_no_fitness_14} gerações)"
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

            # === ESTRATÉGIAS ESPECIALIZADAS PARA ALTA FITNESS ===
            if melhor_fitness == 14:
                regras_faltantes = obter_regras_faltantes(melhor_cromossomo)
                regra_pendente = regras_faltantes[0] if regras_faltantes else None

                if regra_pendente:
                    # Estratégia acadêmica: Análise de convergência prematura
                    if geracao % 25 == 0:
                        print(f"\nANÁLISE DE CONVERGÊNCIA:")
                        print(f"   Regra pendente: {regra_pendente}")
                        regra_debug = debug_regra_especifica(
                            melhor_cromossomo, regra_pendente
                        )
                        print(f"   {regra_debug['description']}")
                        print(f"   {regra_debug['detailed_analysis']}")
                        imprimir_cromossomo_visual(melhor_cromossomo)

                    # Estratégia de intensificação baseada no tempo de estagnação
                    if self.geracoes_no_fitness_14 > 20:  # Busca dirigida
                        print(
                            f"   {geracao:7d} | {melhor_fitness:2d}/15   | {len(populacao):6d} | {percentual_diversidade:3.0f}% | {tempo_decorrido:6.1f}s | Busca dirigida (Regra {regra_pendente})"
                        )

                        # Aplicação de mutação dirigida na elite
                        for i in range(min(50, len(populacao))):
                            if fitness(populacao[i]) == 14:
                                regras_falt = obter_regras_faltantes(populacao[i])
                                if regras_falt:
                                    populacao[i] = mutacao_dirigida(
                                        populacao[i], regras_falt
                                    )

                    elif self.geracoes_no_fitness_14 > 50:  # Busca local intensiva
                        print(
                            f"   {geracao:7d} | {melhor_fitness:2d}/15   | {len(populacao):6d} | {percentual_diversidade:3.0f}% | {tempo_decorrido:6.1f}s | Busca local intensiva (Regra {regra_pendente})"
                        )

                        # Busca local nos melhores candidatos
                        for i in range(min(30, len(populacao))):
                            if fitness(populacao[i]) == 14:
                                candidato_melhorado = busca_local(
                                    populacao[i], fitness, 30
                                )
                                if fitness(candidato_melhorado) > fitness(populacao[i]):
                                    populacao[i] = candidato_melhorado

                    elif self.geracoes_no_fitness_14 > 100:  # Estratégia de escape
                        print(
                            f"   {geracao:7d} | {melhor_fitness:2d}/15   | {len(populacao):6d} | {percentual_diversidade:3.0f}% | {tempo_decorrido:6.1f}s | Estratégia de escape de ótimo local"
                        )

                        # Força bruta especializada na regra pendente
                        versoes_especializadas = (
                            forca_bruta_regra5(melhor_cromossomo, fitness)
                            if regra_pendente == 5
                            else []
                        )

                        if versoes_especializadas:
                            populacao.extend(versoes_especializadas[:50])

            # Análise de diversidade populacional (marco acadêmico)
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

                # Análise de convergência prematura
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

                    # Detecção de convergência prematura
                    if len(configuracoes_unicas) < 10:
                        print(f"   ALERTA ACADÊMICO: Convergência prematura detectada!")
                        print(
                            f"   Interpretação: População convergiu para soluções similares"
                        )

                        # Teste de força bruta científico
                        if melhor_fitness == 14:
                            print(f"\nEXPERIMENTO: Teste de otimalidade local")
                            melhor_14 = max(solucoes_14, key=fitness)
                            imprimir_cromossomo_visual(melhor_14)

                            print(f"Testando configurações alternativas para escape:")
                            candidato_teste = [list(casa) for casa in melhor_14]

                            # Teste sistemático das 4 configurações Verde-Branca
                            for pos_verde, pos_branca in [
                                (0, 1),
                                (1, 2),
                                (2, 3),
                                (3, 4),
                            ]:
                                copia_teste = [list(casa) for casa in candidato_teste]

                                # Força configuração Verde-Branca sequencial
                                copia_teste[pos_verde][0] = "Verde"
                                copia_teste[pos_branca][0] = "Branca"

                                # Redistribui outras cores
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
                                    print(
                                        f"\nDESCOBERTA CIENTÍFICA: Solução ótima identificada!"
                                    )
                                    return [tuple(casa) for casa in copia_teste], 15

                    # Estratégia de diversificação populacional
                    convergencia_detectada = analisar_estagnacao_populacao(
                        populacao[:100], fitness
                    )

                    if convergencia_detectada:
                        print(f"\nAPLICANDO ESTRATÉGIA DE DIVERSIFICAÇÃO")
                        print(
                            f"   Justificativa acadêmica: Escape de ótimo local via perturbação"
                        )
                        print(f"   Metodologia: Explosão de diversidade guiada")

                        # Diversificação científica
                        populacao = explosao_diversidade(
                            melhor_cromossomo, len(populacao), fitness
                        )

                        # Adição de variações especializadas
                        if regra_pendente:
                            variacoes_especializadas = (
                                forcar_variacoes_regra_especifica(
                                    melhor_cromossomo, regra_pendente, 200
                                )
                            )
                            populacao.extend(variacoes_especializadas)

                        # Recálculo após diversificação
                        valores_fitness = [
                            fitness(cromossomo) for cromossomo in populacao
                        ]
                        melhor_fitness = max(valores_fitness)
                        melhor_cromossomo = populacao[
                            valores_fitness.index(melhor_fitness)
                        ]

                        # Reset de contadores após intervenção
                        if regra_pendente == 5:
                            self.geracoes_no_fitness_14 = 0
                            self.geracoes_sem_melhoria = 0

                        print(
                            f"   Diversificação concluída: Nova fitness máxima = {melhor_fitness}/15"
                        )

                # Debug ultra-detalhado para casos extremos
                if melhor_fitness == 14 and self.geracoes_no_fitness_14 > 0:
                    if self.geracoes_no_fitness_14 % 100 == 0:
                        print(
                            f"\nANÁLISE CIENTÍFICA APROFUNDADA - Estagnação de {self.geracoes_no_fitness_14} gerações"
                        )
                        ultra_debug_falha_mutacao(
                            melhor_cromossomo, fitness, regra_pendente, 500
                        )

            # === OPERAÇÕES GENÉTICAS AVANÇADAS ===

            # Estratégia de diversificação populacional geral
            if self.geracoes_sem_melhoria > 1000:
                if melhor_fitness >= 14:
                    # Para alta fitness: diversificação conservadora
                    elite_preservada = int(len(populacao) * 0.15)  # 15% elite
                    print(
                        f"   {geracao:7d} | {melhor_fitness:2d}/15   | {len(populacao):6d} | {percentual_diversidade:3.0f}% | {tempo_decorrido:6.1f}s | Diversificação conservadora (preserva 15% elite)"
                    )
                else:
                    # Para baixa fitness: diversificação agressiva
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

            # === PROCESSO DE SELEÇÃO E REPRODUÇÃO ===

            # Seleção da elite para sobrevivência (10%)
            taxa_sobrevivencia = 0.10
            numero_sobreviventes = int(len(populacao) * taxa_sobrevivencia)
            elite_sobrevivente = populacao[:numero_sobreviventes]

            # Aplicação de busca local na elite de alta fitness
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

            # Geração de descendentes via reprodução
            descendentes = []
            taxa_imigracao = 0.15
            numero_descendentes = (
                len(populacao)
                - numero_sobreviventes
                - int(len(populacao) * taxa_imigracao)
            )

            # Descendentes de elite (estratégia especializada para alta fitness)
            if melhor_fitness >= 13:
                descendentes_elite_count = int(numero_descendentes * 0.2)
                descendentes_elite = criar_descendentes_elite(
                    populacao[:20], valores_fitness[:20], fitness
                )[:descendentes_elite_count]
                descendentes.extend(descendentes_elite)

            # Reprodução principal via seleção e crossover
            while len(descendentes) < numero_descendentes:
                # Seleção adaptativa de pais
                if melhor_fitness >= 14:
                    # Seleção por torneio restrita (busca local intensiva)
                    pai1 = selecao_torneio(populacao[:10], valores_fitness[:10], 3)
                    pai2 = selecao_torneio(populacao[:10], valores_fitness[:10], 3)
                elif melhor_fitness >= 13:
                    # Seleção por torneio moderada
                    pai1 = selecao_torneio(populacao[:50], valores_fitness[:50], 5)
                    pai2 = selecao_torneio(populacao[:50], valores_fitness[:50], 5)
                else:
                    # Seleção híbrida (exploração ampla)
                    pai1 = selecao_hibrida(populacao[:200], valores_fitness[:200])
                    pai2 = selecao_hibrida(populacao[:200], valores_fitness[:200])

                # Aplicação do operador de crossover
                if melhor_fitness >= 13:
                    filho1, filho2 = cruzamento_avancado(
                        pai1, pai2, self.taxa_cruzamento
                    )
                else:
                    filho1, filho2 = cruzamento(pai1, pai2, self.taxa_cruzamento)

                # Aplicação do operador de mutação inteligente
                regras_faltantes_f1 = obter_regras_faltantes(filho1)
                regras_faltantes_f2 = obter_regras_faltantes(filho2)

                filho1 = mutacao_inteligente(filho1, self.taxa_mutacao, fitness(filho1))
                filho2 = mutacao_inteligente(filho2, self.taxa_mutacao, fitness(filho2))

                # Mutação dirigida para cromossomos de alta fitness
                if melhor_fitness >= 12:
                    filho1 = mutacao_dirigida(filho1, regras_faltantes_f1)
                    filho2 = mutacao_dirigida(filho2, regras_faltantes_f2)

                descendentes.extend([filho1, filho2])

            # Processo de imigração (introdução de novos indivíduos)
            numero_imigrantes = int(len(populacao) * taxa_imigracao)
            imigrantes = self.criar_populacao_especializada(numero_imigrantes)

            # Formação da nova geração
            populacao = (
                elite_sobrevivente + descendentes[:numero_descendentes] + imigrantes
            )

            # Controle do tamanho populacional
            if len(populacao) > self.tamanho_populacao:
                populacao = populacao[: self.tamanho_populacao]

        # === APRESENTAÇÃO DOS RESULTADOS FINAIS ===
        self._apresentar_resultados_finais(
            melhor_cromossomo_global,
            melhor_fitness_global,
            geracao,
            tempo_inicio,
            tempo_atingiu_14,
        )

        return melhor_cromossomo_global, melhor_fitness_global

    def _apresentar_resultados_finais(
        self,
        melhor_cromossomo,
        melhor_fitness,
        geracoes_executadas,
        tempo_inicio,
        tempo_14,
    ):
        """Apresenta os resultados finais de forma acadêmica e estruturada."""
        print("\n" + "=" * 80)
        print("                    📊 RELATÓRIO FINAL DE RESULTADOS")
        print("=" * 80)

        mostrar_solucao(melhor_cromossomo)

        # Análise científica detalhada
        relatorio_detalhado = relatorio_detalhado_fitness(melhor_cromossomo)
        pontuacoes_parciais = pontuacoes_parciais_fitness(melhor_cromossomo)

        print(f"\n🔬 ANÁLISE CIENTÍFICA DOS RESULTADOS:")
        print(f"   Regras de satisfação cumpridas: {relatorio_detalhado['satisfied']}")
        if relatorio_detalhado["missing"]:
            print(
                f"   Regras pendentes de satisfação: {relatorio_detalhado['missing']}"
            )
        print(f"   Análise por categorias de restrições:")
        for categoria, pontuacao in pontuacoes_parciais.items():
            print(f"      • {categoria.capitalize()}: {pontuacao}")

        # Identificação da resposta do desafio
        print(f"\n🐟 RESPOSTA AO DESAFIO LÓGICO DE EINSTEIN:")
        for posicao, casa in enumerate(melhor_cromossomo, 1):
            if casa[4] == "Peixes":
                print(f"   🎯 Conclusão: O {casa[1]} possui os Peixes (Casa {posicao})")
                break

        # Métricas de performance computacional
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
    """Função principal para execução do algoritmo genético."""
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
