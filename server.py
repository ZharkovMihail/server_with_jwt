import json
import redis
from flask import Flask, request, Response, make_response
import base64
from jwt.api_jwt import PyJWT

app = Flask(__name__)

d = {'write': '1', 'read': '2', 'delete': '3'}
HOST = 'rediska'
Key = '12345'

@app.route('/auth/')
def requestic4():
	user = request.authorization.username
	password = request.authorization.password
	if d.get(user) != None and d[str(user)] == password:
		payload = {"role": str(user)}
		jwt_Obj = PyJWT()
		jwt_token = jwt_Obj.encode(payload=payload, key=Key)
		rez = make_response(str(jwt_token, 'UTF-8'), 200)
		rez.headers['Authorization'] = str(jwt_token, 'UTF-8')
		return rez
	else:
		return make_response("invalid user or password" + str(user) + ' ' + str(password), 400)


@app.route('/<key>/', methods=['PUT'])
def requestic1(key):
	key = int("{}".format(key))
	data = json.loads(request.data)
	Jwt1 = request.headers['Authorization']
	message = data.get("message")
	try:
		jwt_Obj = PyJWT()
		decode_token = jwt_Obj.decode(str(Jwt1), key=Key)
		if decode_token['role'] == "write":
			if key == None or message == None:
				return Response(status=400)
			else:
				cache = redis.Redis(host=HOST, port=6379)
				cache.ping()
				if cache.exists(key):
					cache.delete(key)
					cache.set(key, json.dumps(message))
					return make_response("changed", 200)
				else:
					cache.set(key, json.dumps(message))
					return make_response({key: message}, 201)
		else:
			return make_response("invalid1 tiket", 400)
	except Exception:
		return make_response("invalid2 tiket", 400)


@app.route('/<key>/', methods=['GET'])
def requestic2(key):
	key=int("{}".format(key))
	Jwt1 = request.headers['Authorization']
	try:
		jwt_Obj = PyJWT()
		decode_token = jwt_Obj.decode(str(Jwt1), key=Key)
		if decode_token['role'] == "read":
			cache = redis.Redis(host = HOST, port=6379)
			cache.ping()
			if cache.exists(key):
				res = json.loads(cache.get(key))
				return make_response({"message": res}, 200)
			else:
				return Response(status=400)
		else:
			return make_response("invalid1 tiket", 400)
	except Exception:
		return make_response("invalid2 tiket", 400)


@app.route('/<key>/', methods=['DELETE'])
def requestic3(key):
	key=int("{}".format(key))
	Jwt1 = request.headers['Authorization']
	try:
		jwt_Obj = PyJWT()
		decode_token = jwt_Obj.decode(str(Jwt1), key=Key)
		if decode_token['role'] == "delete":
			cache = redis.Redis(host = HOST, port=6379)
			cache.ping()
			if key == None:
				return Response(status = 400)
			else:
				if cache.exists(key):
					res = json.loads(cache.get(key))
					cache.delete(key)
					return make_response({"message": res}, 204)
				else:
					return Response(status=404)
		else:
			return make_response("invalid1 tiket", 400)
	except Exception:
		return make_response("invalid2 tiket", 400)


if __name__ == '__main__':
	app.run(host = '0.0.0.0')