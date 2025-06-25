# Algoritmo Genético para o Desafio de Einstein

![Einstein Challenge](https://img.shields.io/badge/Puzzle-Einstein-blue)
![Genetic Algorithm](https://img.shields.io/badge/AI-Genetic%20Algorithm-green)
![Python](https://img.shields.io/badge/Language-Python-yellow)

Este projeto implementa um algoritmo genético para resolver o famoso "Desafio de Einstein", também conhecido como "Puzzle dos Peixes". Utilizando conceitos de inteligência artificial, o algoritmo evolui uma população de soluções candidatas até encontrar a configuração correta que satisfaça todas as 15 regras do desafio.

## 📋 O Desafio de Einstein

O desafio consiste em determinar quem é o dono dos peixes com base em 15 dicas lógicas. O problema envolve 5 casas de cores diferentes, onde moram pessoas de diferentes nacionalidades, que bebem diferentes bebidas, fumam diferentes cigarros e têm diferentes animais de estimação.

Regras básicas:
- Há 5 casas de diferentes cores
- Em cada casa mora uma pessoa de nacionalidade diferente
- Cada morador bebe uma bebida diferente, fuma um tipo de cigarro diferente e tem um animal de estimação diferente
- Nenhum morador compartilha qualquer característica com outro
- As 15 dicas devem ser usadas para determinar: quem tem os peixes?

## 🧬 Algoritmo Genético

O algoritmo genético implementado usa as seguintes características:

- **Representação cromossômica**: Cada cromossomo representa 5 casas com 5 atributos cada (cor, nacionalidade, bebida, cigarro, animal)
- **Função de fitness**: Conta quantas das 15 regras são satisfeitas
- **Operações genéticas**:
  - Seleção por roleta
  - Crossover (taxa: 80%)
  - Mutação (taxa: 5%)
  - Sobrevivência/Elitismo (10%)
  - Imigração (5%)
- **População**: 800 indivíduos
- **Critério de parada**: Quando todas as 15 regras são satisfeitas

## 🚀 Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/GabrielBeloDev/genetic-algorithm-einstein-challenge.git
   cd genetic-algorithm-einstein-challenge
   ```

2. Instale as dependências (se houver):
   ```bash
   pip install -r requirements.txt
   ```

3. Execute o algoritmo:
   ```bash
   python genetic_algorithm_einstein.py
   ```

## 📊 Estrutura do Projeto

```
genetic-algorithm-einstein-challenge/
│
├── genetic_algorithm_einstein.py  # Implementação principal
├── README.md                      # Este arquivo
├── requirements.txt              # Dependências do projeto
└── results/                      # Resultados das execuções
    ├── best_solutions.txt
    └── evolution_stats.csv
```

## 🔬 Detalhes da Implementação

### Representação dos Cromossomos

Cada cromossomo é representado como uma matriz 5x5, onde:
- Linhas representam as casas (1-5)
- Colunas representam os atributos (cor, nacionalidade, bebida, cigarro, animal)

### Função de Fitness

A função de fitness avalia quantas das 15 regras do desafio são satisfeitas:

1. O britânico mora na casa vermelha
2. O sueco tem um cachorro
3. O dinamarquês bebe chá
4. A casa verde fica à esquerda da casa branca
5. O morador da casa verde bebe café
6. A pessoa que fuma Pall Mall tem um pássaro
7. O morador da casa amarela fuma Dunhill
8. O morador da casa do meio bebe leite
9. O norueguês mora na primeira casa
10. O homem que fuma Blends mora ao lado do que tem gato
11. O homem que tem cavalos mora ao lado do que fuma Dunhill
12. O homem que fuma Blue Master bebe cerveja
13. O alemão fuma Prince
14. O norueguês mora ao lado da casa azul
15. O homem que fuma Blends tem um vizinho que bebe água

### Operadores Genéticos

#### Seleção
- **Método**: Seleção por roleta viciada
- **Objetivo**: Indivíduos com maior fitness têm maior probabilidade de serem selecionados

#### Crossover
- **Taxa**: 80%
- **Método**: Crossover de um ponto
- **Processo**: Troca de informações genéticas entre dois pais para gerar dois filhos

#### Mutação
- **Taxa**: 5%
- **Método**: Mutação aleatória de atributos
- **Objetivo**: Manter diversidade genética na população

#### Elitismo
- **Percentual**: 10%
- **Função**: Preserva os melhores indivíduos para a próxima geração

#### Imigração
- **Taxa**: 5%
- **Objetivo**: Introduz novos indivíduos aleatórios para evitar convergência prematura

## 📈 Resultados Esperados

O algoritmo tipicamente converge entre 50-200 gerações, dependendo da configuração inicial da população. A solução final mostra:

```
Casa 1: Amarela, Norueguês, Água, Dunhill, Gato
Casa 2: Azul, Dinamarquês, Chá, Blends, Cavalo
Casa 3: Vermelha, Britânico, Leite, Pall Mall, Pássaro
Casa 4: Verde, Alemão, Café, Prince, PEIXE
Casa 5: Branca, Sueco, Cerveja, Blue Master, Cachorro
```

**Resposta**: O alemão é o dono dos peixes!

## 🛠️ Personalização

Você pode ajustar os seguintes parâmetros no código:

```python
POPULATION_SIZE = 800      # Tamanho da população
CROSSOVER_RATE = 0.8       # Taxa de crossover
MUTATION_RATE = 0.05       # Taxa de mutação
ELITISM_RATE = 0.1         # Taxa de elitismo
IMMIGRATION_RATE = 0.05    # Taxa de imigração
MAX_GENERATIONS = 1000     # Máximo de gerações
```

## 📝 Logs e Monitoramento

O algoritmo gera logs detalhados incluindo:
- Progresso por geração
- Melhor fitness encontrado
- Diversidade da população
- Tempo de execução
- Estatísticas de convergência

## 🤝 Contribuições

Contribuições são bem-vindas! Algumas ideias para melhorias:

- [ ] Implementar diferentes estratégias de seleção
- [ ] Adicionar visualização gráfica da evolução
- [ ] Otimizar a função de fitness
- [ ] Implementar algoritmos de otimização alternativos
- [ ] Adicionar testes unitários

## 📚 Referências

- [Algoritmos Genéticos - Conceitos Fundamentais](https://example.com)
- [Einstein's Riddle - Wikipedia](https://en.wikipedia.org/wiki/Zebra_Puzzle)
- [Genetic Algorithms in Python](https://example.com)

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Gabriel Belo**
- GitHub: [@GabrielBeloDev](https://github.com/GabrielBeloDev)
- LinkedIn: [Gabriel Belo](www.linkedin.com/in/gabriel--belo

)

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!