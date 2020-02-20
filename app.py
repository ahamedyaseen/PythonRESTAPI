from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import pymongo
from flask_cors import CORS
from bson.objectid import ObjectId


app = Flask(__name__)
CORS(app)
api = Api(app)
app.config['MONGO_DBNAME'] = 'attendance'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/attendance'

myclient = pymongo.MongoClient('mongodb://localhost:27017/attendance')
db = myclient['attendance']
mycol = db['addattendance']


class RequestAttendance(Resource):
    # Corresponds to POST request
    def post(self):
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        
        print(json_data)
        x = mycol.insert_one(json_data)
        #print(x)
        return {'result': 'success'},201

class GetAttendanceRequest(Resource):
    def get(self):
        attendance_request = []    
        for data in mycol.find({}):
            data['_id'] = str(data['_id'])
            attendance_request.append(data)
        return attendance_request

class GetApprovalList(Resource):
    def get(self):
        attendance_request = []    
        for data in mycol.find({"approval_status" : "Pending"}):
            data['_id'] = str(data['_id'])
            attendance_request.append(data)
        return attendance_request

class DeleteRequest(Resource):
    def get(self):
        mycol.delete_one({"_id":ObjectId(request.args["id"])})
        return {"success":"success"},200

class ApprovalRequest(Resource):
    def get(self):
        mycol.update_one({"_id":ObjectId(request.args["id"])},{"$set": { "approval_status": request.args["approve"] }})
        return {"success":"success"},200


api.add_resource(RequestAttendance, '/addAttendance')
api.add_resource(GetAttendanceRequest, '/getAttendance')
api.add_resource(DeleteRequest,'/deleteRequest')
api.add_resource(ApprovalRequest,'/approve')
api.add_resource(GetApprovalList,'/approval_list')

if __name__ == '__main__':
    app.run(debug=True)

			