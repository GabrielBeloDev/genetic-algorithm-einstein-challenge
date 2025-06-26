"""
Módulo do Algoritmo Genético OTIMIZADO para resolver o Desafio de Einstein
Implementa operadores genéticos avançados e estratégias de busca local
"""

import random
import copy
from typing import List, Tuple, Callable

# ================== CROMOSSOMO E CODIFICAÇÃO ===================

# Definição das características de cada casa
CORES = ["Vermelha", "Verde", "Branca", "Amarela", "Azul"]
NACIONALIDADES = ["Inglês", "Sueco", "Dinamarquês", "Norueguês", "Alemão"]
BEBIDAS = ["Chá", "Café", "Leite", "Cerveja", "Água"]
CIGARROS = ["Pall Mall", "Dunhill", "Blends", "BlueMaster", "Prince"]
ANIMAIS = ["Cachorros", "Pássaros", "Gatos", "Cavalos", "Peixes"]


def cromossomo_aleatorio() -> List[Tuple[str, str, str, str, str]]:
    """
    Gera um cromossomo aleatório representando uma configuração válida.
    Cada casa é uma tupla: (cor, nacionalidade, bebida, cigarro, animal)
    """
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


# ==================== OPERADORES GENÉTICOS ====================


def mutacao(cromossomo: List[Tuple], taxa_mutacao: float) -> List[Tuple]:
    """
    Operador de mutação básico: troca aleatória de elementos entre casas.

    Args:
        cromossomo: Configuração atual das casas
        taxa_mutacao: Probabilidade de mutação

    Returns:
        Cromossomo após aplicação da mutação
    """
    if random.random() > taxa_mutacao:
        return cromossomo

    novo_cromossomo = [list(casa) for casa in cromossomo]

    # Escolhe duas casas aleatórias
    casa1, casa2 = random.sample(range(5), 2)

    # Escolhe uma característica aleatória (0=cor, 1=nacionalidade, etc.)
    caracteristica = random.randint(0, 4)

    # Troca a característica entre as duas casas
    novo_cromossomo[casa1][caracteristica], novo_cromossomo[casa2][caracteristica] = (
        novo_cromossomo[casa2][caracteristica],
        novo_cromossomo[casa1][caracteristica],
    )

    return [tuple(casa) for casa in novo_cromossomo]


def mutacao_inteligente(
    cromossomo: List[Tuple], taxa_mutacao: float, fitness_atual: int
) -> List[Tuple]:
    """
    Mutação adaptativa baseada no fitness atual.

    Para cromossomos de alto fitness (≥13), aplica múltiplas mutações pequenas
    para explorar finamente o espaço de soluções próximas.
    """
    if random.random() > taxa_mutacao:
        return cromossomo

    resultado = cromossomo

    if fitness_atual >= 13:
        # Para alto fitness: múltiplas mutações suaves
        numero_mutacoes = random.randint(2, 4)
        for _ in range(numero_mutacoes):
            resultado = mutacao(resultado, 0.3)
    else:
        # Para baixo fitness: mutação padrão
        resultado = mutacao(resultado, 1.0)

    return resultado


def mutacao_dirigida(
    cromossomo: List[Tuple], regras_faltantes: List[int]
) -> List[Tuple]:
    """
    Mutação dirigida que foca nas regras que ainda não foram satisfeitas.

    Estratégia acadêmica: Prioriza modificações que podem resolver regras específicas
    """
    if not regras_faltantes:
        return cromossomo

    novo_cromossomo = [list(casa) for casa in cromossomo]

    # Foca especialmente nas regras de vizinhança (10, 11, 14, 15)
    regras_vizinhanca = [10, 11, 14, 15]
    regras_prioritarias = [r for r in regras_faltantes if r in regras_vizinhanca]

    if regras_prioritarias:
        # Para regras de vizinhança, tenta reorganizar casas adjacentes
        for _ in range(2):
            posicao = random.randint(0, 3)  # Posições 0-3 para ter vizinhos
            if random.random() < 0.5:
                # Troca característica entre casas adjacentes
                caracteristica = random.randint(0, 4)
                (
                    novo_cromossomo[posicao][caracteristica],
                    novo_cromossomo[posicao + 1][caracteristica],
                ) = (
                    novo_cromossomo[posicao + 1][caracteristica],
                    novo_cromossomo[posicao][caracteristica],
                )
    else:
        # Para outras regras, aplica mutação padrão
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


