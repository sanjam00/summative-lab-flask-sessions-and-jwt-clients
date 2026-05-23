"""
Notes app/Journal Entries
- Date/time last edited. If created: Date/Time created
- title
- body text
# using jwt
"""

from flask import make_response, jsonify, request, session
# from flask_migrate import Migrate
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request, jwt_required

from config import app, db, jwt, api
from models import User, UserSchema, JournalEntry, JournalEntrySchema

# @app.before_request
# def check_if_logged_in():
#   open_access_list = [
#     'signup',
#     'login'
#   ]

#   if (request.endpoint) not in open_access_list and (not verify_jwt_in_request()):
#     return {'error': '401 Unauthorized'}, 401
  
class Signup(Resource):
  def post(self):
    request_json = request.get_json()

    username = request_json.get('username')
    password = request_json.get('password')

    password_confirmation = request_json.get('password_confirmation')

    if password != password_confirmation:
      return {'error': 'Passwords do not match'}, 400

    user = User(
      username=username
    )
    user.password_hash = password

    try:
      db.session.add(user)
      db.session.commit()
      access_token = create_access_token(identity=user.id)
      return make_response(jsonify(token=access_token, user=UserSchema().dump(user)), 200)
    except IntegrityError:
      return {'errors': ['422 Unprocessable Entity']}, 422
    
class WhoAmI(Resource):
  @jwt_required()
  def get(self):
    user_id = get_jwt_identity()
        
    user = User.query.filter(User.id == user_id).first()
    
    return UserSchema().dump(user), 200
  
class Login(Resource):
  def post(self):

    username = request.json['username']
    password = request.json['password']

    user = User.query.filter(User.username == username).first()

    if user and user.authenticate(password):
      access_token = create_access_token(identity=str(user.id))
      return make_response(jsonify(token=access_token, user=UserSchema().dump(user)), 200)

    return {'errors': ['401 Unauthorized']}, 401
  
class JournalIndex(Resource):
  @jwt_required()
  def get(self):
    user_id = get_jwt_identity()

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    pagination = JournalEntry.query.filter(
        JournalEntry.user_id == user_id
    ).paginate(page=page, per_page=per_page, error_out=False)

    entries = pagination.items

    # return [JournalEntrySchema().dump(entry) for entry in entries], 200
    return {
    "entries": JournalEntrySchema(many=True).dump(entries),
    "total_pages": pagination.pages,
    "current_page": page,
    "has_next": pagination.has_next,
    "has_prev": pagination.has_prev
    }, 200

  @jwt_required()
  def post(self):
    request_json = request.get_json()

    entry = JournalEntry(
      title=request_json.get('title'),
      body=request_json.get('body'),
      user_id=get_jwt_identity()
    )

    try:
      db.session.add(entry)
      db.session.commit()
      return JournalEntrySchema().dump(entry), 201
    except IntegrityError:
      return {'errors': ['422 Unprocessable Entity']}, 422
    
class JournalByID(Resource):

  # get by id
  @jwt_required()
  def get(self, id):

    entry = JournalEntry.query.filter(
      JournalEntry.id == id,
      JournalEntry.user_id == get_jwt_identity()
    ).first()

    if not entry:
      return {'error': '404 Entry not found'}, 404

    return JournalEntrySchema().dump(entry), 200
  
  # update
  @jwt_required()
  def patch(self, id):
    entry = JournalEntry.query.filter(
        JournalEntry.id == id,
        JournalEntry.user_id == get_jwt_identity()
      ).first()

    if not entry:
      return {'error': '404 Entry not found'}, 404

    request_json = request.get_json()

    if 'title' in request_json:
      entry.title = request_json['title']

    if 'body' in request_json:
      entry.body = request_json['body']

    db.session.commit()

    return JournalEntrySchema().dump(entry), 200

  # delete
  @jwt_required()
  def delete(self, id):
    entry = JournalEntry.query.filter(
      JournalEntry.id == id,
      JournalEntry.user_id == get_jwt_identity()
    ).first()

    if not entry:
      return {'error': '404 Entry not found'}, 404

    db.session.delete(entry)

    db.session.commit()

    return {}, 204
  
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(WhoAmI, '/me', endpoint='me')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(JournalIndex, '/entries')
api.add_resource(JournalByID, '/entries/<int:id>')

if __name__ == '__main__':
  app.run(port=5555, debug=True)