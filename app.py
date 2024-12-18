
from bson.objectid import ObjectId
from flask import Flask, jsonify, request
from flask_cors import CORS
import datetime
from db import db
from utility import parse_json

app = Flask(__name__)

# handle cors
CORS(app)

@app.route('/api/health', methods=['GET']) 
def healthCheck(): 
	return "Contact App is running..."

@app.route('/api/upsert-contact', methods=["POST"])
def createContact():
	try:
		# extract data from request
		data = request.get_json()
		id = data.get("id")
		first_name = data["first_name"].lower()
		last_name = data["last_name"].lower()
		phone_number = data["phone_number"]
		email =data["email"].lower()
		label_ids = data["label_ids"]
		note= data["note"]
		address = data["address"]
		dob = data["dob"]

		if id is None:
			print('caommm')
			# inserting into document 
			db.contacts.insert_one({
				"first_name":first_name,
				"last_name":last_name,
				"phone_number":phone_number,
				"email":email,
				"label_ids":label_ids,
				"note":note,
				"address":address,
				"dob":dob,
				"is_delete":False,
				"dateCreated":datetime.datetime.now()
			})
			print('contact created')
			return jsonify({"isCreated":True}), 200
		else:
			#edit document based on id
			db.contacts.find_one_and_update({"_id":ObjectId(id)},{"$set":{
				"first_name":first_name,
				"last_name":last_name,
				"phone_number":phone_number,
				"email":email,
				"label_ids":label_ids,
				"note":note,
				"address":address,
				"dob":dob,
			}})
			return jsonify({"isUpdated":True}), 200
			
	except:
		print('error while creating/updating contact..')
		return jsonify({"isCreated":False, "isUpdated":False, "msg":"error white creating/updating contact"}), 500

@app.route('/api/create-label', methods=["POST"])
def createLabel():
	try:
		data = request.get_json()
		title = data["title"]
		result = db.label.find_one({"title":title})
		if result is None:
			print("not found")
			db.label.insert_one({"title":title})
			return jsonify({"isCreated":True,"msg":"label is created"}), 200
		else:
			print("label is already presnet")
			return jsonify({"isCreated":False,"msg":"label is already there"}), 200
		
	except:
		print('getting error')

@app.route('/api/fetch-contacts',methods=["GET"])
def fetchContactList():
	try:
		search = request.args.get('search')	
		if search:
			print('searching')
			match = {"is_delete":False, "first_name":search}
		else:
			match = {"is_delete":False}
		
		result = db.contacts.find(match).sort({"first_name":1})
		print("contact fetchs")
		return list(parse_json(result)), 200
	except:
		return jsonify({"msg":"error while fetching contacts"}), 500

@app.route('/api/fetch-labels', methods=["GET"])
def fetchLabelList():
	try:
		result = db.label.find()
		print("labels fetchs")
		return list(parse_json(result)), 200
	except:
		return jsonify({"msg":"error while fetch lables"}), 500

@app.route('/api/delete-contact', methods=["POST"])
def deleteContact():
	try:
		data = request.get_json()
		id = data["id"]

		db.contacts.find_one_and_update({"_id":ObjectId(id)},{
			"$set" : {"is_delete":True}
		})

		return jsonify({"isDeleted": True}), 200

	except:
		print("some error during delete contact")
		return jsonify({"isDeleted":False}), 500

	

if __name__ == '__main__': 
	app.run(debug=True) 
