"""
Módulo do Algoritmo Genético para resolver o Desafio de Einstein
Implementamos operadores genéticos e estratégias de busca local
"""

import random
import copy
from typing import List, Tuple, Callable


CORES = ["Vermelha", "Verde", "Branca", "Amarela", "Azul"]
NACIONALIDADES = ["Inglês", "Sueco", "Dinamarquês", "Norueguês", "Alemão"]
BEBIDAS = ["Chá", "Café", "Leite", "Cerveja", "Água"]
CIGARROS = ["Pall Mall", "Dunhill", "Blends", "BlueMaster", "Prince"]
ANIMAIS = ["Cachorros", "Pássaros", "Gatos", "Cavalos", "Peixes"]


# método para gerar um cromossomo aleatório para uma config válida
def cromossomo_aleatorio() -> List[Tuple[str, str, str, str, str]]:
    cores = CORES.copy()
    nacionalidades = NACIONALIDADES.copy()
    bebidas = BEBIDAS.copy()
    cigarros = CIGARROS.copy()
    animais = ANIMAIS.copy()

    random.shuffle(cores)
    random.shuffle(nacionalidades)
    random.shuffle(bebidas)
    random.shuffle(cigarros)
    random.shuffle(animais)

    return [
        (cores[i], nacionalidades[i], bebidas[i], cigarros[i], animais[i])
        for i in range(5)
    ]


# método para mutar um cromossomo com uma taxa de aleatória // args: cromossomo(config atual das casas) e taxa de mutação / return dess metodo é o cromossomo mutado
def mutacao(cromossomo: List[Tuple], taxa_mutacao: float) -> List[Tuple]:
    if random.random() > taxa_mutacao:
        return cromossomo

    novo_cromossomo = [list(casa) for casa in cromossomo]

    casa1, casa2 = random.sample(range(5), 2)  # escolhe duas casas aleatórias

    caracteristica = random.randint(0, 4)  # '' config aleatória

    # trocou a característica entre as duas casas
    novo_cromossomo[casa1][caracteristica], novo_cromossomo[casa2][caracteristica] = (
        novo_cromossomo[casa2][caracteristica],
        novo_cromossomo[casa1][caracteristica],
    )

    return [tuple(casa) for casa in novo_cromossomo]


# metodo adaptativo para mutação no current fitness, baseado em tecnicas de comp paralela com mpi e openmp / para cromossomo de alto fitness aplica mutações suaves e para cromossomo de baixo fitness aplica mutação padrão
def mutacao_inteligente(
    cromossomo: List[Tuple], taxa_mutacao: float, fitness_atual: int
) -> List[Tuple]:
    if random.random() > taxa_mutacao:
        return cromossomo

    resultado = cromossomo

    if fitness_atual >= 13:
        numero_mutacoes = random.randint(2, 4)
        for _ in range(numero_mutacoes):
            resultado = mutacao(resultado, 0.3)
    else:
        resultado = mutacao(resultado, 1.0)

    return resultado


# metodo para mutação dirigida que foca nas regras que ainda não foram satisfeitas // tenta priorizar regras de maior peso para melhorar essa resolução.
def mutacao_dirigida(
    cromossomo: List[Tuple], regras_faltantes: List[int]
) -> List[Tuple]:

    if not regras_faltantes:
        return cromossomo

    novo_cromossomo = [list(casa) for casa in cromossomo]

    # regras de vizinhança / maior peso
    regras_vizinhanca = [10, 11, 14, 15]
    regras_prioritarias = [r for r in regras_faltantes if r in regras_vizinhanca]

    if regras_prioritarias:
        # para regras de maior peso ponderado, tenta reorganizar casas vizinhas
        for _ in range(2):
            posicao = random.randint(0, 3)
            if random.random() < 0.5:
                # troca característica entre casas adjacentes para melhor tentativa de resolver
                caracteristica = random.randint(0, 4)
                (
                    novo_cromossomo[posicao][caracteristica],
                    novo_cromossomo[posicao + 1][caracteristica],
                ) = (
                    novo_cromossomo[posicao + 1][caracteristica],
                    novo_cromossomo[posicao][caracteristica],
                )
    else:
        casa1, casa2 = random.sample(
            range(5), 2
        )  # para outras regras, aplica mutação padrão
        caracteristica = random.randint(0, 4)
        (
            novo_cromossomo[casa1][caracteristica],
            novo_cromossomo[casa2][caracteristica],
        ) = (
            novo_cromossomo[casa2][caracteristica],
            novo_cromossomo[casa1][caracteristica],
        )

    return [tuple(casa) for casa in novo_cromossomo]


