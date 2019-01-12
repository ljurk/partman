from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse

class Categories(Resource):
    cursor = None
    def getCategories(self):
        self.cursor.execute("SELECT * FROM categories;")
        output = self.cursor.fetchone()
        print(output[0])
        cats=[]
        while output != None:
            cat = {'id': output[0],'name': output[1] }
            cats.append(cat)
            output = self.cursor.fetchone()
        return cats

    def get(self):
        return(jsonify({'categories':self.getCategories()}))

    def put(self):
        args = parser.parse_args()
        sqlCommand = "INSERT INTO categories(name) VALUES('" + args['name'] + "')"

        self.cursor.execute(sqlCommand)
        con.commit()
        #read new entry
        self.cursor.execute("SELECT * FROM categories ORDER BY id DESC LIMIT 1;")
        output = self.cursor.fetchone()
        part = {'id': output[0],'name': output[1]}
        return part, 201
