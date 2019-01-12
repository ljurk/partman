# Product Service

# Import framework
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import psycopg2

# Instantiate the app
app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False
host = 'http://localhost:5001/'

#initiate parser for put
parser = reqparse.RequestParser()
parser.add_argument('categoryId')
parser.add_argument('name')
parser.add_argument('friendlyName')

#db
con = psycopg2.connect( "dbname='partman' user='partman' host='partmandb' password='docker'")
cur = con.cursor()
output =""

class Parts(Resource):
    def getParts(self):
        cur.execute("SELECT * FROM parts;")
        output = cur.fetchone()
        print(output[0])
        parts=[]
        while output != None:
            part = {'id': output[0],'categoryId': output[1], 'name': output[2], 'friendlyName': output[3] }
            parts.append(part)
            output = cur.fetchone()
        return parts

    def get(self):
        return(jsonify({'parts':self.getParts()}))

    def put(self):
        args = parser.parse_args()
        sqlCommand = "INSERT INTO parts(categoryId,name,friendlyName) VALUES(" + args['categoryId'] + ",'" + args['name'] + "','" + args['friendlyName']+"')"

        cur.execute(sqlCommand)
        con.commit()
        #read new entry
        cur.execute("SELECT * FROM parts ORDER BY id DESC LIMIT 1;")
        output = cur.fetchone()
        part = {'id': output[0],'categoryId': output[1], 'name': output[2], 'friendlyName': output[3] }
        return part, 201


class Categories(Resource):
    def getCategories(self):
        cur.execute("SELECT * FROM categories;")
        output = cur.fetchone()
        print(output[0])
        cats=[]
        while output != None:
            cat = {'id': output[0],'name': output[1] }
            cats.append(cat)
            output = cur.fetchone()
        return cats

    def get(self):
        return(jsonify({'categories':self.getCategories()}))

    def put(self):
        args = parser.parse_args()
        sqlCommand = "INSERT INTO categories(name) VALUES('" + args['name'] + "')"

        cur.execute(sqlCommand)
        con.commit()
        #read new entry
        cur.execute("SELECT * FROM categories ORDER BY id DESC LIMIT 1;")
        output = cur.fetchone()
        part = {'id': output[0],'name': output[1]}
        return part, 201

class index(Resource):
    def getCategories(self):
        cur.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE tableowner = 'partman';")
        output = cur.fetchone()
        print(output[0])
        cats=[]
        while output != None:
            cat = {'path': host + output[0]}
            cats.append(cat)
            output = cur.fetchone()
        return cats

    def get(self):
        return(jsonify({'categories':self.getCategories()}))

# Create routes
api.add_resource(index, '/')
api.add_resource(Parts, '/parts')
api.add_resource(Categories, '/categories')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

