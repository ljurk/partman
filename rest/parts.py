from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse


class Parts(Resource):
    cursor = None
    def getParts(self):
        self.cursor.execute("SELECT * FROM parts;")
        output = self.cursor.fetchone()
        print(output[0])
        parts=[]
        while output != None:
            part = {'id': output[0],'categoryId': output[1], 'name': output[2], 'friendlyName': output[3] }
            parts.append(part)
            output = self.cursor.fetchone()
        return parts

    def get(self):
        return(jsonify({'parts':self.getParts()}))

    def put(self):
        args = parser.parse_args()
        sqlCommand = "INSERT INTO parts(categoryId,name,friendlyName) VALUES(" + args['categoryId'] + ",'" + args['name'] + "','" + args['friendlyName']+"')"

        self.cursor.execute(sqlCommand)
        con.commit()
        #read new entry
        self.cursor.execute("SELECT * FROM parts ORDER BY id DESC LIMIT 1;")
        output = self.cursor.fetchone()
        part = {'id': output[0],'categoryId': output[1], 'name': output[2], 'friendlyName': output[3] }
        return part, 201
