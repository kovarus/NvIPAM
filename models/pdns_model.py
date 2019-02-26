'''


BSD 3-Clause License

Copyright (c) 2019, Kovarus
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Assuming an existing pdns database.  The intent here is to use the existing Metadata as the model, rather than define
something new.

Reference: https://docs.sqlalchemy.org/en/latest/orm/extensions/automap.html

'''

from run import db
from flask import app
from sqlalchemy import MetaData
from flask_marshmallow import Marshmallow
from sqlalchemy.ext.automap import automap_base

metadata=MetaData()


''' using db.engine rather than creating a new one. '''
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

