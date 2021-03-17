import flask
from flask import jsonify, request

app = flask.Flask(__name__)
app.config["DEBUG"] = True

users_list = [
    {
        'id': 1001,
        'name': 'Mohan Vamsi',
        'age': 23,
        'present_location': 'HYD',
        'phoneNumber': '9515261762',
        'loggedIn': False
    },
    {
        'id': 1002,
        'name': 'Bhavana',
        'age': 27,
        'present_location': 'TPTY',
        'phoneNumber': '8500692478',
        'loggedIn': False
    }
]

login_details = [
    {
        'id': 1001,
        'username': 'mohan1155',
        'password': 'mohan1111'
    },
    {
        'id': 1002,
        'username': 'bhavana',
        'password': 'bhavana123'
    }
]


@app.route('/', methods=['GET'])
def home():
    return "<h1>Home Page</h1>"


@app.route('/users', methods=['GET'])
def users():
    response = jsonify(users_list)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/user', methods=['GET'])
def user():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "NO ID specified"

    results = []

    for i in users_list:
        if i['id'] == id:
            results.append(i)
    return jsonify(results)


@app.route('/login', methods=['GET'])
def loginCheck():
    if 'username' in request.args:
        username = str(request.args['username'])
    else:
        return "Required username parameter"

    if 'password' in request.args:
        password = str(request.args['password'])
    else:
        return "Required Password parameter"

    success = False
    success_id = -1
    failure_id = -1

    for val in login_details:
        if val['username'] == username and val['password'] == password:
            success = True
            success_id = val['id']
        elif val['username'] == username and val['password'] != password:
            success = False
            failure_id = val['id']

    if success:
        result = []
        for value in users_list:
            if value['id'] == success_id:
                value['loggedIn'] = True
                return jsonify(value)
    elif not success:
        if failure_id == -1:
            return jsonify({"errorMessage": "No user found"})
        else:
            return jsonify({"errorMessage": "Invalid Password"})


@app.route('/logout', methods=['GET'])
def logout():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "NO ID specified"

    for val in users_list:
        if val['id'] == id and val['loggedIn']:
            val['loggedIn'] = False
            return jsonify(val)
    return jsonify({"errorMessage": "No User Found"})


app.run()
