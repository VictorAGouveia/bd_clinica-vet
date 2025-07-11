from flask import Blueprint, jsonify, request
from db import get_db_session
from repositories.clinica_rep import ClinicaRepository
from models.clinica import Clinica

# Blueprint para poder importar no main.py
clinica_bp = Blueprint('clinica_bp', __name__)

# --- ROTAS ---
# POST CLINICA
@clinica_bp.route('/clinicas', methods=['POST'])
def create_clinica():
    """Cria uma nova clínica.
    ---
    tags:
      - Clínicas
    parameters:
      - name: body
        in: body
        required: true
        schema:
            $ref: '#/definitions/Clinica'
    responses:
      201:
        description: Clínica criada com sucesso.
        schema:
            $ref: '#/definitions/Clinica'
      400:
        description: Um campo obrigatório estava faltando.
    """
    dados = request.get_json()
    if not dados or not dados.get('nome') or not dados.get('cidade'):
        return jsonify({"error": "Os campos 'nome' e 'cidade' são obrigatórios"}), 400

    db = get_db_session()
    repo = ClinicaRepository(db)

    nova_clinica = Clinica(nome=dados['nome'], cidade=dados['cidade'])
    clinica_salva = repo.create(nova_clinica)
    return jsonify(clinica_salva.to_dict()), 201

# GET CLINICAS
@clinica_bp.route('/clinicas', methods=['GET'])
def get__clinicas():
    """Lista todas as clínicas cadastradas.
    ---
    tags:
      - Clínicas
    responses:
      200:
        description: Uma lista de todas as clínicas.
        schema:
          type: array
          items:
            $ref: '#/definitions/Clinica'
    """
    db = get_db_session()
    repo = ClinicaRepository(db)
    clinicas = repo.get_all()
    return jsonify([c.to_dict() for c in clinicas])

# GET CLINICA POR ID
@clinica_bp.route('/clinicas/<int:clinica_id>', methods=['GET'])
def get__clinicas_id(clinica_id: int):
    """Lista uma clínica cadastra partir de seu ID.
    ---
    tags:
      - Clínicas
    parameters:
      - name: clinica_id
        in: path
        type: integer
        required: true
        description: O ID da clínica a ser buscada.
    responses:
      200:
        description: As informações da clínica buscada.
        schema:
            $ref: '#/definitions/Clinica'
      404:
        description: Não foi encontrada uma clínica com o ID dado.
    """
    db = get_db_session()
    repo = ClinicaRepository(db)
    clinica = repo.get_by_id(clinica_id)
    if not clinica:
        return jsonify({"error":"clinica nao encontrada"}), 404
    return jsonify(clinica.to_dict())

# GET VETERINARIOS DE CLINICA POR ID
@clinica_bp.route('/clinicas/<int:clinica_id>/veterinarios', methods=['GET'])
def get_veterinarios_da_clinica(clinica_id: int):
    """Lista os veterinários de uma clínica por seu ID.
    ---
    tags:
      - Clínicas
    parameters:
      - name: clinica_id
        in: path
        type: integer
        required: true
        description: O ID da clínica a ser buscada.
    responses:
      200:
        description: A lisa de veterinários da clínica buscada.
        schema:
            type: array
            items:
                $ref: '#/definitions/Veterinario'
      404:
        description: Não foi encontrada uma clínica ou nenhum veterinário na clínica com o ID dado.
    """
    db = get_db_session()
    repo = ClinicaRepository(db)
    veterinarios = repo.get_vets(clinica_id)
    if not veterinarios:
        return jsonify({"message": f"Nenhuma clínica ou veterinário encontrado para o ID {clinica_id}"}), 404
    return jsonify([v.to_dict() for v in veterinarios])
