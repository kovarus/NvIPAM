from run import db
from utils import save_changes
from models.network_model import Tags, TagsSchema
from flask import jsonify


def save_new_tag(data):
    # see if the machine name already exists, add if not.
    print(data)
    tag = Tags.query.filter_by(name=data['name']).first()
    if not tag:
        new_tag = Tags(
            tag_id=None,
            name=data['name']
        )
        save_changes(new_tag)
        response_object = {
            'status': 'success',
            'message': 'Successfully added.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Tag with that name already exists.',
        }
        return response_object, 409


def get_all_tags():
    all_tags = Tags.query.all()
    tags_schema = TagsSchema(many=True)
    output = tags_schema.dump(all_tags).data
    # return jsonify({'data': output})
    return output

    # return Tags.query.all()


def get_a_tag(id):
    return Tags.query.filter_by(tag_id=id).first()


def update_a_tag(tag_id, data):
    ''' update a Tag name item '''
    tag = Tags.query.get(tag_id)

    if data['name'] != 'string':
        tag.name = data['name']

    ''' apply the changes '''
    db.session.commit()
    tag_schema = TagsSchema()
    output = tag_schema.dump(tag).data
    return output


def delete_tag(id):
    return jsonify({'in': 'progress'})

#
# def save_changes(data):
#     db.session.add(data)
#     db.session.commit()
