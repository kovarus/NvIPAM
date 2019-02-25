'''

Adding Networks, pools, ip assignments and tags to this model due to the relationship between the tables.

'''

from run import db
from flask import app
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)


''' add tag junction table '''
tags_junction_table = db.Table('tags_junction_table',
                               db.Column('tag_id', db.Integer, db.ForeignKey('tags.tag_id')),
                               db.Column('network_id', db.Integer, db.ForeignKey('networks.id')),
                               db.Column('pool_id', db.Integer, db.ForeignKey('network_pools.id')),
                               db.Column('assignment_id', db.Integer, db.ForeignKey('pool_assignments.id'))
                               )

''' add Tags class '''


class Tags(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


class TagsSchema(ma.ModelSchema):
    class Meta:
        model = Tags


class PoolAssignments(db.Model):
    """ User Model for storing network related details """
    __tablename__ = "pool_assignments"

    id = db.Column(db.Integer, primary_key=True)
    ipaddress = db.Column(db.String(20))
    machinename = db.Column(db.String(50))
    status = db.Column(db.Integer, default=0)
    rangeid = db.Column(db.Integer, db.ForeignKey('network_pools.id'))
    assignment_tag = db.relationship('Tags', secondary=tags_junction_table, backref=db.backref('assignment_tag'), lazy='dynamic')


class PoolAssignmentsSchema(ma.ModelSchema):
    class Meta:
        model = PoolAssignments


class NetworkPools(db.Model):
    """ Model for storing network related details """
    __tablename__ = "network_pools"

    id = db.Column(db.Integer, primary_key=True)
    poolname = db.Column(db.String(50))
    poolrange = db.Column(db.String(20))
    subnetmask = db.Column(db.String(20))
    gateway = db.Column(db.String(20))
    dns1 = db.Column(db.String(20))
    dns2 = db.Column(db.String(20))
    domainname = db.Column(db.String(50))
    owner_id = db.Column(db.Integer, db.ForeignKey('networks.id'))
    hostips = db.relationship('PoolAssignments', backref='ipowner')
    pool_tag = db.relationship('Tags', secondary=tags_junction_table, backref=db.backref('pool_tag'), lazy='dynamic')


class PoolsSchema(ma.ModelSchema):
    class Meta:
        model = NetworkPools


class Networks(db.Model):
    """ User Model for storing network related details """
    __tablename__ = "networks"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(75))
    networkname = db.Column(db.String(50))
    vlanid = db.Column(db.String(25))
    datacenter = db.Column(db.String(50))
    cluster = db.Column(db.String(50))
    subnets = db.relationship('NetworkPools', backref='owner', lazy='joined')
    network_tag = db.relationship('Tags', secondary=tags_junction_table, backref=db.backref('network_tag'), lazy='dynamic')


class NetworksSchema(ma.ModelSchema):
    class Meta:
        model = Networks