# operador de cruzamento de um ponto aleatório // args: pai1 e pai2 e probabilidade de cruzamento / return: tupla com dois filhos gerados
def cruzamento(
    pai1: List[Tuple], pai2: List[Tuple], taxa_cruzamento: float
) -> Tuple[List[Tuple], List[Tuple]]:

    if random.random() > taxa_cruzamento:
        return pai1, pai2

    ponto_corte = random.randint(1, 4)

    filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
    filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]

    # reparacao para os cromossomos validos
    filho1 = reparar_cromossomo(filho1)
    filho2 = reparar_cromossomo(filho2)

    return filho1, filho2


# cruzamento uniforme com reparação inteligente, cada gene é herdado independentemente com 50% de probabilidade de cada pai
def cruzamento_avancado(
    pai1: List[Tuple], pai2: List[Tuple], taxa_cruzamento: float
) -> Tuple[List[Tuple], List[Tuple]]:
    if random.random() > taxa_cruzamento:
        return pai1, pai2

    filho1 = []
    filho2 = []

    for i in range(5):
        if random.random() < 0.5:
            filho1.append(pai1[i])
            filho2.append(pai2[i])
        else:
            filho1.append(pai2[i])
            filho2.append(pai1[i])

    # de novo, usei a funcao reparar_cromossomo para cromossomos válidos
    filho1 = reparar_cromossomo(filho1)
    filho2 = reparar_cromossomo(filho2)

    return filho1, filho2


# funcao para reparar cromossomos válidos, logo com cada característica apareça exatamente uma vez. // resolve tambem as duplicatas pela troca aleatória
def reparar_cromossomo(cromossomo: List[Tuple]) -> List[Tuple]:

    novo_cromossomo = [list(casa) for casa in cromossomo]

    for caracteristica_idx in range(5):
        valores_atuais = [casa[caracteristica_idx] for casa in novo_cromossomo]
        valores_unicos = list(set(valores_atuais))

        if len(valores_unicos) < 5:
            todos_valores = [CORES, NACIONALIDADES, BEBIDAS, CIGARROS, ANIMAIS][
                caracteristica_idx
            ]
            valores_faltantes = [v for v in todos_valores if v not in valores_unicos]

            contagem = {}
            for i, valor in enumerate(valores_atuais):
                if valor not in contagem:
                    contagem[valor] = []
                contagem[valor].append(i)

            # tenta substituir duplicatas por valores faltantes // estrategia para otimizacao 14/15
            idx_faltante = 0
            for valor, posicoes in contagem.items():
                if len(posicoes) > 1:
                    # mantém a ocorrencia certa e substitui as outras
                    for pos in posicoes[1:]:
                        if idx_faltante < len(valores_faltantes):
                            novo_cromossomo[pos][caracteristica_idx] = (
                                valores_faltantes[idx_faltante]
                            )
                            idx_faltante += 1

    return [tuple(casa) for casa in novo_cromossomo]


# seleção por roleta baseada no fitness (proporcional a ele) // diversificação - exploração ampla
def selecao_roleta(
    populacao: List[List[Tuple]], valores_fitness: List[int]
) -> List[Tuple]:
    if not valores_fitness or max(valores_fitness) == 0:
        return random.choice(populacao)

    fitness_ajustado = [
        max(0, f) + 1 for f in valores_fitness
    ]  # valores positivos para a roleta
    fitness_total = sum(fitness_ajustado)

    r = random.uniform(0, fitness_total)
    acumulado = 0

    for i, fitness in enumerate(fitness_ajustado):
        acumulado += fitness
        if acumulado >= r:
            return populacao[i]

    return populacao[-1]