def cruzamento(
    pai1: List[Tuple], pai2: List[Tuple], taxa_cruzamento: float
) -> Tuple[List[Tuple], List[Tuple]]:
    """
    Operador de cruzamento de um ponto.

    Args:
        pai1, pai2: Cromossomos pais
        taxa_cruzamento: Probabilidade de cruzamento

    Returns:
        Tupla com dois filhos gerados
    """
    if random.random() > taxa_cruzamento:
        return pai1, pai2

    ponto_corte = random.randint(1, 4)

    filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
    filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]

    # Reparação para garantir cromossomos válidos
    filho1 = reparar_cromossomo(filho1)
    filho2 = reparar_cromossomo(filho2)

    return filho1, filho2


def cruzamento_avancado(
    pai1: List[Tuple], pai2: List[Tuple], taxa_cruzamento: float
) -> Tuple[List[Tuple], List[Tuple]]:
    """
    Cruzamento uniforme com reparação inteligente.
    Cada gene é herdado independentemente com 50% de probabilidade de cada pai.
    """
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

    # Reparação essencial para cromossomos válidos
    filho1 = reparar_cromossomo(filho1)
    filho2 = reparar_cromossomo(filho2)

    return filho1, filho2


def reparar_cromossomo(cromossomo: List[Tuple]) -> List[Tuple]:
    """
    Repara um cromossomo garantindo que cada característica apareça exatamente uma vez.
    Resolve duplicatas através de trocas aleatórias.
    """
    novo_cromossomo = [list(casa) for casa in cromossomo]

    for caracteristica_idx in range(5):
        # Coleta valores atuais para esta característica
        valores_atuais = [casa[caracteristica_idx] for casa in novo_cromossomo]
        valores_unicos = list(set(valores_atuais))

        # Se há duplicatas, corrige
        if len(valores_unicos) < 5:
            todos_valores = [CORES, NACIONALIDADES, BEBIDAS, CIGARROS, ANIMAIS][
                caracteristica_idx
            ]
            valores_faltantes = [v for v in todos_valores if v not in valores_unicos]

            # Identifica posições com duplicatas
            contagem = {}
            for i, valor in enumerate(valores_atuais):
                if valor not in contagem:
                    contagem[valor] = []
                contagem[valor].append(i)

            # Substitui duplicatas por valores faltantes
            idx_faltante = 0
            for valor, posicoes in contagem.items():
                if len(posicoes) > 1:
                    # Mantém primeira ocorrência, substitui as outras
                    for pos in posicoes[1:]:
                        if idx_faltante < len(valores_faltantes):
                            novo_cromossomo[pos][caracteristica_idx] = (
                                valores_faltantes[idx_faltante]
                            )
                            idx_faltante += 1

    return [tuple(casa) for casa in novo_cromossomo]


# ===================== OPERADORES DE SELEÇÃO ===================


def selecao_roleta(
    populacao: List[List[Tuple]], valores_fitness: List[int]
) -> List[Tuple]:
    """
    Seleção por roleta russa baseada no fitness.
    Indivíduos com maior fitness têm maior probabilidade de seleção.
    """
    if not valores_fitness or max(valores_fitness) == 0:
        return random.choice(populacao)

    # Garante valores positivos para a roleta
    fitness_ajustado = [max(0, f) + 1 for f in valores_fitness]
    fitness_total = sum(fitness_ajustado)

    r = random.uniform(0, fitness_total)
    acumulado = 0

    for i, fitness in enumerate(fitness_ajustado):
        acumulado += fitness
        if acumulado >= r:
            return populacao[i]

    return populacao[-1]


def selecao_torneio(
    populacao: List[List[Tuple]], valores_fitness: List[int], tamanho_torneio: int = 5
) -> List[Tuple]:
    """
    Seleção por torneio com tamanho configurável.

    Args:
        tamanho_torneio: Número de indivíduos competindo (maior = mais seletivo)
    """
    if len(populacao) < tamanho_torneio:
        tamanho_torneio = len(populacao)

    indices_torneio = random.sample(range(len(populacao)), tamanho_torneio)

    melhor_indice = max(indices_torneio, key=lambda i: valores_fitness[i])
    return populacao[melhor_indice]


