from sqlalchemy import create_engine, Column, Integer, String, JSON, Table, MetaData
from sqlalchemy.orm import sessionmaker
from ..config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {})
SessionLocal = sessionmaker(bind=engine)
metadata = MetaData()

# Simple table for storing contract analytics
contracts = Table(
    "contracts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("address", String, unique=True, nullable=False),
    Column("meta", JSON, nullable=True),
)


def init_db():
    metadata.create_all(engine)


def upsert_contract(address: str, meta: dict):
    session = SessionLocal()
    stmt = contracts.select().where(contracts.c.address == address)
    existing = session.execute(stmt).fetchone()
    if existing:
        upd = contracts.update().where(contracts.c.address == address).values(meta=meta)
        session.execute(upd)
    else:
        ins = contracts.insert().values(address=address, meta=meta)
        session.execute(ins)
    session.commit()
    session.close()


def get_contract(address: str):
    session = SessionLocal()
    stmt = contracts.select().where(contracts.c.address == address)
    r = session.execute(stmt).fetchone()
    session.close()
    return dict(r) if r else None
