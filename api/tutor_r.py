from flask import Blueprint, jsonify, request
from db import get_db_session
from repositories.tutor_rep import TutorRepository
from models.tutor import Tutor

# Blueprint para poder importar no main.py
tutor_bp = Blueprint('tutor_bp', __name__)

# --- ROTAS ---
# POST TUTOR
@tutor_bp.route('/tutores', methods=['POST'])
def create_tutor():
    """Cria um novo tutor.
    ---
    tags:
      - Tutores
    parameters:
      - name: body
        in: body
        required: true
        schema:
            $ref: '#/definitions/Tutor'
    responses:
      201:
        description: Tutor criado com sucesso.
        schema:
            $ref: '#/definitions/Tutor'
      400:
        description: Um campo obrigatório estava faltando.
    """
    dados = request.get_json()
    if not dados or not dados.get('nome'):
        return jsonify({"error": "O campo 'nome' é obrigatório"}), 400
    
    db = get_db_session()
    repo = TutorRepository(db)

    novo_tutor = Tutor(nome=dados['nome'], telefone=dados['telefone'])
    tutor_salvo = repo.create(novo_tutor)
    return jsonify(tutor_salvo.to_dict()), 201

# GET TUTORES
@tutor_bp.route('/tutores', methods=['GET'])
def get__tutores():
    """Lista todos os tutores cadastradas.
    ---
    tags:
      - Tutores
    responses:
      200:
        description: Uma lista de todos os tutores.
        schema:
          type: array
          items:
            $ref: '#/definitions/Tutor'
    """
    db = get_db_session()
    repo = TutorRepository(db)
    tutores = repo.get_all()
    return jsonify([t.to_dict() for t in tutores])

# GET PETS DE TUTOR POR ID
@tutor_bp.route('/tutores/<int:tutor_id>/pets', methods=['GET'])
def get_pets_do_tutor(tutor_id: int):
    """Lista os pets de um tutor por seu ID.
    ---
    tags:
      - Tutores
    parameters:
      - name: tutor_id
        in: path
        type: integer
        required: true
        description: O ID do tutor a ser buscado.
    responses:
      200:
        description: A lisa de pets do tutor buscado.
        schema:
            type: array
            items:
                $ref: '#/definitions/Pet'
      404:
        description: Não foi encontrada um tutor ou nenhum pet para o tutor pelo ID dado.
    """
    db = get_db_session()
    repo = TutorRepository(db)
    pets = repo.get_pets(tutor_id)
    if not pets:
        return jsonify({"message": f"Nenhum pet ou tutor encontrado para o ID {tutor_id}"}), 404
    return jsonify([p.to_dict() for p in pets])