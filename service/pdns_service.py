from run import db
from utils import save_changes
from models.pdns_model import Domains, DomainsSchema, Records, RecordsSchema
from flask import jsonify


def GetDomains():
    # myDomains = Domains.query.all()
    myDomains = db.session.query(Domains).all()
    domains_schema = DomainsSchema(many=True)
    result = domains_schema.dump(myDomains).data
    print({'data': result})
    return {'data': result}


def GetRecords():
    # myRecords = Records.query.all()
    myRecords = db.session.query(Records).all()
    records_schema = RecordsSchema(many=True)
    result = records_schema.dump(myRecords).data
    print({'data': result})
    return {'data': result}
