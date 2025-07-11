from flask import Blueprint, jsonify, request
from db import get_db_session
from repositories.pet_rep import PetRepository
from repositories.tutor_rep import TutorRepository
from models.pet import Pet

# Blueprint para poder importar no main.py
pet_bp = Blueprint('pet_bp', __name__)

# --- ROTAS ---
# POST PET
@pet_bp.route('/pets', methods=['POST'])
def create_pet():
    """Cria um novo pet.
    ---
    tags:
      - Pets
    parameters:
      - name: body
        in: body
        required: true
        schema:
            $ref: '#/definitions/Pet'
    responses:
      201:
        description: Pet criado com sucesso.
        schema:
            $ref: '#/definitions/Pet'
      400:
        description: Um campo obrigatório estava faltando.
      404:
        description: Não foi encontrado um tutor com o ID dado.
    """
    dados = request.get_json()
    if not dados or not dados.get('nome') or not dados.get('especie') or not dados.get('tutor_id'):
        return jsonify({"error": "Os campos 'nome' e 'especie' são obrigatórios"}), 400
    
    db = get_db_session()
    repo_t = TutorRepository(db)
    if not repo_t.get_by_id(dados['tutor_id']):
        return jsonify({"error":f"Nao foi encontrado nenhum tutor com id {dados['tutor_id']}"}), 404
    
    repo = PetRepository(db)

    novo_pet = Pet(nome=dados['nome'], especie=dados['especie'], idade=dados['idade'], tutor_id=dados['tutor_id'])
    pet_salvo = repo.create(novo_pet)
    return jsonify(pet_salvo.to_dict()), 201

# GET PETS
@pet_bp.route('/pets', methods=['GET'])
def get__pets():
    """Lista todos os pets cadastrados.
    ---
    tags:
      - Pets
    responses:
      200:
        description: Uma lista de todos os pets.
        schema:
          type: array
          items:
            $ref: '#/definitions/Pet'
    """
    db = get_db_session()
    repo = PetRepository(db)
    pets = repo.get_all()
    return jsonify([p.to_dict() for p in pets])

# GET ATENDIMENTOS DE PET POR ID
@pet_bp.route('/pets/<int:pet_id>/atendimentos', methods=['GET'])
def get_pets_do_tutor(pet_id: int):
    """Lista os atendimentos de um pet.
    ---
    parameters:
      - name: pet_id
        in: path
        type: integer
        required: true
        description: O ID do pet a ser consultado.
    tags:
      - Pets
    responses:
      200:
        description: Uma lista dos atendimentos do pet.
        schema:
          type: array
          items:
            $ref: '#/definitions/Atendimento'
      404:
        description: Não tem atendimentos ou o pet não foi encontrado.
    """
    db = get_db_session()
    repo = PetRepository(db)
    atends = repo.get_atends(pet_id)
    if not atends:
        return jsonify({"message": f"Nenhum atendimento ou pet encontrado para o ID {pet_id}"}), 404
    return jsonify([a.to_dict() for a in atends])