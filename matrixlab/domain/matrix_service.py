"""Validação e encaminhamento. Os algoritmos pertencem apenas a matrizes.py."""
from math import isfinite
from . import matrizes

MAX_SIZE = 8
OPERATIONS = {"somar", "subtrair", "multiplicar", "transpor", "determinante", "identidade", "nula"}


class InvalidInput(ValueError):
    """Dados do usuário que não atendem ao contrato da operação."""


class InvalidResult(ValueError):
    """Uma função preenchida retornou um formato incompatível."""


def finite_number(value):
    try:
        return type(value) in (int, float) and isfinite(value)
    except OverflowError:
        return False


def dimension(value, name):
    if type(value) is not int or not 1 <= value <= MAX_SIZE:
        raise InvalidInput(f"{name} deve ser um inteiro entre 1 e {MAX_SIZE}.")
    return value


def matrix_shape(value, name):
    if not isinstance(value, list) or not 1 <= len(value) <= MAX_SIZE:
        raise InvalidInput(f"{name} deve ter de 1 a {MAX_SIZE} linhas.")
    if not isinstance(value[0], list) or not 1 <= len(value[0]) <= MAX_SIZE:
        raise InvalidInput(f"{name} deve ter de 1 a {MAX_SIZE} colunas.")
    columns = len(value[0])
    for row in value:
        if not isinstance(row, list) or len(row) != columns:
            raise InvalidInput(f"Todas as linhas de {name} devem ter o mesmo tamanho.")
        if not all(finite_number(number) for number in row):
            raise InvalidInput(f"{name} deve conter apenas números finitos, sem células vazias.")
    return len(value), columns


def prepare(data):
    if not isinstance(data, dict):
        raise InvalidInput("Envie um objeto JSON com a operação e seus dados.")
    operation = data.get("operacao")
    if not isinstance(operation, str) or operation not in OPERATIONS:
        raise InvalidInput("Escolha uma operação válida.")
    if operation == "identidade":
        order = dimension(data.get("ordem"), "A ordem")
        return operation, [order], (order, order)
    if operation == "nula":
        rows = dimension(data.get("linhas"), "O número de linhas")
        columns = dimension(data.get("colunas"), "O número de colunas")
        return operation, [rows, columns], (rows, columns)

    a = data.get("a")
    rows_a, columns_a = matrix_shape(a, "A matriz A")
    if operation == "determinante":
        if rows_a != columns_a or rows_a not in (2, 3):
            raise InvalidInput("O determinante aceita somente matrizes 2 × 2 ou 3 × 3.")
        return operation, [a], None
    if operation == "transpor":
        return operation, [a], (columns_a, rows_a)

    b = data.get("b")
    rows_b, columns_b = matrix_shape(b, "A matriz B")
    if operation in ("somar", "subtrair"):
        if (rows_a, columns_a) != (rows_b, columns_b):
            raise InvalidInput("A e B precisam ter as mesmas dimensões para somar ou subtrair.")
        return operation, [a, b], (rows_a, columns_a)
    if columns_a != rows_b:
        raise InvalidInput("Para multiplicar, o número de colunas de A deve ser igual ao de linhas de B.")
    return operation, [a, b], (rows_a, columns_b)


def normalize_result(raw, expected_shape):
    if isinstance(raw, dict):
        result, steps = raw.get("resultado"), raw.get("passos", [])
    else:
        result, steps = raw, []
    if not isinstance(steps, list) or len(steps) > 2000 or any(not isinstance(step, str) or len(step) > 10000 for step in steps):
        raise InvalidResult("Os passos devem ser uma lista de textos (até 2.000 passos de 10.000 caracteres).")
    if expected_shape is None:
        if not finite_number(result):
            raise InvalidResult("O determinante deve retornar um número finito.")
    else:
        try:
            actual = matrix_shape(result, "O resultado")
        except InvalidInput as error:
            raise InvalidResult(str(error)) from error
        if actual != expected_shape:
            raise InvalidResult(f"O resultado deve ter dimensão {expected_shape[0]} × {expected_shape[1]}.")
    normalized = {"resultado": result, "passos": steps}
    if isinstance(raw, dict) and "visualizacao" in raw:
        normalized["visualizacao"] = raw["visualizacao"]
    return normalized


def calculate(data):
    operation, arguments, expected_shape = prepare(data)
    # Ponto de ligação: chama a função de mesmo nome no arquivo de vocês.
    raw = getattr(matrizes, operation)(*arguments)
    return {"operacao": operation, **normalize_result(raw, expected_shape)}