# seleção por torneio com tamanho configurável // args: populacao e valores de fitness e tamanho do torneio - numero de individuos competindo ( maior = mais seletivo)
# return com o maior fitness --  melhor_indice // conceito de intensificação: busca local -  mais elitista, pode convergir mais rapido
def selecao_torneio(
    populacao: List[List[Tuple]], valores_fitness: List[int], tamanho_torneio: int = 5
) -> List[Tuple]:
    if len(populacao) < tamanho_torneio:
        tamanho_torneio = len(populacao)

    indices_torneio = random.sample(range(len(populacao)), tamanho_torneio)

    melhor_indice = max(indices_torneio, key=lambda i: valores_fitness[i])
    return populacao[melhor_indice]


# seleção hibrida adaptativa -- nesse caso, a seleção é feita com base na combinacao de torneio e roleta baseada na qualidade da população
# alto fitness máximo: torneio pequeno (intensificação)
# baixo fitness máximo: roleta (diversificação)
def selecao_hibrida(
    populacao: List[List[Tuple]], valores_fitness: List[int]
) -> List[Tuple]:
    fitness_maximo = max(valores_fitness) if valores_fitness else 0

    if fitness_maximo >= 14:
        return selecao_torneio(populacao, valores_fitness, 3)
    elif fitness_maximo >= 13:
        return selecao_torneio(populacao, valores_fitness, 5)
    elif fitness_maximo >= 10:
        return selecao_torneio(populacao, valores_fitness, 7)
    else:
        return selecao_roleta(populacao, valores_fitness)


# busca local tipo hill-climbing (um algoritmo de busca local que se inspira na escalada ao pico de uma montanha,encontrar a melhor solução a partir de um conjunto de soluções possíveis.
# Para esse caso do refinamento de soluções,eficaz para cromossomos com fitness ≥ 13, ele explora sistematicamente vizinhanças através de trocas pequenas.
def busca_local(
    cromossomo: List[Tuple], funcao_fitness: Callable, max_iteracoes: int = 50
) -> List[Tuple]:
    melhor_cromossomo = cromossomo
    melhor_fitness = funcao_fitness(cromossomo)

    for _ in range(max_iteracoes):
        vizinho = gerar_vizinho(
            melhor_cromossomo
        )  # gera vizinho através de pequena perturbação
        fitness_vizinho = funcao_fitness(vizinho)

        if fitness_vizinho > melhor_fitness:  # so vai aceitar se tem a melhoria
            melhor_cromossomo = vizinho
            melhor_fitness = fitness_vizinho

            if melhor_fitness == 15:  # achou o resultado, para o loop
                break

    return melhor_cromossomo


# gera vizinho através de uma pequena modificação aleatória, troca entre casas adjacentes ou troca de característica específica.
def gerar_vizinho(cromossomo: List[Tuple]) -> List[Tuple]:
    novo_cromossomo = [list(casa) for casa in cromossomo]

    estrategia = random.choice(
        ["troca_adjacente", "troca_caracteristica", "troca_aleatoria"]
    )

    if estrategia == "troca_adjacente" and len(novo_cromossomo) > 1:
        posicao = random.randint(0, 3)  # troca entre casas adjacentes
        caracteristica = random.randint(0, 4)
        (
            novo_cromossomo[posicao][caracteristica],
            novo_cromossomo[posicao + 1][caracteristica],
        ) = (
            novo_cromossomo[posicao + 1][caracteristica],
            novo_cromossomo[posicao][caracteristica],
        )

    elif estrategia == "troca_caracteristica":
        casa1, casa2 = random.sample(
            range(5), 2
        )  # Troca uma característica específica entre duas casas quaisquer
        caracteristica = random.randint(0, 4)
        (
            novo_cromossomo[casa1][caracteristica],
            novo_cromossomo[casa2][caracteristica],
        ) = (
            novo_cromossomo[casa2][caracteristica],
            novo_cromossomo[casa1][caracteristica],
        )

    else:  # troca_aleatoria
        # mutação padrão
        casa1, casa2 = random.sample(range(5), 2)
        caracteristica = random.randint(0, 4)
        (
            novo_cromossomo[casa1][caracteristica],
            novo_cromossomo[casa2][caracteristica],
        ) = (
            novo_cromossomo[casa2][caracteristica],
            novo_cromossomo[casa1][caracteristica],
        )

    return [tuple(casa) for casa in novo_cromossomo]


