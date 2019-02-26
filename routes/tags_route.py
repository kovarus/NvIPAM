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
from flask import request
from service.tags_service import save_new_tag, get_all_tags, get_a_tag, update_a_tag
from flask_restplus import Resource, Namespace, reqparse, fields
from flask_jwt_extended import jwt_required

api = Namespace('tags', description='Tags related operations')


''' adding models for marshalling '''


class TagsDto:
    tags = api.model('tag_operations', {
        'tag_id': fields.Integer(description='Unique tag id'),
        'name': fields.String(description='Tag name')
    })


@api.route('/')
class GetTags(Resource):
    @jwt_required
    @api.marshal_list_with(TagsDto.tags, envelope='data')
    def get(self):
        """Get all tags """
        return get_all_tags()

    @jwt_required
    @api.expect(TagsDto.tags)
    def post(self):
        """Creates a new tag """
        data = request.json
        return save_new_tag(data=data)


@api.route('/<id>')
class GetTag(Resource):
    @jwt_required
    @api.marshal_list_with(TagsDto.tags, envelope='data')
    def get(self, id):
        """Get a tag by id """
        return get_a_tag(id)

    @jwt_required
    @api.expect(TagsDto.tags)
    def put(self, id):
        """Update a tag name by id """
        data = request.json
        return update_a_tag(id, data)





