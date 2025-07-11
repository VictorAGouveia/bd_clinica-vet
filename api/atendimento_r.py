from flask import Blueprint, jsonify, request
from db import get_db_session
from datetime import datetime
from repositories.atendimento_rep import AtendimentoRepository
from repositories.pet_rep import PetRepository
from repositories.veterinario_rep import VeterinarioRepository
from models.atendimento import Atendimento

# Blueprint para poder importar no main.py
atend_bp = Blueprint('atend_bp', __name__)

# --- ROTAS ---
# POST ATENDIMENTOS
@atend_bp.route('/atendimentos', methods=['POST'])
def create_atend():
    """Cria um novo atendimento.
    ---
    tags:
      - Atendimentos
    parameters:
      - name: body
        in: body
        required: true
        schema:
            $ref: '#/definitions/Atendimento'  # <-- Apenas referenciamos a definição global
    responses:
      201:
        description: Atendimento criado com sucesso.
        schema:
            $ref: '#/definitions/Atendimento'
      400:
        description: Um campo obrigatório estava faltando.
      404:
        description: Não foi encontrado um pet ou veterinário com os IDs dados.
    """
    dados = request.get_json()
    if not dados or not dados.get('data') or not dados.get('pet_id') or not dados.get('veterinario_id'):
        return jsonify({"error": "Os campos 'data', 'pet_id' e 'veterinario_id' são obrigatórios"}), 400
    
    try:
        data_atendimento = datetime.fromisoformat(dados['data'])
    except (ValueError, TypeError):
        return jsonify({"error": "Formato de data inválido. Use o formato ISO 8601: YYYY-MM-DDTHH:MM:SS"}), 400

    db = get_db_session()
    repo_p = PetRepository(db)
    if not repo_p.get_by_id(dados['pet_id']):
        return jsonify({"error":f"Nao foi encontrado nenhum pet com id {dados['pet_id']}"}), 404
    
    repo_v = VeterinarioRepository(db)
    if not repo_v.get_by_id(dados['veterinario_id']):
        return jsonify({"error":f"Nao foi encontrado nenhum veterinario com id {dados['veterinario_id']}"}), 404
    
    
    repo = AtendimentoRepository(db)
    novo_atend = Atendimento(data=dados['data'], pet_id=dados['pet_id'], veterinario_id=dados['veterinario_id'], descricao=dados['descricao'])
    atend_salvo = repo.create(novo_atend)
    return jsonify(atend_salvo.to_dict()), 201

# GET ATENDIMENTOS
@atend_bp.route('/atendimentos', methods=['GET'])
def get__atends():
    """Lista todos os Atendimentos cadastrados.
    ---
    tags:
      - Atendimentos
    responses:
      200:
        description: Uma lista de todos os Atendimentos.
        schema:
          type: array
          items:
            $ref: '#/definitions/Atendimento'
    """
    db = get_db_session()
    repo = AtendimentoRepository(db)
    atends = repo.get_all()
    return jsonify([a.to_dict() for a in atends])
