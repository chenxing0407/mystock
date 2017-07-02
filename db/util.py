
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Date,DateTime, Float,Integer, Time
import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
_ENGINE = None
_MAKER = None
# CONF = cfg.CONF
# LOG = logging.getLogger(__name__)


def get_session(autocommit=True, expire_on_commit=False):
    """Return a SQLAlchemy session."""
    global _MAKER
    maker = _MAKER

    if maker is None:
        engine = get_engine()
        maker = get_maker(engine, autocommit, expire_on_commit)

    session = maker()
    return session


def get_engine():
    """Return a SQLAlchemy engine."""
    global _ENGINE
    if _ENGINE:
        return _ENGINE

    db_uri = "mysql+pymysql://admin:admin@192.168.1.116:3306/stock"
    _ENGINE = sqlalchemy.create_engine(db_uri, encoding='utf-8', echo=False,
                                       connect_args={'charset': 'utf8'})
    return _ENGINE


def get_maker(engine, autocommit=True, expire_on_commit=False):
    """Return a SQLAlchemy sessionmaker using the given engine."""
    global _MAKER
    if _MAKER:
        return _MAKER

    _MAKER = sqlalchemy.orm.sessionmaker(bind=engine,
                                         autocommit=autocommit,
                                         expire_on_commit=expire_on_commit)
    return _MAKER

class StockCurrentInfo(Base):
    __tablename__ = 'stock_current_info'
    code = Column(String(10), primary_key=True)
    name = Column(String(10))
    high = Column(Float)
    low = Column(Float)
    ltsz = Column(Float)
    total_sz = Column(Float)
    turnover = Column(Float)
    volume = Column(Float)
    amount = Column(Float)
    pb = Column(Float)
    pe = Column(Float)
    date = Column(Date)


class StockCurrentHistory(Base):
    __tablename__ = 'stock_current_history'
    code = Column(String(10), primary_key=True)
    name = Column(String(10))
    time = Column(DateTime)
    type = Column(String(1))
    count = Column(Float)
    price = Column(Float)
    high = Column(Float)
    low = Column(Float)




class StockDaDantHistory(Base):
    __tablename__ = 'stock_dadan_history'
    id = Column(Integer, primary_key=True)
    code = Column(String(10))
    name = Column(String(10))
    date = Column(Date)
    time = Column(Time)
    type = Column(String(1))
    count = Column(Float)
    price = Column(Float)
    high = Column(Float)
    low = Column(Float)
