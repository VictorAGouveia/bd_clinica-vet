from flask import Blueprint, jsonify, request
from db import get_db_session
from repositories.clinica_rep import ClinicaRepository
from repositories.veterinario_rep import VeterinarioRepository
from models.veterinario import Veterinario

# Blueprint para poder importar no main.py
vet_bp = Blueprint('vets_bp', __name__)

# --- ROTAS ---
# POST VETERINARIO
@vet_bp.route('/veterinarios', methods=['POST'])
def create_vet():
    """Cria um novo veterinário.
    ---
    tags:
      - Veterinários
    parameters:
      - name: body
        in: body
        required: true
        schema:
            $ref: '#/definitions/Veterinario'
    responses:
      201:
        description: Veterinário criado com sucesso.
        schema:
            $ref: '#/definitions/Veterinario'
      400:
        description: Um campo obrigatório estava faltando.
    """
    dados = request.get_json()
    if not dados or not dados.get('nome') or not dados.get('clinica_id') or not dados.get('especialidade'):
        return jsonify({"error": "Os campos 'nome', 'clinica_id' e 'especialidade' são obrigatórios"}), 400

    db = get_db_session()
    repo_c = ClinicaRepository(db)
    if not repo_c.get_by_id(dados['clinica_id']):
        return jsonify({"error":f"Nao foi encontrado nenhuma clinica com id {dados['clinica_id']}"}), 400
    
    repo = VeterinarioRepository(db)

    nova_clinica = Veterinario(nome=dados['nome'], clinica_id=dados['clinica_id'], especialidade=dados['especialidade'])
    clinica_salva = repo.create(nova_clinica)
    return jsonify(clinica_salva.to_dict()), 201

# GET VETERINARIO
@vet_bp.route('/veterinarios', methods=['GET'])
def get__vets():
    """Lista todos os veterinarios cadastradas.
    ---
    tags:
      - Veterinários
    responses:
      200:
        description: Uma lista de todos os veterinários.
        schema:
          type: array
          items:
            $ref: '#/definitions/Veterinario'
    """
    db = get_db_session()
    repo = VeterinarioRepository(db)
    veterinarios = repo.get_all()
    return jsonify([v.to_dict() for v in veterinarios])

# GET ATENDIMENTOS DE VETERINARIOS POR ID
@vet_bp.route('/veterinarios/<int:vet_id>/atendimentos', methods=['GET'])
def get_atends_do_vet(vet_id: int):
    """Lista os atendimentos de um veterinário por seu ID.
    ---
    tags:
      - Veterinários
    parameters:
      - name: vet_id
        in: path
        type: integer
        required: true
        description: O ID do veterinário a ser buscado.
    responses:
      200:
        description: A lisa de atendimentos do veterinário buscado.
        schema:
            type: array
            items:
                $ref: '#/definitions/Atendimento'
      404:
        description: Não foi encontrado um veterinário ou nenhum atendimento para o veterinário pelo ID dado.
    """
    db = get_db_session()
    repo = VeterinarioRepository(db)
    atends = repo.get_atends(vet_id)
    if not atends:
        return jsonify({"message": f"Nenhum atendimento ou veterinario encontrado para o ID {vet_id}"}), 404
    return jsonify([a.to_dict() for a in atends])
