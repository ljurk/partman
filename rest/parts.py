from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse


class Parts(Resource):
    cursor = None
    parser = None
    connection = None
    def getParts(self):
        sql ='SELECT p.id,  c.name,p.name, p.friendlyName, a.amount FROM parts as p LEFT JOIN amounts as a ON p.id=a.partid LEFT JOIN categories as c ON c.id = p.categoryId ORDER BY p.id;'

        self.cursor.execute(sql)
        output = self.cursor.fetchone()
        parts=[]
        while output != None:
            part = {'id': output[0],'category': output[1], 'name': output[2], 'friendlyName': output[3], 'amount': output[4] }
            parts.append(part)
            output = self.cursor.fetchone()
        return parts

    def get(self):
        return(jsonify({'parts':self.getParts()}))

    def put(self):
        args = self.parser.parse_args()
        cat = int(args['categoryId']) ;
        sqlCommand = "INSERT INTO parts(categoryId,name,friendlyName) VALUES(" + str(cat) + ",'" + args['name'] + "','" + args['friendlyName']+"')"

        self.cursor.execute(sqlCommand)
        self.connection.commit()
        #read new entry
        self.cursor.execute("SELECT * FROM parts ORDER BY id DESC LIMIT 1;")
        output = self.cursor.fetchone()
        part = {'id': output[0],'categoryId': output[1], 'name': output[2], 'friendlyName': output[3] }
        return part, 201
