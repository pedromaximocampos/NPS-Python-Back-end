from flask import Flask
from src.Infra.Config import init_connections_with_database


def create_app():
    app = Flask(__name__)
    connections = init_connections_with_database(app)
    
    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)