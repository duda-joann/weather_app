import pytest
from flask import request, jsonify

@app.route('/api/auth')
def auth():
    api_data = request.get_json("http://api.openweathermap.org/data/2.5/weather?q=Paris&appid=dfce6593bf021b63c0f93c369d4ad310&units=metric")


