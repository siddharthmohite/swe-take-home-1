from db.session import engine, SessionLocal
from contextlib import contextmanager

@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def execute_query(query, as_mappings=False):
    with get_db_session() as db:
        if as_mappings:
            result = db.execute(query).mappings().all()
        else:
            result = db.execute(query).all()
        return result