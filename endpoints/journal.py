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
        return jsonify('failed', 401)

@app.get('/api/all-task')
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
        return jsonify('failed', 401)