def selecao_hibrida(
    populacao: List[List[Tuple]], valores_fitness: List[int]
) -> List[Tuple]:
    """
    Seleção híbrida adaptativa.

    Combina torneio e roleta baseado na qualidade da população:
    - Alto fitness máximo: Torneio pequeno (intensificação)
    - Baixo fitness máximo: Roleta (diversificação)
    """
    fitness_maximo = max(valores_fitness) if valores_fitness else 0

    if fitness_maximo >= 14:
        return selecao_torneio(populacao, valores_fitness, 3)
    elif fitness_maximo >= 13:
        return selecao_torneio(populacao, valores_fitness, 5)
    elif fitness_maximo >= 10:
        return selecao_torneio(populacao, valores_fitness, 7)
    else:
        return selecao_roleta(populacao, valores_fitness)


# ==================== BUSCA LOCAL E REFINAMENTO ================


def busca_local(
    cromossomo: List[Tuple], funcao_fitness: Callable, max_iteracoes: int = 50
) -> List[Tuple]:
    """
    Busca local tipo hill-climbing para refinamento de soluções.

    Especialmente eficaz para cromossomos com fitness ≥ 13.
    Explora sistematicamente vizinhanças através de trocas pequenas.
    """
    melhor_cromossomo = cromossomo
    melhor_fitness = funcao_fitness(cromossomo)

    for _ in range(max_iteracoes):
        # Gera vizinho através de pequena perturbação
        vizinho = gerar_vizinho(melhor_cromossomo)
        fitness_vizinho = funcao_fitness(vizinho)

        # Aceita se houve melhoria
        if fitness_vizinho > melhor_fitness:
            melhor_cromossomo = vizinho
            melhor_fitness = fitness_vizinho

            # Se encontrou solução ótima, retorna imediatamente
            if melhor_fitness == 15:
                break

    return melhor_cromossomo


def gerar_vizinho(cromossomo: List[Tuple]) -> List[Tuple]:
    """
    Gera um vizinho através de uma pequena modificação aleatória.
    Estratégias: troca entre casas adjacentes ou troca de característica específica.
    """
    novo_cromossomo = [list(casa) for casa in cromossomo]

    estrategia = random.choice(
        ["troca_adjacente", "troca_caracteristica", "troca_aleatoria"]
    )

    if estrategia == "troca_adjacente" and len(novo_cromossomo) > 1:
        # Troca característica entre casas adjacentes
        posicao = random.randint(0, 3)
        caracteristica = random.randint(0, 4)
        (
            novo_cromossomo[posicao][caracteristica],
            novo_cromossomo[posicao + 1][caracteristica],
        ) = (
            novo_cromossomo[posicao + 1][caracteristica],
            novo_cromossomo[posicao][caracteristica],
        )

    elif estrategia == "troca_caracteristica":
        # Troca uma característica específica entre duas casas quaisquer
        casa1, casa2 = random.sample(range(5), 2)
        caracteristica = random.randint(0, 4)
        (
            novo_cromossomo[casa1][caracteristica],
            novo_cromossomo[casa2][caracteristica],
        ) = (
            novo_cromossomo[casa2][caracteristica],
            novo_cromossomo[casa1][caracteristica],
        )

    else:  # troca_aleatoria
        # Mutação padrão
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


# ================= ESTRATÉGIAS ESPECIALIZADAS ==================


def criar_descendentes_elite(
    populacao_elite: List[List[Tuple]],
    valores_fitness: List[int],
    funcao_fitness: Callable,
) -> List[List[Tuple]]:
    """
    Cria descendentes de alta qualidade através de cruzamento dirigido da elite.

    Metodologia:
    1. Seleciona pais de alto fitness
    2. Aplica cruzamento avançado
    3. Refinamento via busca local
    """
    descendentes = []

    # Garante população mínima para operação
    if len(populacao_elite) < 2:
        return descendentes

    for _ in range(min(20, len(populacao_elite))):
        # Seleção dirigida: prioriza indivíduos de alto fitness
        pai1 = selecao_torneio(populacao_elite, valores_fitness, 3)
        pai2 = selecao_torneio(populacao_elite, valores_fitness, 3)

        # Cruzamento avançado com alta probabilidade
        filho1, filho2 = cruzamento_avancado(pai1, pai2, 0.95)

        # Refinamento via busca local
        filho1 = busca_local(filho1, funcao_fitness, 10)
        filho2 = busca_local(filho2, funcao_fitness, 10)

        descendentes.extend([filho1, filho2])

    return descendentes


