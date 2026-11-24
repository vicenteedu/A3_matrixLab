"""Etapas didáticas separadas do código dos alunos.

Reproduz as operações e a aritmética nativa de matrizes.determinante.
Nunca substitui resultado ou passos; omite a visualização se houver divergência.
Ao mudar o método dos alunos, este adaptador também precisa ser revisado.
"""


def _texto(valor):
    return str(valor)


def _produto(fatores):
    produto = 1
    for fator in fatores:
        produto *= fator
    return produto


def _quadro(matriz):
    return [[_texto(valor) for valor in linha] for linha in matriz]


def visualizar_determinante(a, resultado):
    matriz = [linha[:] for linha in a]
    n = len(matriz)
    etapas = []
    inicial = _quadro(matriz)
    if n == 1:
        metodo = "direto"
        calculado = matriz[0][0]
        etapas.append({"tipo": "diagonal", "celulas": [[0, 0]],
                       "expressao": f"det(A) = {calculado}",
                       "explicacao": "O determinante é o único elemento da matriz."})
    elif n in (2, 3):
        metodo = "formula_2x2" if n == 2 else "sarrus"
        if n == 3:
            inicial = [linha + linha[:2] for linha in inicial]
        calculado = _determinante_diagonais(matriz, etapas)
    else:
        metodo = "gauss"
        calculado = _determinante_gauss(matriz, etapas)
    if calculado != resultado:
        return None
    visualizacao = {"versao": 1, "tipo": "determinante", "metodo": metodo,
                    "matriz": inicial, "etapas": etapas}
    if type(resultado) is int and abs(resultado) > 2**53 - 1:
        visualizacao["resultado_texto"] = str(resultado)
    return visualizacao


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
    for k in range(n - 1):
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
            return 0

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
    resultado = sinal
    for valor in diagonal:
        resultado *= valor
    fatores = " × ".join(f"({_texto(valor)})" for valor in diagonal)
    celulas = [[i, i] for i in range(n)]
    etapas.append({"tipo": "diagonal", "matriz": triangular, "celulas": celulas,
                   "expressao": f"{fatores} = {_texto(produto)}",
                   "explicacao": "O determinante da matriz triangular é o produto das entradas da diagonal."})
    etapas.append({"tipo": "final", "matriz": triangular, "celulas": celulas,
                   "expressao": f"det(A) = ({sinal:+d}) × ({_texto(produto)}) = {_texto(resultado)}",
                   "explicacao": f"Aplique o sinal (−1) elevado ao número de trocas ({trocas})."})
    return resultado


