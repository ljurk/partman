# Product Service

# Import framework
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import psycopg2
from index import Index
from parts import Parts
from categories import Categories

# Instantiate the app
app = Flask(__name__)
api = Api(app)
app.config['JSON_SORT_KEYS'] = False
#host = 'http://localhost:5001/'
host = 'https://303.ddns.net/pm/api/'

#initiate parser for put
parser = reqparse.RequestParser()
parser.add_argument('id', type=int, store_missing=False)
#parser.add_argument('id', type=int, default=1, required=False,store_missing=False)
parser.add_argument('categoryId')
parser.add_argument('name')
parser.add_argument('description')
parser.add_argument('amount', type=int )

#db
con = psycopg2.connect( "dbname='partman' user='partman' host='pm-db' password='docker'")
cur = con.cursor()
output =""

Index.cursor = cur
Index.host = host
Parts.cursor = cur
Parts.parser = parser
Parts.connection = con
Categories.cursor = cur
Categories.parser = parser
Categories.connection = con

# Create routes
api.add_resource(Index, '/')
api.add_resource(Parts, '/parts')
api.add_resource(Categories, '/categories')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