# ================= ESTRATÉGIAS PARA REGRA 5 ====================


def mutacao_especializada_regra5(cromossomo: List[Tuple]) -> List[Tuple]:
    """
    Mutação especializada para resolver a Regra 5: Casa Verde à esquerda da Casa Branca.

    Estratégia: Força configurações Verde-Branca em posições sequenciais válidas.
    """
    novo_cromossomo = [list(casa) for casa in cromossomo]

    # Posições válidas para Verde-Branca: (0,1), (1,2), (2,3), (3,4)
    posicoes_validas = [(0, 1), (1, 2), (2, 3), (3, 4)]
    pos_verde, pos_branca = random.choice(posicoes_validas)

    # Força cores Verde e Branca nas posições escolhidas
    cor_atual_verde = novo_cromossomo[pos_verde][0]
    cor_atual_branca = novo_cromossomo[pos_branca][0]

    # Encontra onde estão Verde e Branca atualmente
    pos_atual_verde = next(
        (i for i, casa in enumerate(novo_cromossomo) if casa[0] == "Verde"), -1
    )
    pos_atual_branca = next(
        (i for i, casa in enumerate(novo_cromossomo) if casa[0] == "Branca"), -1
    )

    # Realiza as trocas necessárias
    if pos_atual_verde != -1:
        novo_cromossomo[pos_atual_verde][0] = cor_atual_verde
    if pos_atual_branca != -1:
        novo_cromossomo[pos_atual_branca][0] = cor_atual_branca

    novo_cromossomo[pos_verde][0] = "Verde"
    novo_cromossomo[pos_branca][0] = "Branca"

    return [tuple(casa) for casa in novo_cromossomo]


def debug_status_regra5(cromossomo: List[Tuple]) -> dict:
    """
    Debug detalhado da Regra 5 para análise científica.

    Returns:
        Dicionário com análise completa da situação das cores Verde e Branca
    """
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


def reparacao_intensiva_regra5(
    cromossomo: List[Tuple], max_tentativas: int = 100
) -> List[Tuple]:
    """
    Reparação intensiva focada especificamente na Regra 5.

    Tenta múltiplas configurações Verde-Branca sequenciais até encontrar uma válida.
    """
    melhor_cromossomo = cromossomo

    for _ in range(max_tentativas):
        candidato = mutacao_especializada_regra5(cromossomo)

        # Verifica se a regra 5 foi satisfeita
        debug_info = debug_status_regra5(candidato)
        if debug_info["regra5_satisfeita"]:
            melhor_cromossomo = candidato
            break

    return melhor_cromossomo


def forca_bruta_regra5(
    cromossomo: List[Tuple], funcao_fitness: Callable
) -> List[List[Tuple]]:
    """
    Força bruta sistemática para todas as 4 configurações possíveis de Verde-Branca.

    Testa explicitamente todas as posições sequenciais válidas: (0,1), (1,2), (2,3), (3,4)
    """
    configuracoes_geradas = []
    posicoes_verde_branca = [(0, 1), (1, 2), (2, 3), (3, 4)]

    for pos_verde, pos_branca in posicoes_verde_branca:
        candidato = [list(casa) for casa in cromossomo]

        # Salva cores atuais das posições que serão modificadas
        cor_original_verde = candidato[pos_verde][0]
        cor_original_branca = candidato[pos_branca][0]

        # Encontra posições atuais de Verde e Branca
        pos_atual_verde = next(
            (i for i, casa in enumerate(candidato) if casa[0] == "Verde"), -1
        )
        pos_atual_branca = next(
            (i for i, casa in enumerate(candidato) if casa[0] == "Branca"), -1
        )

        # Realiza troca de cores
        if pos_atual_verde != -1 and pos_atual_verde != pos_verde:
            candidato[pos_atual_verde][0] = cor_original_verde
        if pos_atual_branca != -1 and pos_atual_branca != pos_branca:
            candidato[pos_atual_branca][0] = cor_original_branca

        # Força configuração Verde-Branca
        candidato[pos_verde][0] = "Verde"
        candidato[pos_branca][0] = "Branca"

        candidato_final = [tuple(casa) for casa in candidato]
        configuracoes_geradas.append(candidato_final)

    return configuracoes_geradas


