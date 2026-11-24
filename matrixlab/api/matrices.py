"""Transporte HTTP; sem implementações matemáticas."""
from flask import current_app, jsonify, request
from werkzeug.exceptions import BadRequest, RequestEntityTooLarge
from ..domain.matrizes import DeterminanteForaDaFaixa
from ..domain.matrix_service import InvalidInput, InvalidResult, calculate


def calculate_matrix():
    if not request.is_json:
        return jsonify(codigo="json_necessario", erro="Envie os dados como JSON."), 415
    try:
        data = request.get_json()
        return jsonify(calculate(data))
    except BadRequest:
        return jsonify(codigo="json_invalido", erro="O JSON enviado está incompleto ou inválido."), 400
    except RequestEntityTooLarge:
        return jsonify(codigo="dados_muito_grandes", erro="O conteúdo enviado excede o tamanho permitido."), 413
    except InvalidInput as error:
        return jsonify(codigo="entrada_invalida", erro=str(error)), 400
    except NotImplementedError as error:
        return jsonify(codigo="nao_implementado", erro=str(error) or "Esta operação ainda não foi implementada."), 501
    except DeterminanteForaDaFaixa:
        return jsonify(codigo="determinante_fora_da_faixa", erro="O determinante está fora da faixa numérica que o site consegue exibir."), 422
    except InvalidResult as error:
        return jsonify(codigo="resultado_invalido", erro=f"A função retornou um resultado inválido. {error}"), 500
    except Exception:
        current_app.logger.exception("Falha na operação matricial")
        return jsonify(codigo="falha_calculo", erro="Não foi possível concluir o cálculo. Confira o terminal do servidor."), 500
