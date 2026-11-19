"""PREENCHAM ESTE ARQUIVO: a conexão com a tela já está pronta.

As entradas já chegam validadas. Matrizes são listas de listas de números.
Não usem input(), Flask, NumPy ou JavaScript aqui.

Em cada função, substituam o `raise NotImplementedError` pelo algoritmo.
Retornem: {"resultado": sua_matriz_ou_numero, "passos": ["Explicação", ...]}.
`passos` é opcional; também é permitido retornar só a matriz ou o número.
As explicações devem descrever os cálculos que vocês realmente executaram.

Guia e exemplos de uso: docs/IMPLEMENTAR_MATRIZES.md.
"""


def somar(a, b):
    """Somar matrizes de mesmas dimensões. Retornar matriz desse tamanho."""
    linhas = len(a)
    colunas = len(a[0])
    resultado = []
    passos = []
    etapas = []

    passos.append(f"Somar duas matrizes {linhas}x{colunas} elemento a elemento.")

    for i in range(linhas):
        nova_linha = []
        for j in range(colunas):
            soma = a[i][j] + b[i][j]

            passos.append(f"a[{i}][{j}] + b[{i}][{j}] = {a[i][j]} + {b[i][j]} = {soma}")
            etapas.append(
                {
                    "linha": i,
                    "coluna": j,
                    "a": a[i][j],
                    "b": b[i][j],
                    "valor": soma,
                    "expressao": f"{a[i][j]} + ({b[i][j]}) = {soma}",
                    "explicacao": f"Some os elementos da linha {i + 1}, coluna {j + 1}, de A e B para preencher C.",
                }
            )
            nova_linha.append(soma)

        resultado.append(nova_linha)
    passos.append("Matriz resultante construida com sucesso.")
    return {
        "resultado": resultado,
        "passos": passos,
        "visualizacao": {
            "versao": 1,
            "tipo": "somar",
            "a": a,
            "b": b,
            "etapas": etapas,
        },
    }


def subtrair(a, b):
    """Calcular A - B, com dimensões iguais. Retornar uma matriz."""
    linhas = len(a)
    colunas = len(a[0])
    resultado = []
    passos = []
    etapas = []

    passos.append(
        f"Subtrair duas matrizes {linhas}x{colunas} elemento a elemento (A - B)."
    )

    for i in range(linhas):
        nova_linha = []
        for j in range(colunas):
            diferenca = a[i][j] - b[i][j]

            passos.append(
                f"a[{i}][{j}] - b[{i}][{j}] = {a[i][j]} - {b[i][j]} = {diferenca}"
            )
            etapas.append(
                {
                    "linha": i,
                    "coluna": j,
                    "a": a[i][j],
                    "b": b[i][j],
                    "valor": diferenca,
                    "expressao": f"{a[i][j]} - ({b[i][j]}) = {diferenca}",
                    "explicacao": f"Subtraia o elemento da linha {i + 1}, coluna {j + 1}, de B do elemento correspondente de A para preencher C.",
                }
            )
            nova_linha.append(diferenca)

        resultado.append(nova_linha)

    passos.append("Matriz resultante construida com sucesso.")
    return {
        "resultado": resultado,
        "passos": passos,
        "visualizacao": {
            "versao": 1,
            "tipo": "subtrair",
            "a": a,
            "b": b,
            "etapas": etapas,
        },
    }


def multiplicar(a, b):
    """Produto A(m×n) por B(n×p). Retornar matriz m×p."""
    linhas_a = len(a)
    colunas_a = len(a[0])
    linhas_b = len(b)
    colunas_b = len(b[0])
    resultado = []
    passos = []
    etapas = []

    passos.append(
        f"Multiplicar matriz {linhas_a}x{colunas_a} por matriz {linhas_b}x{colunas_b}."
    )

    for i in range(linhas_a):
        nova_linha = []
        for j in range(colunas_b):
            soma = 0
            produtos = []
            for k in range(colunas_a):
                prod = a[i][k] * b[k][j]
                soma += prod
                produtos.append(f"{a[i][k]}x{b[k][j]}")
            passos.append(f"C[{i}][{j}] = " + " + ".join(produtos) + f" = {soma}")

            etapas.append(
                {
                    "linha": i,
                    "coluna": j,
                    "a_linha": a[i],
                    "b_coluna": [b[k][j] for k in range(linhas_b)],
                    "produtos": [a[i][k] * b[k][j] for k in range(colunas_a)],
                    "valor": soma,
                    "expressao": " + ".join(produtos) + f" = {soma}",
                    "explicacao": f"Produto escalar da linha {i+1} de A com a coluna {j+1} de B.",
                }
            )

            nova_linha.append(soma)
        resultado.append(nova_linha)
    passos.append("Matriz resultante construida com sucesso.")
    return {
        "resultado": resultado,
        "passos": passos,
        "visualizacao": {
            "versao": 1,
            "tipo": "multiplicar",
            "a": a,
            "b": b,
            "etapas": etapas,
        },
    }


def transpor(a):
    """TODO: transposta de A(m×n). Retornar matriz n×m."""
    raise NotImplementedError("A transposta ainda não foi implementada.")


def determinante(a):
    """TODO: determinante de matriz quadrada 2×2 ou 3×3. Retornar um número."""
    raise NotImplementedError("O determinante ainda não foi implementado.")


def identidade(ordem):
    """TODO: criar identidade quadrada. `ordem` é inteiro de 1 a 8."""
    raise NotImplementedError("A matriz identidade ainda não foi implementada.")


def nula(linhas, colunas):
    """TODO: criar matriz nula. Dimensões são inteiros de 1 a 8."""
    raise NotImplementedError("A matriz nula ainda não foi implementada.")