# ================= ANÁLISE E DEBUG AVANÇADOS ===================


def analisar_cromossomo_detalhado(
    cromossomo: List[Tuple], funcao_fitness: Callable
) -> dict:
    """
    Análise científica completa de um cromossomo.

    Returns:
        Dicionário com métricas detalhadas de qualidade e satisfação de restrições
    """
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


def debug_regra_especifica(cromossomo: List[Tuple], numero_regra: int) -> dict:
    """
    Debug específico para uma regra individual.

    Args:
        numero_regra: Número da regra (1-15) para análise

    Returns:
        Dicionário com análise detalhada da regra específica
    """
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

    # Análise específica para Regra 5 (Verde-Branca)
    if numero_regra == 5:
        debug_r5 = debug_status_regra5(cromossomo)
        analise["detailed_analysis"] = (
            f"Verde na posição {debug_r5['posicao_verde']}, Branca na posição {debug_r5['posicao_branca']}. "
            f"Diferença: {debug_r5['diferenca_posicoes']}. Sequência: {debug_r5['sequencia_cores']}"
        )

    # Análise para outras regras críticas
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


def imprimir_cromossomo_visual(cromossomo: List[Tuple]) -> None:
    """
    Imprime representação visual limpa do cromossomo para análise.
    """
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


def analise_profunda_populacao(
    populacao: List[List[Tuple]], funcao_fitness: Callable, top_n: int = 5
) -> None:
    """
    Análise científica aprofundada dos melhores indivíduos da população.
    """
    print(f"\nANÁLISE APROFUNDADA DOS TOP {top_n} INDIVÍDUOS:")
    print("=" * 60)

    # Ordena população por fitness
    populacao_ordenada = sorted(populacao, key=funcao_fitness, reverse=True)

    for i, cromossomo in enumerate(populacao_ordenada[:top_n], 1):
        fitness_atual = funcao_fitness(cromossomo)
        print(f"\nINDIVÍDUO {i} - Fitness: {fitness_atual}/15")
        print("-" * 40)

        analise = analisar_cromossomo_detalhado(cromossomo, funcao_fitness)

        # Mostra configuração compacta
        for j, casa in enumerate(cromossomo, 1):
            print(
                f"Casa {j}: {casa[0]:<8} {casa[1]:<10} {casa[2]:<6} {casa[3]:<10} {casa[4]}"
            )

        # Validação estrutural
        if not all(analise["validacao_estrutural"].values()):
            print("AVISO: Cromossomo com estrutura inválida detectado!")


def mostrar_solucao(cromossomo: List[Tuple]) -> None:
    """
    Apresenta a solução final de forma clara e organizada.
    """
    print("\nSOLUÇÃO ENCONTRADA:")
    print("=" * 50)

    imprimir_cromossomo_visual(cromossomo)

    # Identifica quem tem os peixes
    for i, casa in enumerate(cromossomo, 1):
        if casa[4] == "Peixes":
            print(f"\nRESPOSTA: O {casa[1]} possui os Peixes (Casa {i})")
            break


# ================= ESTRATÉGIAS AVANÇADAS DE ESCAPE =============


def correcao_controlada_regra5(
    cromossomo: List[Tuple], tentativas: int = 50
) -> List[Tuple]:
    """
    Correção controlada específica para a Regra 5 com preservação de qualidade.
    """
    melhor_cromossomo = cromossomo

    for _ in range(tentativas):
        candidato = mutacao_especializada_regra5(cromossomo)

        # Preserva outras características de alta qualidade
        if debug_status_regra5(candidato)["regra5_satisfeita"]:
            melhor_cromossomo = candidato
            break

    return melhor_cromossomo


