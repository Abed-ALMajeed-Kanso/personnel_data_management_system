
from flask import Flask, make_response, request
from data import data

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route("/exp")
def index_explicit():
    resp = make_response({"message": "Hello World"})
    resp.status_code = 200
    return resp

@app.route("/data")
def get_data():
    try:
        if data and len(data) > 0:
            return {"message": f"Data of length {len(data)} found"}
        else:
            return {"message": "Data is empty"}, 500
    except NameError:
        return {"message": "Data not found"}, 404

@app.route("/name_search")
def name_search():
    query = request.args.get("q")
    if not query:
        return {"message": "Invalid input parameter"}, 422
    for person in data:
        if query.lower() in person["first_name"].lower():
            return person

@app.route("/count")
def count():
    try:
        return {"data count": len(data)}, 200
    except NameError:
        return {"message": "data not defined"}, 500

@app.route("/person/<var_name>")
def find_by_uuid(var_name):
    for person in data:
        if person["id"] == str(var_name):
            return person
    return {"message": "Person not found"}, 404

@app.route("/person/<uuid:id>", methods=['DELETE'])
def delete_by_uuid(id):
    for person in data:
        if person["id"] == str(id):
            data.remove(person)
            return {"message": f"Person with ID {id} deleted"}, 200
    return {"message": "person not found"}, 404

@app.route("/person", methods=['POST'])
def add_by_uuid():
    new_person = request.json
    if not new_person:
        return {"message": "Invalid input parameter"}, 422
    try:
        data.append(new_person)
    except NameError:
        return {"message": "data not defined"}, 500

    return {"message": f"{new_person['id']}"}, 200

if __name__ == "__main__":
    app.run(debug=True)
