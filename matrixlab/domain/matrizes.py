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


def determinante(a):
    """Calcular determinante de A(n×n)."""
    linhas = len(a)
    colunas = len(a[0])

    if linhas != colunas:
        raise ValueError("O determinante exige uma matriz quadrada.")

    #matriz 1x1
    if linhas == 1:
        determinante_1x1 = a[0][0]
        return {
            "resultado": determinante_1x1,
            "passos": [f"Determinante de 1x1 é o próprio elemento: {determinante_1x1}"],
        }
        
    #matriz 2x2
    elif linhas == 2:
       determinante_2x2 = a[0][0] * a[1][1] - a[0][1] * a[1][0]
       return {
            "resultado": determinante_2x2,
            "passos": [
                f"Determinante de 2x2: a*d - b*c = {a[0][0]}*{a[1][1]} - {a[0][1]}*{a[1][0]} = {determinante_2x2}"
            ],
        }
    
    #matriz 3x3
    elif linhas == 3:
        passos =[]
        etapas = []
        passos.append("Calculando determinante de 3x3 usando a regra de Sarrus.")
        soma_positiva = (
            a[0][0] * a[1][1] * a[2][2]
            + a[0][1] * a[1][2] * a[2][0]
            + a[0][2] * a[1][0] * a[2][1]
        )
        passos.append(f"Soma positiva: {a[0][0]}*{a[1][1]}*{a[2][2]} + {a[0][1]}*{a[1][2]}*{a[2][0]} + {a[0][2]}*{a[1][0]}*{a[2][1]} = {soma_positiva}")
        soma_negativa = (
            a[0][2] * a[1][1] * a[2][0]
            + a[0][0] * a[1][2] * a[2][1]
            + a[0][1] * a[1][0] * a[2][2]
        )
        passos.append(f"Soma negativa: {a[0][2]}*{a[1][1]}*{a[2][0]} + {a[0][0]}*{a[1][2]}*{a[2][1]} + {a[0][1]}*{a[1][0]}*{a[2][2]} = {soma_negativa}")
        
        determinante_3x3 = soma_positiva - soma_negativa
        passos.append(f"Determinante = Soma positiva - Soma negativa = {soma_positiva} - {soma_negativa} = {determinante_3x3}")
        return {
            "resultado": determinante_3x3,
            "passos": passos,
        }
    
    #fiz pq nao sabia que nao precisava :) 
    else:
        matriz = [linha[:] for linha in a]

        n = len(matriz)
        sinal = 1

        for k in range(n - 1):
            linha_pivo = k

            # Procurar o melhor pivô
            for i in range(k + 1, n):
                if abs(matriz[i][k]) > abs(matriz[linha_pivo][k]):
                    linha_pivo = i

            # Verificar se a matriz é singular
            if matriz[linha_pivo][k] == 0:
                return {
                    "resultado": 0,
                    "passos": ["Matriz singular: determinante igual a zero."]
                }

            # Trocar linhas, se necessário
            if linha_pivo != k:
                matriz[k], matriz[linha_pivo] = matriz[linha_pivo], matriz[k]
                sinal *= -1

            # Pivô atualizado após a troca
            pivo = matriz[k][k]

            # Eliminação de Gauss
            for i in range(k + 1, n):
                fator = matriz[i][k] / pivo

                for j in range(k, n):
                    matriz[i][j] -= fator * matriz[k][j]

        
        determinante_final = sinal

        for i in range(n):
            determinante_final *= matriz[i][i]

        # Fora do for i
        return {
            "resultado": determinante_final,
            "passos": ["Determinante calculado usando eliminação de Gauss."],
        }
def identidade(ordem):
    """TODO: criar identidade quadrada. `ordem` é inteiro de 1 a 8."""
    raise NotImplementedError("A matriz identidade ainda não foi implementada.")


def nula(linhas, colunas):
    """TODO: criar matriz nula. Dimensões são inteiros de 1 a 8."""
    raise NotImplementedError("A matriz nula ainda não foi implementada.")
