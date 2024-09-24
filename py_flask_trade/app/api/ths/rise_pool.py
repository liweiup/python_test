from app import create_app
from sqlalchemy.orm import sessionmaker

def insert_data(json_data):
    with create_app.app_context():
        Session = sessionmaker(bind=create_app.db.engine)
        session = Session()
        
        new_stock = StockData(
            # ... 现有代码 ...
        )
        session.add(new_stock)
        session.commit()
        session.close()

# ... 剩余代码 ...
