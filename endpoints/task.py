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

def get_client_Id(token):
    max_token_age = datetime.datetime.utcnow() - datetime.timedelta(minutes=60)
    print(max_token_age)
    
    query = 'SELECT client_Id from client_session WHERE token = ? AND created_at > ?' 
    result = run_query(query, (token, max_token_age))
    if result:
        return result[0][0]
    else: 
        return None

# route to create new task
@app.post('/api/create-task')
def create_task():
    request_payload = request.get_json()
    token = request.headers.get('token')
    
    client_Id = get_client_Id(token)
    if client_Id:
        query = 'INSERT INTO tasks (clientId, taskTitle, taskDesc, startDate, startTime, endDate, endTime, taskPriority, taskStatus) VALUES (?,?,?,?,?,?,?,?,?)'
        userId = client_Id
        taskTitle = request_payload.get('taskTitle')
        taskDesc = request_payload.get('taskDesc')
        startDate = request_payload.get('startDate').replace("/", "-")
        startTime = request_payload.get('startTime')
        endDate = request_payload.get('endDate').replace("/", "-")
        endTime = request_payload.get('endTime')
        taskPriority = request_payload.get('taskPriority').capitalize()
        taskStatus = 'Pending'

        result = run_query(query, (userId, taskTitle, taskDesc, startDate, startTime, endDate, endTime,taskPriority, taskStatus))
        
        print(result)
        
        
        return jsonify('Task created'), 200
    else:
        return jsonify('failed'), 401



# route to select all created task 
@app.get('/api/all-tasks')
def fetch_all_tasks():
    token = request.headers.get('token')
    
    client_Id = get_client_Id(token)
    print(client_Id)
    if client_Id:
    
        query = 'SELECT * FROM tasks where client_id=?'
        
        result = run_query(query, (client_Id,))
        print(result)

        return jsonify(result)

    else:
        return jsonify('failed'), 401


# Using named parameters in the decorator
# # Vs. query parameters and JSON
# # Since this route is only getting one parameter
# https://flask.palletsprojects.com/en/2.1.x/quickstart/#rendering-templates
# sorry I know we discussed this, but  i just couldnt think through that logic in these case

@app.get('/api/task/<id>')
def fetch_single_task(id):
    token = request.headers.get('token')
    
    client_Id = get_client_Id(token)
    if client_Id:
    
        query = 'SELECT * FROM tasks where id=?'
        
        result = run_query(query, (id,))

        return jsonify(result[0])

        # return jsonify({
        #     'client_Id': result[0][0],
        #     'email': result[0][1],
        #     'username': result[0][2],
        #     'password': result[0][3],
        #     'name': result[0][4],
        # })
    else:
        return jsonify('Unauthorized'), 401


# route to delete a single task
@app.delete('/api/task/<id>')
def delete_task(id):
    token = request.headers.get('token')
    client_Id = get_client_Id(token)
    if client_Id:
    
        query = 'DELETE from tasks where id=?'
        
        result = run_query(query, (id,))

        return jsonify('Task deleted'), 200 

    else:
        return jsonify('Unauthorized'), 401


# route to update a single task
@app.patch('/api/task/<id>')
def update_task(id):
    data=request.get_json()
    token = request.headers.get('token')
    
    client_Id = get_client_Id(token)
    if client_Id:
        taskTitle = data.get('taskTitle')
        taskDesc = data.get('taskDesc')
        startDate = data.get('startDate')
        startTime = data.get('startTime')
        endDate = data.get('endDate')
        endTime = data.get('endTime')
        taskPriority = data.get('taskPriority')
        taskStatus = data.get('taskStatus')

        print(client_Id)
        
        query = 'UPDATE tasks SET taskTitle=?, taskDesc=?, startDate=?, startTime=?, endDate=?, endTime=?, taskPriority=?, taskStatus=? WHERE id = ?'
        
        result = run_query(query, (taskTitle, taskDesc, startDate, startTime, endDate, endTime, taskPriority, taskStatus, id)) 
        
        return jsonify('client updated'), 200
    
    else: 
        return jsonify('Unauthorized'), 401