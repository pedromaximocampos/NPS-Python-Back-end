from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from contextlib import contextmanager
from typing import Generator, Optional
from sqlalchemy.exc import SQLAlchemyError
import logging

class ConnectionSQL:
    def __init__(self, app=None, connection_string=None, development=False):
        self.__connection_string = connection_string
        self.__db = SQLAlchemy()
        self.logger = logging.getLogger(__name__)
        self.__session = None
        
       
        # Configurações do pool de conexões
        self.__engine_options = {
            'pool_size': 10,        # Número máximo de conexões simultâneas no pool
            'pool_recycle': 3600,   # Tempo em segundos para reciclar conexões (1 hora)
            'pool_pre_ping': True,  # Verifica se a conexão está ativa antes de usar
            'echo': True           # Mostra as queries SQL no console (útil para debug)
        }
        
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Inicializa a aplicação com as configurações do SQLAlchemy
        """
        app.config['SQLALCHEMY_DATABASE_URI'] = self.__connection_string
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = self.__engine_options
        
        self.__db.init_app(app)
        self.__engine = self.__create_database_engine()


    def __create_database_engine(self):
        try:
            engine = create_engine(
                self.__connection_string,
                **self.__engine_options
            )
            return engine
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao criar engine: {str(e)}")
            raise


    def get_engine(self):
        return self.__engine


    def get_db(self):
        return self.__db


    def close_db(self):
        try:
            self.__db.close()
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao fechar conexão: {str(e)}")
            raise
    
        
    @contextmanager
    def get_session(self) -> Generator:
        """
        Context manager para gerenciar sessões de forma segura
        """
        if self.__session is None:
            session_maker = sessionmaker(bind=self.__engine)
            self.__session = session_maker()
            
        try:
            yield self.__session
            self.__session.commit()
            
        except SQLAlchemyError as e:
            self.__session.rollback()
            self.logger.error(f"Erro na sessão: {str(e)}")
            raise
        except Exception as e:
            self.__session.rollback()
            self.logger.error(f"Erro inesperado: {str(e)}")
            raise
        finally:
            self.__session.close()
    
    
    def __enter__(self):
        session_maker = sessionmaker(bind=self.__engine)
        self.__session = session_maker()
        return self
    
    
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            if exc_type is not None:
                self.__session.rollback()
            else:
                self.__session.commit()
        except SQLAlchemyError as e:
            self.logger.error(f"Erro no contexto: {str(e)}")
            raise
        finally:
            self.__session.close()
            


    def execute_query(self, query: str, params: Optional[dict] = None):
        """
        Executa uma query SQL com parâmetros opcionais
        """
        try:
            with self.get_session() as session:
                if params:
                    return session.execute(query, params)
                return session.execute(query)
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao executar query: {str(e)}")
            raise
