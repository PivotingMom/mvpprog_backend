from app import app
from flask import Flask, jsonify, request
import json
from db_helpers import run_query
from flask_cors import CORS
import os
import datetime
from datetime import datetime, timedelta
import bcrypt
import uuid
from endpoints import client




@app.post('/api/client_login')
def client_login():
    request_payload = request.get_json()
    query = 'SELECT * FROM client WHERE email=?'

    email = request_payload.get('email')
    password = request_payload.get('password')

    
    result =run_query(query, [email])

    print(result)
    if not result:
        if (not email or not len(email)):
            return jsonify({'message': 'Incorrect email'}), 401
    if not password:
        return jsonify({'message': 'No password defined'}), 401
        
    try:
        if bcrypt.checkpw(password.encode(), result[0][5].encode()):

            token=str(uuid.uuid4())
            run_query( 'INSERT INTO client_session (token, client_Id) VALUES (?,?)', [token, result[0][0]])
            
            
            return jsonify({'clientId':result[0][0],'token':token}), 200
        else:
            return jsonify(result, 401)
    except Exception as e:
        return jsonify({'message': 'Incorrect password'}), 401


def get_client_Id(token):
    max_token_age = datetime.datetime.utcnow() - datetime.timedelta(minutes=720)
    print(max_token_age)
    
    query = 'SELECT client_Id from client_session WHERE token = ? AND created_at > ?' 
    result = run_query(query, (token, max_token_age))
    if result:
        return result[0][0]
    else: 
        return None
    
@app.delete('/api/client_login')
def client_login_delete():
    token = request.headers.get('token')
    client_Id = get_client_Id(token)
    if client_Id:
        query = 'DELETE from client_session WHERE client_Id = ?'
        run_query(query, (client_Id,))
        
        #query = 'DELETE from client_session WHERE token =?'
        #run_query(query, (token,)))
        
        return jsonify('token deleted', 204) 
    else: 
        return jsonify('no token to delete', 401)
    





    
