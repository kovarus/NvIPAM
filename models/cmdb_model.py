'''

CMDB model

'''

from run import db
from flask import app
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)


class CmdbData(db.Model):
    """ User Model for storing network related details """
    __tablename__ = "cmdb_data"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    machinename = db.Column(db.String)
    ipaddress = db.Column(db.String)
    network = db.Column(db.String)
    mem = db.Column(db.Integer)
    cpus = db.Column(db.Integer)
    disk = db.Column(db.Integer)
    os = db.Column(db.String)
    datacenter = db.Column(db.String)


class CmdbSchema(ma.ModelSchema):
    class Meta:
        model = CmdbData
