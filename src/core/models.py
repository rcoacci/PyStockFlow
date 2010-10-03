# -*- coding: UTF-8 -*-
'''
Created on 28/09/2010

@author: rodrigo
'''


from elixir.entity import Entity
from elixir.fields import Field
from elixir.options import using_options
from elixir.relationships import ManyToOne, OneToMany
import datetime
import logging
import sqlalchemy.types as types

def initDB(drop=False):

    from elixir import metadata, setup_all, drop_all, create_all
    from genericpath import exists
    from os import makedirs
    from posixpath import expanduser

    DB_NAME = "stockflow.sqlite"
    log = logging.getLogger(__name__)
    log.info("Inicializando o Core")
    dbpath = expanduser("~/.stockflow/")
    if not exists(dbpath):
        try:
            makedirs(dbpath)
        except OSError:
            log.warning("Nao foi possivel criar os diretorios, \
                usando o home do usuário.")
            dbpath = expanduser("~")

    metadata.bind = "".join(("sqlite:///", dbpath, DB_NAME))
    metadata.bind.echo = False

    setup_all()
    if(drop):
        drop_all()


    if not exists("".join((dbpath, DB_NAME))) or drop:
        log.debug("Criando tabelas...")
        create_all()

class Trade(Entity):
    Buy = "B"
    Sell = "S"

    stock = Field(types.String(length=10, convert_unicode=True), required=True)
    date = Field(types.DateTime(), default=datetime.datetime.now)
    type = Field(types.CHAR())
    price = Field(types.Float())
    quantity = Field(types.Integer())
    broker = ManyToOne("Broker")
    cost = Field(types.Float())

    using_options(shortnames=True, order_by='stock')

    def calculateCost(self):
        pass

class Broker(Entity):

    name = Field(types.String(255), required=True, unique=True)
    fixed_cost = Field(types.Float())
    volume_cost = Field(types.Float())
    custody_cost = Field(types.Float())
    trades = OneToMany("Trade")

    using_options(shortnames=True, order_by='name')

class Portfolio(object):

    def __init__(self, start, end, quotes):
        self.start = start
        self.end = end
        self.quotes = quotes

class Quote(object):

    def __init__(self, symbol, low, high, last, opening, volume):
        self.symbol = symbol
        self.min = min
        self.max = max
        self.last = last
        self.opening = opening
        self.volume = volume


