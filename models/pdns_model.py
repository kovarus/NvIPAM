'''

PDNS model

'''

from run import db
from flask import app
from sqlalchemy import MetaData
from flask_marshmallow import Marshmallow
from sqlalchemy.ext.automap import automap_base

metadata=MetaData()

metadata.reflect(db.engine, only=['domains', 'records'])

Base = automap_base(metadata=metadata)

Base.prepare()

Domains, Records = Base.classes.domains, Base.classes.records
# Base = automap_base()
#
# # engine, suppose it has two tables 'user' and 'address' set up
# # engine = db.connect
# Base.prepare(db.engine, reflect=True)
#
#
# Domains = Base.classes.domains
# Records = Base.classes.records

ma = Marshmallow(app)

# # db.Model.metadata.reflect(only=['domains','records'],db.engine.connect())
# db.Model.metadata.reflect(only=['domains','records'])
#
# class Domains(db.Model):
#     __table__ = db.Model.metadata.tables['domains']


class DomainsSchema(ma.ModelSchema):
    class Meta:
        model = Domains


# class Records(db.Model):
#     __table__ = db.Model.metadata.tables['records']


class RecordsSchema(ma.ModelSchema):
    class Meta:
        model = Records
        include_fk = True