# cria descendentes de alta qualidade através de cruzamento dirigido da elite
# 1. Seleciona pais de alto fitness
# 2. Aplica cruzamento avançado
# 3. Refinamento via busca local
def criar_descendentes_elite(
    populacao_elite: List[List[Tuple]],
    valores_fitness: List[int],
    funcao_fitness: Callable,
) -> List[List[Tuple]]:
    descendentes = []

    if len(populacao_elite) < 2:  # população minima para operação
        return descendentes

    for _ in range(min(20, len(populacao_elite))):
        pai1 = selecao_torneio(
            populacao_elite, valores_fitness, 3
        )  # seleção dirigida: prioriza indivíduos de alto fitness
        pai2 = selecao_torneio(populacao_elite, valores_fitness, 3)

        filho1, filho2 = cruzamento_avancado(
            pai1, pai2, 0.95
        )  # cruzamento avançado com alta probabilidade

        filho1 = busca_local(filho1, funcao_fitness, 10)  # busca hill-climbing
        filho2 = busca_local(filho2, funcao_fitness, 10)

        descendentes.extend([filho1, filho2])

    return descendentes


# mutação especializada para resolver a Regra 5 (otimizacao)
def mutacao_especializada_regra5(cromossomo: List[Tuple]) -> List[Tuple]:

    novo_cromossomo = [list(casa) for casa in cromossomo]

    posicoes_validas = [(0, 1), (1, 2), (2, 3), (3, 4)]
    pos_verde, pos_branca = random.choice(posicoes_validas)

    cor_atual_verde = novo_cromossomo[pos_verde][0]
    cor_atual_branca = novo_cromossomo[pos_branca][0]

    pos_atual_verde = next(
        (i for i, casa in enumerate(novo_cromossomo) if casa[0] == "Verde"), -1
    )
    pos_atual_branca = next(
        (i for i, casa in enumerate(novo_cromossomo) if casa[0] == "Branca"), -1
    )

    if pos_atual_verde != -1:
        novo_cromossomo[pos_atual_verde][0] = cor_atual_verde
    if pos_atual_branca != -1:
        novo_cromossomo[pos_atual_branca][0] = cor_atual_branca

    novo_cromossomo[pos_verde][0] = "Verde"
    novo_cromossomo[pos_branca][0] = "Branca"

    return [tuple(casa) for casa in novo_cromossomo]


# debug
def debug_status_regra5(cromossomo: List[Tuple]) -> dict:

    cores_casas = [casa[0] for casa in cromossomo]

    pos_verde = next((i for i, cor in enumerate(cores_casas) if cor == "Verde"), -1)
    pos_branca = next((i for i, cor in enumerate(cores_casas) if cor == "Branca"), -1)

    info = {
        "sequencia_cores": cores_casas,
        "posicao_verde": pos_verde + 1 if pos_verde != -1 else None,
        "posicao_branca": pos_branca + 1 if pos_branca != -1 else None,
        "regra5_satisfeita": False,
        "diferenca_posicoes": None,
        "configuracao_valida": False,
    }

    if pos_verde != -1 and pos_branca != -1:
        info["diferenca_posicoes"] = pos_branca - pos_verde
        info["regra5_satisfeita"] = pos_branca == pos_verde + 1
        info["configuracao_valida"] = True

    return info


# reparacao intensiva (otimizacao) // tenta múltiplas configurações Verde-Branca sequenciais até encontrar uma válida.
def reparacao_intensiva_regra5(
    cromossomo: List[Tuple], max_tentativas: int = 100
) -> List[Tuple]:

    melhor_cromossomo = cromossomo

    for _ in range(max_tentativas):
        candidato = mutacao_especializada_regra5(cromossomo)

        debug_info = debug_status_regra5(candidato)
        if debug_info["regra5_satisfeita"]:
            melhor_cromossomo = candidato
            break

    return melhor_cromossomo


