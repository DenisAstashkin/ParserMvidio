from sqlalchemy import create_engine
from Model.model import Base
from sqlalchemy.orm import Session


class Manager:
    
    def __init__(self, path: str, type_table: type):
        self.sql_db = f"sqlite:///{path}"
        self.engine = None
        self.type = type_table
        
    def Connection(self):
        try:
            self.engine = create_engine(self.sql_db)
            Base.metadata.create_all(bind=self.engine)
            return True
        except Exception:
            return False

    def AddItems(self, items: list) -> bool:
        try:
            with Session(autoflush=False, bind=self.engine) as db:
                self.DelItems()
                db.add_all(items)
                db.commit()
            return True
        except Exception:
            return False
            
    def DelItems(self) -> bool:
        try:
            with Session(autoflush=False, bind=self.engine) as db:
                db.query(self.type).delete()
                db.commit()
            return True
        except Exception:
            return False
