# Algoritmo Genético Avançado para o Desafio de Einstein

![Einstein Challenge](https://img.shields.io/badge/Puzzle-Einstein-blue)
![Genetic Algorithm](https://img.shields.io/badge/AI-Genetic%20Algorithm-green)
![Python](https://img.shields.io/badge/Language-Python-yellow)
![Advanced AI](https://img.shields.io/badge/AI-Advanced%20Techniques-red)

Este projeto implementa um **algoritmo genético otimizado e avançado** para resolver o famoso "Desafio de Einstein" (também conhecido como "Puzzle dos Peixes" ou "Zebra Puzzle"). O sistema utiliza técnicas avançadas de inteligência artificial, incluindo adaptação paramétrica dinâmica, estratégias de escape de ótimos locais, e análise profunda populacional.

## 📋 O Desafio de Einstein

O desafio lógico consiste em determinar **quem é o dono dos peixes** com base em 15 regras específicas. O problema envolve:

- **5 casas** de cores diferentes (Amarela, Azul, Vermelha, Verde, Branca)
- **5 nacionalidades** diferentes (Norueguês, Dinamarquês, Inglês, Alemão, Sueco)
- **5 bebidas** diferentes (Água, Chá, Leite, Café, Cerveja)
- **5 cigarros** diferentes (Dunhill, Blends, Pall Mall, Prince, BlueMaster)
- **5 animais** diferentes (Gatos, Cavalos, Pássaros, Cachorros, Peixes)

### As 15 Regras do Desafio

1. O Norueguês vive na primeira casa
2. O Inglês vive na casa Vermelha
3. O Sueco tem Cachorros
4. O Dinamarquês bebe Chá
5. A casa Verde fica do lado esquerdo da casa Branca
6. O homem que vive na casa Verde bebe Café
7. O homem que fuma Pall Mall cria Pássaros
8. O homem que vive na casa Amarela fuma Dunhill
9. O homem que vive na casa do meio bebe Leite
10. O homem que fuma Blends vive ao lado do que tem Gatos
11. O homem que cria Cavalos vive ao lado do que fuma Dunhill
12. O homem que fuma BlueMaster bebe Cerveja
13. O Alemão fuma Prince
14. O Norueguês vive ao lado da casa Azul
15. O homem que fuma Blends é vizinho do que bebe Água

## 🧬 Algoritmo Genético Avançado

Esta implementação utiliza um **algoritmo genético de última geração** com as seguintes características inovadoras:

### 🎯 Características Principais

- **População Adaptativa**: Começa com 1.800 indivíduos, podendo chegar a 5.000
- **Fitness Ponderado**: Regras críticas têm pesos maiores (vizinhança = 2.0x)
- **Adaptação Paramétrica Dinâmica**: Taxas ajustadas automaticamente baseadas no progresso
- **Estratégias Anti-Convergência**: Escape inteligente de ótimos locais
- **Análise Populacional Profunda**: Monitoramento de diversidade genética em tempo real

### 🔧 Operadores Genéticos Avançados

#### Seleção Híbrida

- **Seleção por Torneio**: Para alta qualidade (fitness ≥ 14)
- **Seleção Híbrida**: Combinação torneio + roleta para exploração
- **Seleção Adaptativa**: Estratégia baseada no fitness atual

#### Cruzamento Inteligente

- **Cruzamento Avançado**: Para soluções de alta qualidade (fitness ≥ 13)
- **Cruzamento Uniforme**: Com reparo automático de restrições
- **Taxa Adaptativa**: 80% a 95% baseada no progresso

#### Mutação Especializada

- **Mutação Inteligente**: Adaptada ao fitness atual
- **Mutação Dirigida**: Foco em regras não satisfeitas
- **Mutação Especializada**: Estratégias específicas para regras complexas
- **Taxa Dinâmica**: 15% a 40% baseada na fase evolutiva

#### Estratégias Avançadas

- **Busca Local**: Hill-climbing para refinamento
- **Elite Preservation**: Preservação dos melhores indivíduos
- **Explosão de Diversidade**: Para escape de convergência prematura
- **Força Bruta Especializada**: Para regras específicas (ex: Regra 5)

### 📊 Sistema de Fitness Multicamada

```python
# Fitness Simples
fitness_simples = contagem_regras_satisfeitas

# Fitness Ponderado (utilizado no algoritmo)
fitness_ponderado = soma(peso_regra * satisfeita_regra)

# Pesos das Regras
PESOS_REGRAS = {
    'simples': 1.0,        # Regras de atribuição direta
    'intermediária': 1.5,   # Regras sequenciais
    'crítica': 2.0         # Regras de vizinhança
}
```

## 🚀 Como Executar

### Pré-requisitos

```bash
Python 3.8+
```

### Execução

1. Clone o repositório:

   ```bash
   git clone https://github.com/GabrielBeloDev/genetic-algorithm-einstein-challenge.git
   cd genetic-algorithm-einstein-challenge
   ```

2. Execute o algoritmo:
   ```bash
   python src/main.py
   ```

## 📁 Estrutura do Projeto

```
genetic-algorithm-einstein-challenge/
│
├── src/
│   ├── __init__.py                 # Módulo Python
│   ├── main.py                     # Implementação principal do AG
│   ├── einstein_rules.py           # 15 regras + funções de fitness
│   └── genetic_algorithm.py        # Operadores genéticos avançados
│
├── docs/                          # Documentação (se houver)
├── README.md                      # Este arquivo
├── requirements.txt              # Dependências
└── .git/                         # Controle de versão
```

## 🔬 Detalhes Técnicos da Implementação

### Representação Cromossômica

```python
# Cromossomo = Lista de 5 casas
cromossomo = [
    (cor, nacionalidade, bebida, cigarro, animal),  # Casa 1
    (cor, nacionalidade, bebida, cigarro, animal),  # Casa 2
    (cor, nacionalidade, bebida, cigarro, animal),  # Casa 3
    (cor, nacionalidade, bebida, cigarro, animal),  # Casa 4
    (cor, nacionalidade, bebida, cigarro, animal),  # Casa 5
]
```

### Configuração Dinâmica do Algoritmo

```python
# Configuração Base
TAMANHO_POPULACAO_BASE = 1800
TAXA_CRUZAMENTO_BASE = 0.85
TAXA_MUTACAO_BASE = 0.15
TAMANHO_MAXIMO_POPULACAO = 5000

# Adaptação Automática Baseada no Fitness
if fitness >= 14:
    # Fase de Intensificação
    populacao_max = 5000
    taxa_mutacao = 0.4    # Mutação intensiva
    taxa_cruzamento = 0.95

elif fitness >= 13:
    # Fase de Convergência Guiada
    populacao_max = 4000
    taxa_mutacao = 0.25
    taxa_cruzamento = 0.90
```

### Estratégias de Otimização

#### Para Fitness ≥ 14 (Uma regra pendente)

- **Busca Dirigida**: Foco na regra não satisfeita
- **Busca Local Intensiva**: Hill-climbing com 30 iterações
- **Força Bruta Especializada**: Para regras específicas (ex: Regra 5)
- **Análise de Convergência**: Detecção de ótimos locais

#### Para Fitness < 13 (Múltiplas regras pendentes)

- **Diversificação Agressiva**: Explosão populacional
- **Imigração Controlada**: 15% de novos indivíduos por geração
- **Mutação Exploratória**: Taxa elevada para exploração

## 📈 Métricas e Análises

### Monitoramento em Tempo Real

- **Progresso Evolutivo**: Fitness por geração
- **Diversidade Populacional**: Percentual de configurações únicas
- **Análise de Convergência**: Detecção de estagnação
- **Distribuição de Regras**: Quais regras estão sendo problemas

### Relatórios Automáticos

```python
# Exemplo de saída do sistema
"""
📊 EVOLUÇÃO DO ALGORITMO:
   Geração | Fitness | Tamanho Pop | Diversidade | Tempo | Status Evolutivo
   -------------------------------------------------------------------------
      25   | 13/15   |   1800     |    78.5%    |  2.3s | Convergência intermediária
      50   | 14/15   |   2100     |    65.2%    |  4.7s | Refinamento: Regra 5 pendente
      75   | 15/15   |   2100     |    62.1%    |  7.1s | SOLUÇÃO ÓTIMA ENCONTRADA!
"""
```

## 🎯 Resultados Típicos

### Performance Computacional

- **Tempo Médio de Convergência**: 7-15 segundos
- **Gerações Típicas**: 50-200 gerações
- **Taxa de Sucesso**: ~95% para fitness = 15
- **Eficiência**: ~0.05-0.1s por geração

### Solução Final Típica

```
🏠 CONFIGURAÇÃO DA SOLUÇÃO:
┌──────────────────────────────────────────────────────────────────────────────┐
│CASA │ COR       │ NACIONALIDADE │ BEBIDA  │ CIGARRO    │ ANIMAL    │
├──────────────────────────────────────────────────────────────────────────────┤
│ 1   │ Amarela   │ Norueguês     │ Água    │ Dunhill    │ Gatos     │
│ 2   │ Azul      │ Dinamarquês   │ Chá     │ Blends     │ Cavalos   │
│ 3   │ Vermelha  │ Inglês        │ Leite   │ Pall Mall  │ Pássaros  │
│ 4   │ Verde     │ Alemão        │ Café    │ Prince     │ Peixes    │
│ 5   │ Branca    │ Sueco         │ Cerveja │ BlueMaster │ Cachorros │
└──────────────────────────────────────────────────────────────────────────────┘

🐟 RESPOSTA: O Alemão possui os Peixes!
```

## 🛠️ Personalização Avançada

### Parâmetros Configuráveis

```python
# Em main.py - Classe AlgoritmoGeneticoAvancado
TAMANHO_POPULACAO_BASE = 1800      # População inicial
TAXA_CRUZAMENTO_BASE = 0.85        # Taxa de cruzamento base
TAXA_MUTACAO_BASE = 0.15           # Taxa de mutação base
LIMITE_GERACOES = 1000             # Máximo de gerações

# Em einstein_rules.py - Pesos das regras
PESOS_REGRAS = {
    0: 1.0,   # r1 - simples
    9: 2.0,   # r10 - vizinhança (crítica)
    10: 2.0,  # r11 - vizinhança (crítica)
    # ... outros pesos
}
```

### Estratégias Experimentais

- **Teste de Força Bruta**: Para regras específicas
- **Análise de Estagnação**: Detecção automática de convergência prematura
- **Ultra Debug**: Análise profunda de falhas de mutação
- **Correção Controlada**: Reparação inteligente de regras específicas

## 📊 Análises Acadêmicas

### Categorização de Regras

- **Regras Simples** (peso 1.0): Atribuição direta de características
- **Regras de Posição** (peso 1.0): Localização fixa na sequência
- **Regras Sequenciais** (peso 1.5): Ordem específica entre elementos
- **Regras de Vizinhança** (peso 2.0): Adjacência entre casas

### Métricas de Qualidade

```python
relatorio_detalhado = {
    "score": 15,                    # Regras satisfeitas
    "satisfied": [1,2,3,...,15],    # Lista de regras OK
    "missing": [],                  # Lista de regras pendentes
    "weighted_score": 17.5          # Score ponderado
}
```

## 🤝 Contribuições

Áreas de pesquisa para contribuições:

- [ ] **Otimização de Hiperparâmetros**: Algoritmos de otimização bayesiana
- [ ] **Paralelização**: Implementação multi-threading/multi-processing
- [ ] **Visualização**: Interface gráfica para acompanhar evolução
- [ ] **Benchmarking**: Comparação com outros métodos (CSP, SAT, etc.)
- [ ] **Análise Estatística**: Estudos de convergência e robustez
- [ ] **Extensões**: Adaptação para outros puzzles lógicos

## 📚 Fundamentação Teórica

### Algoritmos Genéticos

- **Base Teórica**: Holland (1975), Goldberg (1989)
- **Operadores**: Seleção, Cruzamento, Mutação, Elitismo
- **Estratégias**: Nichos, Compartilhamento, Diversidade

### Problemas de Satisfação de Restrições (CSP)

- **Modelagem**: Variáveis, Domínios, Restrições
- **Técnicas**: Busca Local, Propagação de Restrições
- **Otimização**: Escape de Ótimos Locais

### Referências

- Holland, J. H. (1975). "Adaptation in Natural and Artificial Systems"
- Goldberg, D. E. (1989). "Genetic Algorithms in Search, Optimization and Machine Learning"
- Russell, S. & Norvig, P. (2020). "Artificial Intelligence: A Modern Approach"

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Gabriel Belo**

- GitHub: [@GabrielBeloDev](https://github.com/GabrielBeloDev)
- LinkedIn: [Gabriel Belo](https://www.linkedin.com/in/gabriel--belo)

---

**Disciplina**: Inteligência Artificial  
**Professor**: Tiago Bonini Borchartt  
**Instituição**: [Sua Instituição]

⭐ **Se este projeto foi útil para seus estudos ou pesquisa, considere dar uma estrela no repositório!**
