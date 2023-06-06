from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Table, Numeric
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

engine = create_engine('sqlite:///main.db')


card_tribe = Table('cards_tribes', Base.metadata,
                   Column('card_id', Integer, ForeignKey('cards.id')),
                   Column('tribe_id', Integer, ForeignKey('tribes.id'))
                   )


card_sigil = Table('cards_sigils', Base.metadata,
                   Column('card_id', Integer, ForeignKey('cards.id')),
                   Column('sigil_id', Integer, ForeignKey('sigils.id'))
                   )


class Tribe(Base):
    __tablename__ = 'tribes'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)


class Sigil(Base):
    __tablename__ = 'sigils'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    description = Column(String(255), nullable=False)


class Card(Base):
    __tablename__ = 'cards'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    cost = Column(Numeric(2), nullable=True)
    cost_type = Column(String(8), nullable=True)
    power = Column(Numeric(2), nullable=True)
    health = Column(Numeric(2), nullable=True)
    traits = Column(String(255), nullable=True)
    grown_id = Column(Integer, ForeignKey('cards.id'), nullable=True)
    grown = relationship('Card', backref='fledgling', remote_side=[id])
    image = Column(String(32), nullable=False)
    tribes = relationship('Tribe', secondary=card_tribe)
    sigils = relationship('Sigil', secondary=card_sigil)


Base.metadata.create_all(engine)
