from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from sql import Sql

sql = Sql()

class Categories(Resource):
    cursor = None
    parser = None
    connection = None
    def __init__(self):
        sql.cursor = self.cursor
        sql.connection = self.connection

    def get(self):
        return(jsonify({'categories':sql.getObjects('categories',0)}))

    def put(self):
        args = self.parser.parse_args()
        sqlCommand = "INSERT INTO categories(name) VALUES('" + args['name'] + "')"

        self.cursor.execute(sqlCommand)
        self.connection.commit()
        #read new entry
        self.cursor.execute("SELECT * FROM categories ORDER BY id DESC LIMIT 1;")
        output = self.cursor.fetchone()
        part = {'id': output[0],'name': output[1]}
        return part, 201

    def delete(self):
        args = self.parser.parse_args()
        sqlCommand = "DELETE FROM categories WHERE id = " + str(args['id']) + ";"
        self.cursor.execute(sqlCommand)
        return 200
