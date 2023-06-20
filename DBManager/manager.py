from sqlalchemy import create_engine
from Model.model import Base
from sqlalchemy.orm import Session


class Manager:
    
    def __init__(self, path: str, type_table: type):
        self.sql_db = f"sqlite:///{path}"
        self.engine = None
        self.type = type_table
        
    
