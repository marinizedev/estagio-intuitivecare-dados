from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

DATABASE_URL = "mysql+pymysql://root:85731705VVAmv%25@localhost:3306/ans_despesas"

engine: Engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)