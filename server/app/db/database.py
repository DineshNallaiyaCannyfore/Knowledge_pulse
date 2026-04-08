from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:root@localhost:5432/knowledge_pulse"

Base = declarative_base()

engine = create_engine(DATABASE_URL)

sessionLocal = sessionmaker(bind=engine, autocommit=False)
