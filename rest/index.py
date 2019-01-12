from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse

class Index(Resource):
    cursor = None
    host = None
    def getCategories(self):
        self.cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE tableowner = 'partman';")
        output = self.cursor.fetchone()
        print(output[0])
        cats=[]
        while output != None:
            cat = {'path': self.host + output[0]}
            cats.append(cat)
            output = self.cursor.fetchone()
        return cats

    def get(self):
        return(jsonify({'categories':self.getCategories()}))

