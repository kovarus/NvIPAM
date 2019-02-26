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

'''

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
