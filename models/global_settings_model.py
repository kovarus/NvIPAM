'''

Global settings model

'''

from run import db
from flask import app
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)


class GlobalSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dns1 = db.Column(db.String(20))
    dns2 = db.Column(db.String(20))
    domainname = db.Column(db.String(50))


class GlobalSettingsSchema(ma.ModelSchema):
    class Meta:
        model = GlobalSettings

