import json
from flask import Flask, g
from flasgger import Swagger

# 1. Importa os blueprints que você criou
from api.clinica_r import clinica_bp
from api.veterinario_r import vet_bp
from api.tutor_r import tutor_bp
from api.pet_r import pet_bp
from api.atendimento_r import atend_bp

app = Flask(__name__)

with open('swagger_template.json', 'r', encoding='utf-8') as f:
    swagger_template = json.load(f)

# 2. Registra os blueprints na aplicação
app.register_blueprint(clinica_bp)
app.register_blueprint(vet_bp)
app.register_blueprint(tutor_bp)
app.register_blueprint(pet_bp)
app.register_blueprint(atend_bp)

swagger = Swagger(app, template=swagger_template)

# A função de fechar a sessão continua aqui, pois é um evento do ciclo de vida da aplicação.
@app.teardown_appcontext
def close_db_session(exception=None):
    db_session = g.pop('db_session', None)
    if db_session is not None:
        db_session.close()

# O ponto de entrada continua o mesmo
if __name__ == "__main__":
    from db import init_db
    init_db()
    app.run(debug=True)