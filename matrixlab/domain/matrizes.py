"""PREENCHAM ESTE ARQUIVO: a conexão com a tela já está pronta.

As entradas já chegam validadas. Matrizes são listas de listas de números.
Não usem input(), Flask, NumPy ou JavaScript aqui.

Em cada função, substituam o `raise NotImplementedError` pelo algoritmo.
Retornem: {"resultado": sua_matriz_ou_numero, "passos": ["Explicação", ...]}.
`passos` é opcional; também é permitido retornar só a matriz ou o número.
As explicações devem descrever os cálculos que vocês realmente executaram.

Guia e exemplos de uso: docs/IMPLEMENTAR_MATRIZES.md.
"""

from decimal import Decimal, localcontext
from fractions import Fraction
from math import isfinite


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
            detalhes = []
            for k in range(colunas_a):
                prod = a[i][k] * b[k][j]
                soma += prod
                detalhes.append({"linha": i, "coluna": j, "indice": k, "fase": "produto",
                                 "expressao": f"({a[i][k]}) × ({b[k][j]}) = {prod}",
                                 "explicacao": f"Multiplique A[{i+1}, {k+1}] por B[{k+1}, {j+1}]. Soma parcial: {soma}."})
                produtos.append(f"{a[i][k]}x{b[k][j]}")
            passos.append(f"C[{i}][{j}] = " + " + ".join(produtos) + f" = {soma}")

            etapas.extend(detalhes)
            etapas.append(
                {
                    "fase": "resultado",
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
    """Transposta de A(m×n). Retornar matriz n×m."""
    linhas = len(a)
    colunas = len(a[0])
    resultado = []
    passos = []
    etapas  = []
    
    for j in range(colunas):
        nova_linha = []
        for i in range(linhas):
            nova_linha.append(a[i][j])
            passos.append(f"Transpondo elemento A[{i}][{j}] para AT[{j}][{i}]: {a[i][j]}")
            etapas.append({
                "linha_original": i,
                "coluna_original": j,
                "linha_transposta": j,
                "coluna_transposta": i,
                "valor": a[i][j],
                "expressao": f"AT[{j}][{i}] = A[{i}][{j}] = {a[i][j]}",
                "explicacao": f"Coloque o elemento da linha {i + 1}, coluna {j + 1} de A na linha {j + 1}, coluna {i + 1} de AT.",
            })
        resultado.append(nova_linha)
    return {
        "resultado": resultado,
        "passos": passos,
        "visualizacao": {
            "versao": 1,
            "tipo": "transpor",
            "a": a,
            "etapas": etapas,
        },
    }


class DeterminanteForaDaFaixa(ArithmeticError):
    """O determinante exato não cabe no formato numérico da API."""


def _texto(valor):
    """Exibe frações pequenas exatamente e aproxima apenas números longos."""
    if valor.numerator.bit_length() <= 40 and valor.denominator.bit_length() <= 30:
        return str(valor)
    with localcontext() as contexto:
        contexto.prec = 10
        aproximacao = Decimal(valor.numerator) / Decimal(valor.denominator)
        return f"≈{aproximacao:.9g}"


def _produto(fatores):
    produto = Fraction(1)
    for fator in fatores:
        produto *= fator
    return produto


def _quadro(matriz):
    return [[_texto(valor) for valor in linha] for linha in matriz]


def determinante(a):
    """Calcular det(A) pelo método escolhido pela ordem, registrando suas etapas."""
    n = len(a)
    if not 1 <= n <= 8 or any(len(linha) != n for linha in a):
        raise ValueError("O determinante exige uma matriz quadrada de ordem 1 a 8.")

    # Aritmética racional sobre os decimais recebidos evita tolerâncias absolutas,
    # cancelamento e resíduos de arredondamento nos pivôs intermediários.
    matriz = [[Fraction(str(valor)) for valor in linha] for linha in a]
    etapas = []
    inicial = _quadro(matriz)
    if n == 1:
        metodo = "direto"
        resultado = matriz[0][0]
        etapas.append({"tipo": "diagonal", "celulas": [[0, 0]],
                       "expressao": f"det(A) = {_texto(resultado)}",
                       "explicacao": "O determinante é o único elemento da matriz."})
    elif n in (2, 3):
        metodo = "formula_2x2" if n == 2 else "sarrus"
        if n == 3:
            inicial = [linha + linha[:2] for linha in inicial]
        resultado = _determinante_diagonais(matriz, etapas)
    else:
        metodo = "gauss"
        resultado = _determinante_gauss(matriz, etapas)

    try:
        aproximacao = float(resultado)
    except OverflowError:
        raise DeterminanteForaDaFaixa from None
    if not isfinite(aproximacao) or (resultado != 0 and aproximacao == 0):
        raise DeterminanteForaDaFaixa
    valor = resultado.numerator if resultado.denominator == 1 else aproximacao
    visualizacao = {
        "versao": 1, "tipo": "determinante", "metodo": metodo,
        "matriz": inicial, "etapas": etapas,
    }
    if type(valor) is int and abs(valor) > 2**53 - 1:
        # O navegador pode arredondar inteiros grandes ao ler o JSON.
        visualizacao["resultado_texto"] = str(valor)
    return {
        "resultado": valor,
        "passos": [f"{etapa['explicacao']} {etapa['expressao']}" for etapa in etapas],
        "visualizacao": visualizacao,
    }


def _determinante_diagonais(matriz, etapas):
    n = len(matriz)
    if n == 2:
        grupos = [[[(0, 0), (1, 1)]], [[(0, 1), (1, 0)]]]
    else:
        # A cópia das duas primeiras colunas estende as diagonais de Sarrus.
        matriz = [linha + linha[:2] for linha in matriz]
        grupos = [
            [[(i, inicio + i) for i in range(3)] for inicio in range(3)],
            [[(i, inicio - i) for i in range(3)] for inicio in range(2, 5)],
        ]
    totais = []
    for sinal, diagonais in zip(("positiva", "negativa"), grupos):
        produtos = []
        for indice, diagonal in enumerate(diagonais, start=1):
            fatores = [matriz[i][j] for i, j in diagonal]
            produto = _produto(fatores)
            produtos.append(produto)
            expressao = " × ".join(f"({_texto(fator)})" for fator in fatores)
            etapas.append({"tipo": "diagonal", "sinal": sinal, "celulas": diagonal,
                           "expressao": f"{expressao} = {_texto(produto)}",
                           "explicacao": f"Multiplique os elementos da diagonal {sinal} {indice}."})
        total = sum(produtos)
        totais.append(total)
        if n == 3:
            expressao = " + ".join(f"({_texto(valor)})" for valor in produtos)
            etapas.append({"tipo": "soma", "sinal": sinal, "celulas": diagonais[0] + diagonais[1] + diagonais[2],
                           "expressao": f"{expressao} = {_texto(total)}",
                           "explicacao": f"Some os três produtos das diagonais do grupo de sinal {sinal}."})
    positivo, negativo = totais
    resultado = positivo - negativo
    etapas.append({"tipo": "final", "expressao": f"det(A) = ({_texto(positivo)}) − ({_texto(negativo)}) = {_texto(resultado)}",
                   "explicacao": "Subtraia o total das diagonais negativas do total das positivas."})
    return resultado


def _determinante_gauss(matriz, etapas):
    n = len(matriz)
    sinal = 1
    trocas = 0
    for k in range(n):
        linha_pivo = k
        for i in range(k + 1, n):
            if abs(matriz[i][k]) > abs(matriz[linha_pivo][k]):
                linha_pivo = i

        pivo = matriz[linha_pivo][k]
        etapas.append({"tipo": "pivo", "matriz": _quadro(matriz),
                       "pivo": [linha_pivo, k], "candidatos": [[i, k] for i in range(k, n)],
                       "expressao": f"A[{linha_pivo + 1}, {k + 1}] = {_texto(pivo)}",
                       "explicacao": f"Na coluna {k + 1}, escolha o maior valor absoluto a partir da linha {k + 1}."})
        if pivo == 0:
            etapas.append({"tipo": "singular", "matriz": _quadro(matriz), "pivo": [linha_pivo, k],
                           "expressao": "det(A) = 0",
                           "explicacao": "Todos os candidatos a pivô nesta coluna são zero. A matriz é singular."})
            return Fraction(0)

        if linha_pivo != k:
            matriz[k], matriz[linha_pivo] = matriz[linha_pivo], matriz[k]
            sinal *= -1
            trocas += 1
            etapas.append({"tipo": "troca", "matriz": _quadro(matriz), "linhas": [k, linha_pivo],
                           "pivo": [k, k], "expressao": f"L{k + 1} ↔ L{linha_pivo + 1} · sinal acumulado: {sinal:+d}",
                           "explicacao": "A troca coloca o pivô na diagonal e inverte o sinal acumulado do determinante."})

        for i in range(k + 1, n):
            entrada = matriz[i][k]
            fator = entrada / pivo
            if fator == 0:
                continue
            atualizacoes = []
            for j in range(k, n):
                anterior = matriz[i][j]
                valor_pivo = matriz[k][j]
                matriz[i][j] -= fator * valor_pivo
                atualizacoes.append(f"A[{i + 1}, {j + 1}] = ({_texto(anterior)}) − ({_texto(fator)}) × ({_texto(valor_pivo)}) = {_texto(matriz[i][j])}")
            etapas.append({"tipo": "eliminacao", "matriz": _quadro(matriz), "pivo": [k, k],
                           "celulas": [[i, j] for j in range(k, n)], "linha": i,
                           "expressao": f"f = ({_texto(entrada)}) ÷ ({_texto(pivo)}) = {_texto(fator)}",
                           "explicacao": f"L{i + 1} ← L{i + 1} − f × L{k + 1} zera a entrada abaixo do pivô sem alterar o determinante.",
                           "atualizacoes": atualizacoes})

    triangular = _quadro(matriz)
    etapas.append({"tipo": "triangular", "matriz": triangular,
                   "expressao": "Matriz triangular superior",
                   "explicacao": "As entradas abaixo da diagonal principal agora são zero."})
    diagonal = [matriz[i][i] for i in range(n)]
    produto = _produto(diagonal)
    resultado = sinal * produto
    fatores = " × ".join(f"({_texto(valor)})" for valor in diagonal)
    celulas = [[i, i] for i in range(n)]
    etapas.append({"tipo": "diagonal", "matriz": triangular, "celulas": celulas,
                   "expressao": f"{fatores} = {_texto(produto)}",
                   "explicacao": "O determinante da matriz triangular é o produto das entradas da diagonal."})
    etapas.append({"tipo": "final", "matriz": triangular, "celulas": celulas,
                   "expressao": f"det(A) = ({sinal:+d}) × ({_texto(produto)}) = {_texto(resultado)}",
                   "explicacao": f"Aplique o sinal (−1) elevado ao número de trocas ({trocas})."})
    return resultado


def identidade(ordem):
    """TODO: criar identidade quadrada. `ordem` é inteiro de 1 a 8."""
    raise NotImplementedError("A matriz identidade ainda não foi implementada.")


def nula(linhas, colunas):
    """TODO: criar matriz nula. Dimensões são inteiros de 1 a 8."""
    raise NotImplementedError("A matriz nula ainda não foi implementada.")
