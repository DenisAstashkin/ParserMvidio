from sqlalchemy import create_engine
from Model.model import Base
from sqlalchemy.orm import sessionmaker


class Manager:
    
    def __init__(self, path: str, type_table: type):
        self.sql_db = f"sqlite:///{path}"
        self.engine = None
        self.type = type_table
        self.Session = None
        
    def Connection(self):
        try:
            self.engine = create_engine(self.sql_db)
            self.Session = sessionmaker(bind=self.engine)
            Base.metadata.create_all(bind=self.engine)
            return True
        except Exception:
            return False

    def AddItems(self, items: list) -> bool:
        try:
            self.DelItems()
            db = self.Session()
            db.add_all(items)
            db.commit()
            
            return True
        except Exception as ex:    
            print(ex)        
            return False
            
    def DelItems(self) -> bool:
        try:
            db = self.Session()
            db.query(self.type).delete()
            db.commit()
            return True
        except Exception:
            return False