def solucionador_emergencia_regra5(
    cromossomo: List[Tuple], funcao_fitness: Callable
) -> List[Tuple]:
    """
    Solucionador de emergência para casos extremos da Regra 5.
    Tenta todas as configurações possíveis sistematicamente.
    """
    configuracoes_candidatas = forca_bruta_regra5(cromossomo, funcao_fitness)

    melhor_candidato = cromossomo
    melhor_fitness = funcao_fitness(cromossomo)

    for candidato in configuracoes_candidatas:
        fitness_candidato = funcao_fitness(candidato)
        if fitness_candidato > melhor_fitness:
            melhor_candidato = candidato
            melhor_fitness = fitness_candidato

    return melhor_candidato


def ultra_debug_falha_mutacao(
    cromossomo: List[Tuple],
    funcao_fitness: Callable,
    regra_problema: int,
    tentativas: int = 1000,
) -> None:
    """
    Debug ultra-detalhado para diagnóstico de falhas persistentes.
    """
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

                if sucessos <= 3:  # Mostra apenas os primeiros sucessos
                    print(f"\nSucesso {sucessos}: Configuração encontrada")
                    imprimir_cromossomo_visual(candidato)
                    print(f"Fitness: {funcao_fitness(candidato)}/15")

        print(f"\nResultado: {sucessos}/{tentativas} mutações resolveram a Regra 5")


def analisar_estagnacao_populacao(
    populacao: List[List[Tuple]], funcao_fitness: Callable
) -> bool:
    """
    Analisa se a população está em estagnação (convergência prematura).

    Returns:
        True se estagnação for detectada, False caso contrário
    """
    fitness_values = [funcao_fitness(cromossomo) for cromossomo in populacao]
    fitness_maximo = max(fitness_values)

    # Conta quantos indivíduos têm o fitness máximo
    count_maximo = fitness_values.count(fitness_maximo)

    # Calcula diversidade única
    configuracoes_unicas = len(set(str(cromossomo) for cromossomo in populacao))
    percentual_diversidade = configuracoes_unicas / len(populacao)

    # Critérios de estagnação
    estagnacao_por_fitness = (
        count_maximo / len(populacao) > 0.7
    )  # 70% com mesmo fitness
    estagnacao_por_diversidade = percentual_diversidade < 0.3  # Menos de 30% único

    return estagnacao_por_fitness and estagnacao_por_diversidade


def explosao_diversidade(
    melhor_cromossomo: List[Tuple], tamanho_populacao: int, funcao_fitness: Callable
) -> List[List[Tuple]]:
    """
    Estratégia de explosão de diversidade para escape de ótimos locais.

    Cria nova população diversificada mantendo algumas cópias da melhor solução.
    """
    nova_populacao = []

    # Preserva algumas cópias do melhor cromossomo (5%)
    num_preservados = max(1, int(tamanho_populacao * 0.05))
    nova_populacao.extend([melhor_cromossomo] * num_preservados)

    # Gera variações do melhor cromossomo (30%)
    num_variacoes = int(tamanho_populacao * 0.30)
    for _ in range(num_variacoes):
        variacao = melhor_cromossomo
        # Aplica múltiplas mutações para diversificar
        for _ in range(random.randint(2, 5)):
            variacao = mutacao(variacao, 0.8)
        nova_populacao.append(variacao)

    # Preenche resto com cromossomos completamente aleatórios (65%)
    restantes = tamanho_populacao - len(nova_populacao)
    for _ in range(restantes):
        nova_populacao.append(cromossomo_aleatorio())

    return nova_populacao


def forcar_variacoes_regra_especifica(
    cromossomo: List[Tuple], regra_numero: int, quantidade: int
) -> List[List[Tuple]]:
    """
    Força variações específicas focadas em resolver uma regra particular.
    """
    variacoes = []

    for _ in range(quantidade):
        if regra_numero == 5:
            variacao = mutacao_especializada_regra5(cromossomo)
        else:
            # Para outras regras, aplica mutação dirigida
            variacao = mutacao_dirigida(cromossomo, [regra_numero])

        variacoes.append(variacao)

    return variacoes
