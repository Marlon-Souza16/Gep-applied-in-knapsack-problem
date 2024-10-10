# Aplicação de Programação Genética de Expressões (GEP) na Solução do Problema da Mochila

Este documento apresenta a aplicação da **Programação Genética de Expressões (GEP)** para resolver o problema clássico da mochila. O objetivo é selecionar itens que maximizem o valor total sem exceder as restrições de peso (capacidade da mochila) e tempo disponível.

## Introdução ao Problema da Mochila

O problema da mochila consiste em uma coleção de itens, cada um com um peso, valor e tempo associados. A tarefa é escolher um subconjunto desses itens que maximize o valor total, respeitando as restrições de capacidade e tempo.

## Programação Genética de Expressões (GEP)

A GEP é uma técnica evolutiva que combina a programação genética com uma representação genotípica linear. Em vez de evoluir soluções diretamente, evoluímos expressões ou programas que, quando avaliados, produzem soluções para o problema.

## Representação das Expressões

As soluções são representadas como árvores de expressão, onde cada nó pode ser uma função (operador) ou um terminal (operando). Esta estrutura permite a criação de expressões matemáticas e lógicas complexas.

```python
# Funções e terminais utilizados na GEP
FUNCTIONS = ['+', '-', '*', '/', '>', '<', 'and', 'or']
TERMINALS = ['w', 'v', 't'] + [str(i) for i in range(-10, 11) if i != 0]
```

- Funções: Operadores aritméticos e lógicos que definem a estrutura da expressão.
- Terminais: Variáveis que representam propriedades dos itens (w para peso, v para valor, t para tempo) e constantes numéricas.

## Criação de Expressões Aleatórias

A geração inicial da população envolve a criação de expressões aleatórias com profundidade controlada para garantir diversidade e complexidade adequada.

```python
def create_random_expression(depth=0):
    if depth > GENOME_DEPTH or (depth > 0 and random.random() < 0.3):
        # Retorna um terminal (folha da árvore)
        return random.choice(TERMINALS)
    else:
        # Retorna um nó função com filhos recursivos
        func = random.choice(FUNCTIONS)
        return [func, create_random_expression(depth + 1), create_random_expression(depth + 1)]
```

## Avaliação das Expressões

```python
def evaluate_expression(expr, item_properties):
    if isinstance(expr, list):
        func = expr[0]
        arg1 = evaluate_expression(expr[1], item_properties)
        arg2 = evaluate_expression(expr[2], item_properties)
        # Executa a operação correspondente à função
        # ...
    else:
        # Retorna o valor do terminal (variável ou constante)
        return item_properties.get(expr, float(expr))
```

## Crossover
O crossover combina subestruturas de duas expressões parentais para criar uma nova expressão (filho).

```python
def crossover(expr1, expr2, depth=0):
    if random.random() < CROSSOVER_RATE and depth < GENOME_DEPTH:
        if isinstance(expr1, list) and isinstance(expr2, list):
            return expr2
        else:
            return expr1
    else:
        if isinstance(expr1, list) and isinstance(expr2, list):
            return [expr1[0],
                    crossover(expr1[1], expr2[1], depth + 1),
                    crossover(expr1[2], expr2[2], depth + 1)]
        else:
            return expr1
```

## Resultados:

### Best Solution Expression:

$((-8 > ((((8 - 10) > (2 + 2)) * (-8 * (7 > 10))) - (((-10 * v) * -3) and ((-7 * -6) + (v > -10))))) > (((w + (-10 / (-5 / -8))) > ((-8 and 8) + ((3 and 1) and -3))) / ((6 < t) < (-8 > ((v / -6) * (-4 * -3))))))$

### Selected Items:

- Weight: 4, Value: 5, Time: 4
- Weight: 5, Value: 8, Time: 5
- Weight: 4, Value: 7, Time: 4
- Weight: 2, Value: 6, Time: 2

### Total Weight: 15, Total Time: 15
