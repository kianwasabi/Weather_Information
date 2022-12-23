from flask import Flask,make_response , request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
from database.models import *
import socket
#from uuid import getnode as get_mac

hostname = socket.gethostname()
hostIP = socket.gethostbyname(hostname)
#mac = get_mac()

def message_in_Terminal(message):
    print("⬇️-----------msg-start-----------⬇️")
    print(message.headers)
    print(message.get_json())
    print("⬆️------------msg-end------------⬆️")

def api_response(key:str, hostIP:str, res_data:dict):
    '''
    Creates the REST APIs response message.
    :param key: (str) Process Key
    :param decive: (str) Server IP
    :param data: (dict) Payload
    :return: (*args: Any) -> Response 
    '''
    response = make_response(jsonify(res_data))
    response.headers.add("Key",key)
    response.headers.add("Device",hostIP)
    response.headers.add("Port","8080")
    message_in_Terminal(response)
    return response

def api_request():
    '''
    Handels the REST APIs request message.
    :param key: none
    :return req_data: (dict) payload in JSON object
    :return device: (str) Device IP = device_id in DB
    :return key: (str) Process Key
    '''
    req_data = request.get_json()
    #device = request.headers["Host"]
    device = 1 #Übergangslösung -> IN DB ändern! 
    key = request.headers["Key"]
    message_in_Terminal(request)
    return req_data, device, key

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/api')
def api():
    return render_template("api.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/api/post/requestrecipe/', methods = ['POST'])
def api_requestrecipe():
    # http request
    req_data, device, key = api_request()
    # server operation
    recipe = get_recipe_by_device_id(device)
    # http response 
    res_data = {
        "Response_Data":recipe
    }
    response = api_response(key,hostIP,res_data)
    return response

@app.route('/api/post/weatherinformation/refresh', methods=['POST'])
def api_post_weatherinformation_refresh():
    # http request
    req_data, device, key = api_request()
    #cityname = req_data["Location"]
    cityname = "Tokyo"
    # server operation
    _, time_refreshed = refresh_weatherinformation(cityname,device)
    # http response 
    res_data = {
        "Response_Data": 
            {"Status": f"Weatherinformation refreshed at {time_refreshed}."}
    }
    response = api_response(key,hostIP,res_data)
    return response

@app.route('/api/get/weatherinformation/all', methods=['GET'])
def api_get_weatherinformation_all():
    # http request
    req_data, device, key = api_request()
    # server operation 
    current_weather = get_current_weatherinformation()
    # http response 
    res_data = {
        "Response_Data": current_weather
    }
    response = api_response(key,hostIP,res_data)
    return response

@app.route('/api/get/sun/position', methods=['GET'])
def api_get_sun_position():
    # http request
    req_data, device, key = api_request()
    # server operation 
    sunposition = get_current_sunposition()
    # http response 
    res_data = {
        "Response_Data": sunposition
    }
    response = api_response(key,hostIP,res_data)
    return response

@app.route('/api/post/solarpanel/position', methods=['POST'])
def api_post_solarpanel_position():
    # http request
    req_data, device, key = api_request()
    value1 = req_data['Request_Data']['Value1']
    value2 = req_data['Request_Data']['Value2'] 
    # server operation - 
    _, time_saved = post_panelposition(value1,value2)
    # http response 
    res_data = {
        "Response_Data": 
        {
            "Status": f"Values saved to database: {time_saved}"
        }
    }
    response = api_response(key,hostIP,res_data)
    return response