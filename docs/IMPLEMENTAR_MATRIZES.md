# Onde vocês vão programar

**Editem `matrixlab/domain/matrizes.py`.** A tela, o envio dos valores, a API, as validações e a apresentação dos resultados já estão conectados. Os sete algoritmos foram deixados intencionalmente sem implementação.

## 1. Escolham uma função

- `somar(a, b)`: recebe duas matrizes de mesma dimensão; devolve uma matriz dessa dimensão.
- `subtrair(a, b)`: recebe duas matrizes de mesma dimensão; devolve A − B.
- `multiplicar(a, b)`: recebe A de tamanho m×n e B de tamanho n×p; devolve uma matriz m×p.
- `transpor(a)`: recebe uma matriz m×n; devolve uma matriz n×m.
- `determinante(a)`: recebe uma matriz quadrada de ordem 1 a 8; devolve **um número**, não uma matriz.
- `identidade(ordem)`: recebe um inteiro de 1 a 8; devolve uma matriz quadrada dessa ordem.
- `nula(linhas, colunas)`: recebe dois inteiros de 1 a 8; devolve uma matriz com essas dimensões.

O arquivo já contém todas as assinaturas. Substituam o `raise NotImplementedError(...)` da função escolhida pelo código de vocês. Mantenham os nomes e os argumentos para a ligação continuar funcionando.

## 2. Usem diretamente os argumentos

`a` e `b` já são listas de listas Python com os valores preenchidos na tela. Por exemplo:

```python
# Exemplos de acesso, não são o algoritmo de uma operação:
primeiro_valor = a[0][0]
quantidade_de_linhas = len(a)
quantidade_de_colunas = len(a[0])
```

Os índices começam em zero. Não usem `input()` para pedir valores: eles já vieram do site. Não é necessário usar Flask, banco de dados ou JavaScript dentro desse arquivo. Implementem os cálculos com listas, laços e condicionais, sem NumPy ou bibliotecas que resolvam a matemática.

A API já verificou que as matrizes são retangulares, têm de 1 a 8 linhas/colunas e contêm números finitos. Também verificou as condições da operação: dimensões iguais para soma/subtração, compatibilidade para multiplicação e tamanho permitido para determinante. Chamadas diretas pelo terminal não passam pela API; usem entradas válidas nesses testes.

## 3. Retornem o resultado

Depois de construir a variável `resultado` no algoritmo, vocês podem devolver apenas:

```python
return resultado
```

Ou acrescentar explicações calculadas junto com a resolução:

```python
return {
    "resultado": resultado,
    "passos": passos,
}
```

`passos` deve ser uma lista de textos, em ordem. Por exemplo, uma explicação de uma célula pode ter o formato `"Linha 1, coluna 1: 2 + 3 = 5"`. O texto deve descrever a conta realmente feita pelo algoritmo. O site já apresenta essa lista na seção **Ver resolução passo a passo**. Sem passos, essa seção fica escondida.

Não fixem respostas no código. A função precisa trabalhar com os valores recebidos. `print()` é útil para depurar no terminal, mas **somente `return` envia o resultado de volta à tela**. Evitem modificar os argumentos de entrada; construam uma matriz de saída.

## 4. Experimentem no site

1. Salvem `matrizes.py`.
2. Se iniciaram com `python run.py`, parem com `Ctrl+C` e iniciem novamente, pois esse comando está sem recarregamento automático.
3. Atualizem a página, escolham a operação e preencham A e, quando necessário, B.
4. Ao alterar linhas/colunas, cliquem em **Atualizar** para aplicar o tamanho.
5. Cliquem em **Calcular**. O resultado e os passos serão apresentados automaticamente.

Para identidade e nula, a interface pede apenas dimensões, sem valores de entrada.

Enquanto a função tiver `raise NotImplementedError`, o site mostra **Em desenvolvimento**. Isso confirma que os valores chegaram ao backend, mas a resolução ainda falta. Se a função não tiver `return`, retornar uma dimensão incorreta ou produzir números não finitos, a tela informa que o retorno é inválido. Outros erros do código ficam detalhados no terminal do servidor.

Para recarregamento automático durante o desenvolvimento local, vocês podem iniciar com:

```powershell
.\.venv\Scripts\python.exe -m flask --app matrixlab run --debug
```

Mantenham esse modo restrito ao computador local. Não é necessário alterar `run.py`.

## 5. Executem os testes

Na raiz do projeto, no PowerShell:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Para verificar apenas as resoluções:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_matrizes.py -v
```

No macOS/Linux, substituam o executável por `.venv/bin/python`.

- `tests/test_matrizes.py`: dez casos de aceitação com valores esperados. Cada caso fica **skipped** enquanto a função correspondente lança `NotImplementedError`. Quando vocês a implementam, o teste passa a conferir a resposta. Acrescentem outros casos ao desenvolver.
- `tests/test_matrix_api.py`: testa a infraestrutura e simula retornos para verificar transporte e apresentação do contrato. Esses testes não provam que os algoritmos de vocês estão corretos.
- `tests/test_app.py`: mantém os nove testes da base e do grafo de exemplo.

Os casos de identidade e matriz nula ficam pulados até que essas funções sejam implementadas. Os testes de transposta e determinante também verificam as etapas enviadas pelo backend.

## Como os arquivos se conectam

```text
Tela: valores de A e B
    ↓
static/js/matrix-editor.js
    POST /api/matrices/calculate
    ↓
api/matrices.py
    ↓
domain/matrix_service.py  → valida e escolhe a função
    ↓
domain/matrizes.py       → VOCÊS IMPLEMENTAM AQUI
    ↓
Resultado JSON → JavaScript → painel Resultado
```

Exemplo do JSON enviado pelo navegador:

```json
{
  "operacao": "somar",
  "a": [[2, 3]],
  "b": [[4, 5]]
}
```

Isso chama `somar([[2, 3]], [[4, 5]])`. O mesmo fluxo vale para todas as operações, com os argumentos correspondentes. A API chama a função a cada requisição; não é preciso cadastrar novamente uma função depois de preenchê-la.

## Onde os números ficam

Os rascunhos A e B ficam no navegador, na chave `matrixlab.matrices.v2` do `localStorage`. O rascunho antigo `matrixlab.matrix.v1` é carregado como A quando ainda não existe o novo formato. Ao calcular, uma cópia dos dados necessários é enviada ao Python. O servidor não salva os números em disco nem em banco de dados.

Modificar os dados ou a operação limpa o resultado anterior e cancela uma resposta ainda pendente, para não mostrar uma resolução de valores antigos. O módulo de grafos continua como exemplo: esta entrega prepara somente as operações matriciais.