# caso o debug e a mutação inteligente falhe, força a configuração Verde-Branca sequencial // teste explicitamente para todas as posições possíveis
def forca_bruta_regra5(
    cromossomo: List[Tuple], funcao_fitness: Callable
) -> List[List[Tuple]]:

    configuracoes_geradas = []
    posicoes_verde_branca = [(0, 1), (1, 2), (2, 3), (3, 4)]

    for pos_verde, pos_branca in posicoes_verde_branca:
        candidato = [list(casa) for casa in cromossomo]

        cor_original_verde = candidato[pos_verde][0]
        cor_original_branca = candidato[pos_branca][0]

        pos_atual_verde = next(
            (i for i, casa in enumerate(candidato) if casa[0] == "Verde"), -1
        )
        pos_atual_branca = next(
            (i for i, casa in enumerate(candidato) if casa[0] == "Branca"), -1
        )

        if pos_atual_verde != -1 and pos_atual_verde != pos_verde:
            candidato[pos_atual_verde][0] = cor_original_verde
        if pos_atual_branca != -1 and pos_atual_branca != pos_branca:
            candidato[pos_atual_branca][0] = cor_original_branca

        candidato[pos_verde][0] = "Verde"
        candidato[pos_branca][0] = "Branca"

        candidato_final = [tuple(casa) for casa in candidato]
        configuracoes_geradas.append(candidato_final)

    return configuracoes_geradas


# analise científica completa de um cromossomo // retorna um dicionário com métricas de qualidade e satisfação de restrições
def analisar_cromossomo_detalhado(
    cromossomo: List[Tuple], funcao_fitness: Callable
) -> dict:

    fitness_total = funcao_fitness(cromossomo)

    analise = {
        "fitness_total": fitness_total,
        "configuracao": cromossomo,
        "cores": [casa[0] for casa in cromossomo],
        "nacionalidades": [casa[1] for casa in cromossomo],
        "bebidas": [casa[2] for casa in cromossomo],
        "cigarros": [casa[3] for casa in cromossomo],
        "animais": [casa[4] for casa in cromossomo],
        "validacao_estrutural": {
            "cores_unicas": len(set(casa[0] for casa in cromossomo)) == 5,
            "nacionalidades_unicas": len(set(casa[1] for casa in cromossomo)) == 5,
            "bebidas_unicas": len(set(casa[2] for casa in cromossomo)) == 5,
            "cigarros_unicos": len(set(casa[3] for casa in cromossomo)) == 5,
            "animais_unicos": len(set(casa[4] for casa in cromossomo)) == 5,
        },
    }

    return analise


# debug específico para cada regra individual - 1 a 15 // retorna um dicionário com análise detalhada da regra específica
def debug_regra_especifica(cromossomo: List[Tuple], numero_regra: int) -> dict:

    descricoes_regras = {
        1: "O Norueguês vive na primeira casa",
        2: "O Inglês vive na casa Vermelha",
        3: "O Sueco tem Cachorros",
        4: "O Dinamarquês bebe Chá",
        5: "A casa Verde fica do lado esquerdo da casa Branca",
        6: "O homem que vive na casa Verde bebe Café",
        7: "O homem que fuma Pall Mall cria Pássaros",
        8: "O homem que vive na casa Amarela fuma Dunhill",
        9: "O homem que vive na casa do meio bebe Leite",
        10: "O homem que fuma Blends vive ao lado do que tem Gatos",
        11: "O homem que cria Cavalos vive ao lado do que fuma Dunhill",
        12: "O homem que fuma BlueMaster bebe Cerveja",
        13: "O Alemão fuma Prince",
        14: "O Norueguês vive ao lado da casa Azul",
        15: "O homem que fuma Blends é vizinho do que bebe Água",
    }

    analise = {
        "numero_regra": numero_regra,
        "description": descricoes_regras.get(numero_regra, "Regra desconhecida"),
        "detailed_analysis": "Análise específica em desenvolvimento",
    }

    # Análise específica para Regra 5 (Verde-Branca) -- apos validacao de debug e mutacao inteligente, força a configuração Verde-Branca sequencial
    if numero_regra == 5:
        debug_r5 = debug_status_regra5(cromossomo)
        analise["detailed_analysis"] = (
            f"Verde na posição {debug_r5['posicao_verde']}, Branca na posição {debug_r5['posicao_branca']}. "
            f"Diferença: {debug_r5['diferenca_posicoes']}. Sequência: {debug_r5['sequencia_cores']}"
        )

    # Análise para regra 14 regras críticas
    elif numero_regra == 14:  # Norueguês vizinho da casa Azul
        pos_noruegues = next(
            (i for i, casa in enumerate(cromossomo) if casa[1] == "Norueguês"), -1
        )
        pos_azul = next(
            (i for i, casa in enumerate(cromossomo) if casa[0] == "Azul"), -1
        )
        analise["detailed_analysis"] = (
            f"Norueguês na posição {pos_noruegues+1 if pos_noruegues != -1 else 'N/A'}, "
            f"Casa Azul na posição {pos_azul+1 if pos_azul != -1 else 'N/A'}"
        )

    return analise


