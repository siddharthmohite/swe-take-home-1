from fastapi import HTTPException
from db.session import  SessionLocal
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError


@contextmanager
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def execute_query(query, as_mappings=False):
    try:
        with get_db_session() as db:
            if as_mappings:
                result = db.execute(query).mappings().all()
            else:
                result = db.execute(query).all()
            return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Query execution failed: {str(e)}")    