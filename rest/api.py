# Product Service

# Import framework
from flask import Flask, jsonify
from flask_restful import Resource, Api
import psycopg2 

# Instantiate the app
app = Flask(__name__)
api = Api(app)

#db
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
#%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

print( "dbname=partman user=partman host=partmandb password=docker")
con = psycopg2.connect( "dbname='partman' user='partman' host='partmandb' password='docker'")
cur = con.cursor()
output =""
class Product(Resource):
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

# Create routes
api.add_resource(Product, '/')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)