# imprime representação visual limpa do cromossomo para análise
def imprimir_cromossomo_visual(cromossomo: List[Tuple]) -> None:

    print("\nCONFIGURAÇÃO DAS CASAS:")
    print("-" * 80)
    print(
        f"{'Casa':<6} {'Cor':<10} {'Nacionalidade':<12} {'Bebida':<8} {'Cigarro':<12} {'Animal':<10}"
    )
    print("-" * 80)

    for i, casa in enumerate(cromossomo, 1):
        cor, nacionalidade, bebida, cigarro, animal = casa
        print(
            f"{i:<6} {cor:<10} {nacionalidade:<12} {bebida:<8} {cigarro:<12} {animal:<10}"
        )
    print("-" * 80)


# analise dos melhores indivíduos da população
def analise_profunda_populacao(
    populacao: List[List[Tuple]], funcao_fitness: Callable, top_n: int = 5
) -> None:
    print(f"\nANÁLISE APROFUNDADA DOS TOP {top_n} INDIVÍDUOS:")
    print("=" * 60)

    populacao_ordenada = sorted(populacao, key=funcao_fitness, reverse=True)

    for i, cromossomo in enumerate(populacao_ordenada[:top_n], 1):
        fitness_atual = funcao_fitness(cromossomo)
        print(f"\nINDIVÍDUO {i} - Fitness: {fitness_atual}/15")
        print("-" * 40)

        analise = analisar_cromossomo_detalhado(cromossomo, funcao_fitness)

        # mostra configuração compacta
        for j, casa in enumerate(cromossomo, 1):
            print(
                f"Casa {j}: {casa[0]:<8} {casa[1]:<10} {casa[2]:<6} {casa[3]:<10} {casa[4]}"
            )

        if not all(analise["validacao_estrutural"].values()):
            print("AVISO: Cromossomo com estrutura inválida detectado!")


# apresenta a solução final
def mostrar_solucao(cromossomo: List[Tuple]) -> None:
    print("\nSOLUÇÃO ENCONTRADA:")
    print("=" * 50)

    imprimir_cromossomo_visual(cromossomo)
    for i, casa in enumerate(cromossomo, 1):
        if casa[4] == "Peixes":
            print(f"\nRESPOSTA: O {casa[1]} possui os Peixes (Casa {i})")
            break


def correcao_controlada_regra5(
    cromossomo: List[Tuple], tentativas: int = 50
) -> List[Tuple]:
    melhor_cromossomo = cromossomo

    for _ in range(tentativas):
        candidato = mutacao_especializada_regra5(cromossomo)

        if debug_status_regra5(candidato)["regra5_satisfeita"]:
            melhor_cromossomo = candidato
            break

    return melhor_cromossomo


# solucionador de emergência para casos extremos da Regra 5
def solucionador_emergencia_regra5(
    cromossomo: List[Tuple], funcao_fitness: Callable
) -> List[Tuple]:

    configuracoes_candidatas = forca_bruta_regra5(cromossomo, funcao_fitness)

    melhor_candidato = cromossomo
    melhor_fitness = funcao_fitness(cromossomo)

    for candidato in configuracoes_candidatas:
        fitness_candidato = funcao_fitness(candidato)
        if fitness_candidato > melhor_fitness:
            melhor_candidato = candidato
            melhor_fitness = fitness_candidato

    return melhor_candidato


