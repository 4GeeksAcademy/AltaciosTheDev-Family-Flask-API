"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS #allows resources on a web page to be requested from another domain
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__) #creates Flask app instance. Param reps current Py module.
app.url_map.strict_slashes = False # disables strict URL trailing slashes. Routes match with or without trailing slashes. 
CORS(app) #enables CORS support for the Flask application

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException) 
def handle_invalid_usage(error): 
    return jsonify(error.to_dict()), error.status_code #returns errors as dicts to json with code.

# when user GETS the base URL, we generate and return sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app) #sitemap is an index of URLs to preview the content effectively.

@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def post_member():
    new_member = request.json
    result_of_add = jackson_family.add_member(new_member)

    if result_of_add == True:
        return jsonify("Sucess: 1 new member added"), 200

    return jsonify("Bad request: Wrong info"), 400
    
@app.route("/member/<int:member_id>", methods=["GET", "DELETE"])
def retrieve_one_member(member_id):

    if request.method == "GET":
        result_of_request_member = jackson_family.get_member(member_id)

        if result_of_request_member:
            return jsonify(result_of_request_member), 200
        
        return jsonify(f"Bad request: No member with id {member_id} was found"), 404

    else:
        result_of_delete_member = jackson_family.delete_member(member_id)

        if result_of_delete_member:
            return jsonify({
                "done": True,
                "message": f"Member with id {member_id} successfully deleted"
            }), 200
        
        return jsonify(f"Bad request: No member with id {member_id} was found"), 404

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
