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
            etapas.append({"linha": i, "coluna": j, "a": a[i][j], "b": b[i][j], "valor": soma,
                           "expressao": f"{a[i][j]} + ({b[i][j]}) = {soma}",
                           "explicacao": f"Some os elementos da linha {i + 1}, coluna {j + 1}, de A e B para preencher C."})
            nova_linha.append(soma)

        resultado.append(nova_linha)
    passos.append("Matriz resultante construida com sucesso.")
    return {"resultado": resultado, "passos": passos, "visualizacao": {"versao": 1, "tipo": "somar", "a": a, "b": b, "etapas": etapas}}


def subtrair(a, b):
    """TODO: calcular A - B, com dimensões iguais. Retornar uma matriz."""
    raise NotImplementedError("A subtração ainda não foi implementada.")


def multiplicar(a, b):
    """TODO: produto A(m×n) por B(n×p). Retornar matriz m×p."""
    raise NotImplementedError("A multiplicação ainda não foi implementada.")


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