# debug fail final, falhas persistentes na regra 5
def ultra_debug_falha_mutacao(
    cromossomo: List[Tuple],
    funcao_fitness: Callable,
    regra_problema: int,
    tentativas: int = 1000,
) -> None:
    print(f"\nULTRA DEBUG - REGRA {regra_problema}")
    print("=" * 50)

    fitness_inicial = funcao_fitness(cromossomo)
    print(f"Fitness inicial: {fitness_inicial}/15")

    imprimir_cromossomo_visual(cromossomo)

    if regra_problema == 5:
        debug_r5 = debug_status_regra5(cromossomo)
        print(f"\nStatus Regra 5: {debug_r5}")

        print(f"\nTestando {tentativas} mutações especializadas...")
        sucessos = 0

        for i in range(tentativas):
            candidato = mutacao_especializada_regra5(cromossomo)
            if debug_status_regra5(candidato)["regra5_satisfeita"]:
                sucessos += 1

                if sucessos <= 3:
                    print(f"\nSucesso {sucessos}: Configuração encontrada")
                    imprimir_cromossomo_visual(candidato)
                    print(f"Fitness: {funcao_fitness(candidato)}/15")

        print(f"\nResultado: {sucessos}/{tentativas} mutações resolveram a Regra 5")


# analisa se a população está em estagnação (convergência prematura), retorna True se está estagnada
def analisar_estagnacao_populacao(
    populacao: List[List[Tuple]], funcao_fitness: Callable
) -> bool:
    fitness_values = [funcao_fitness(cromossomo) for cromossomo in populacao]
    fitness_maximo = max(fitness_values)

    # conta quantos indivíduos têm o fitness máximo
    count_maximo = fitness_values.count(fitness_maximo)

    # calcula diversidade única
    configuracoes_unicas = len(set(str(cromossomo) for cromossomo in populacao))
    percentual_diversidade = configuracoes_unicas / len(populacao)

    # critérios de estagnação
    estagnacao_por_fitness = (
        count_maximo / len(populacao) > 0.7
    )  # 70% com mesmo fitness
    estagnacao_por_diversidade = percentual_diversidade < 0.3  # Menos de 30% único

    return estagnacao_por_fitness and estagnacao_por_diversidade


# estratégia de explosão de diversidade para escape de ótimos locais, cria nova população diversificada mantendo algumas cópias da melhor solução
def explosao_diversidade(
    melhor_cromossomo: List[Tuple], tamanho_populacao: int, funcao_fitness: Callable
) -> List[List[Tuple]]:
    nova_populacao = []

    # preserva algumas cópias do melhor cromossomo (5%)
    num_preservados = max(1, int(tamanho_populacao * 0.05))
    nova_populacao.extend([melhor_cromossomo] * num_preservados)

    # gera variações do melhor cromossomo (30%)
    num_variacoes = int(tamanho_populacao * 0.30)
    for _ in range(num_variacoes):
        variacao = melhor_cromossomo
        # tenativa de aplica múltiplas mutações para diversificar
        for _ in range(random.randint(2, 5)):
            variacao = mutacao(variacao, 0.8)
        nova_populacao.append(variacao)

    # preenche resto com cromossomos completamente aleatórios (65%)
    restantes = tamanho_populacao - len(nova_populacao)
    for _ in range(restantes):
        nova_populacao.append(cromossomo_aleatorio())

    return nova_populacao


# força variações específicas focadas em resolver uma regra particular
def forcar_variacoes_regra_especifica(
    cromossomo: List[Tuple], regra_numero: int, quantidade: int
) -> List[List[Tuple]]:
    variacoes = []

    for _ in range(quantidade):
        if regra_numero == 5:
            variacao = mutacao_especializada_regra5(cromossomo)
        else:
            # para outras regras, aplica mutação dirigida
            variacao = mutacao_dirigida(cromossomo, [regra_numero])

        variacoes.append(variacao)

    return variacoes
