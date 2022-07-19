from app import app
from flask import Flask, jsonify, request
import json
from db_helpers import run_query
from flask_cors import CORS
import os
import datetime
import bcrypt
import uuid
from endpoints import client
from endpoints.client import get_client_Id


@app.post('/api/create-journal')
def create_journal():
    request_payload = request.get_json()
    print(request_payload)
   # token = request.headers.get('token')
  
   # client_Id = get_client_Id(token)
    client_Id = request_payload.get('client_id')
    
    print(client_Id)
    #date = datetime.datetime.fromutc(float(request_payload.get('Date')))
    
    if client_Id:
        query = 'INSERT INTO journal (client_id, title, content, date) VALUES (?,?,?,?)'

        Title = request_payload.get('Title')
        Content = request_payload.get('content')
        Date = request_payload.get('Date')
        #Date = date.strftime('%Y-%m-%d %H:%M:%S')

        result = run_query(query, (client_Id,Title, Content, Date))
        
        print(result)
      
        return jsonify('Journal note created', 200)
    else:
        return jsonify('failed'), 401

@app.get('/api/all-journal')
def fetch_all_entry():
  token = request.headers.get('token')
    
  client_Id = get_client_Id(token)
  print(client_Id)
  if client_Id:
    
        query = 'SELECT * FROM journal where client_id=?'


        result = run_query(query, (client_Id,))
        print(result)
        
        return jsonify(result)
      
  else:
        return jsonify('failed'), 401

# sorry I know we discussed this, but  i just couldnt think through that logic in these case
# """ # Using named parameters in the decorator
# # Vs. query parameters and JSON
# # Since this route is only getting one parameter
# https://flask.palletsprojects.com/en/2.1.x/quickstart/#rendering-templates """

@app.get('/api/journal/<id>')
def fetch_single_entry(id):
    token = request.headers.get('token')
    #entry_id = id or request.args.get('id', default=1, type = int)
    
    #print(entry_id)
    
    client_Id = get_client_Id(token)
    if client_Id:
    
        query = 'SELECT * FROM journal where id=?'
        
        result = run_query(query, (id,))

        return jsonify(result[0])


    else:
        return jsonify('Unauthorized', 401)
    
    
@app.delete('/api/journal/<id>')
def delete_entry(id):
    token = request.headers.get('token')
    client_Id = get_client_Id(token)
    if client_Id:
    
        query = 'DELETE from journal where id=?'
        
        result = run_query(query, (id,))

        return jsonify('journal entry deleted', 200) 

    else:
        return jsonify('Unsuccessful', 400)


@app.patch('/api/journal/<id>')
def update_entry(id):
    data=request.get_json()
    token = request.headers.get('token')
    
    client_Id = get_client_Id(token)
    
    if client_Id:
        Title = data.get('Title')
        Content = data.get('content')
        #Date = data.get('Date')
        #Date = date.strftime('%Y-%m-%d %H:%M:%S')

        query = 'UPDATE journal SET title=?, content=?  WHERE id = ?'
        result = run_query(query, (Title, Content, id)) 
        
        return jsonify('entry updated', 200) 
    
    else:
        return jsonify('no journal entry', 400)