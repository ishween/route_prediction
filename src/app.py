# from flask import Flask, render_template
#
# app = Flask(__name__)
# app.secret_key = 'ishween'
# app.config.from_object('config')
#
# @app.route('/')
# def home():
#     return render_template('home.html')
#
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# @app.route('/square/', methods=['POST'])
# def square():
#     num = float(request.form.get('number', 0))
#     square = num ** 2
#     data = {'square': square}
#     data = jsonify(data)
#     return data

@app.route('/square/', methods=['GET','POST'])
def square():
    source = request.form.get('source')
    destination = request.form.get('destination')

    #oauth tokens api
    # oauth = "https://outpost.mapmyindia.com/api/security/oauth/token"
    parameters = {"grant_type": "client_credentials",
                    "client_id": "O3wMiHiw95v3LsJ-IiCHxZ2HM2c8F5H8xfdzLnrPdbEkNGsIbvSqKhFUmMHjOz3u1eeu1aIREb42bpDzRij_bA==",
                    "client_secret": "QJcH6ymTGazxFG8ml9UT-UFotuIYSvB-rWynBvJFd1HJULek4Si3KfyimmwjmlKcQVMHwVW8e-rO7J9VaufHgY6XBMp0LC1O"}
    resp = requests.post("https://outpost.mapmyindia.com/api/security/oauth/token", params=parameters)
    tokens = resp.json()
    access_token = tokens['access_token']
    token_type = tokens['token_type']
    print(access_token)
    print(token_type)

    #geocoding api
    address_source = "https://atlas.mapmyindia.com/api/places/geocode?address={}".format(source)
    headers = '{}'.format(token_type+" "+access_token)
    location_source = requests.get(address_source, headers={'Authorization':headers})
    json_source = location_source.json()
    source_longitude = json_source['copResults']['longitude']
    source_latitude = json_source['copResults']['latitude']
    print(json_source)

    address_destination = "https://atlas.mapmyindia.com/api/places/geocode?address={}".format(destination)
    headers = '{}'.format(token_type + " " + access_token)
    location_destination = requests.get(address_destination, headers={'Authorization': headers})
    json_destination = location_destination.json()
    destination_longitude = json_destination['copResults']['longitude']
    destination_latitude = json_destination['copResults']['latitude']
    print(json_destination)

    #multiple lat long api
    # arr = {'square':"source_latitude, source_longitude+destination_latitude+,+destination_longitude"}
    # print(arr)
    str = "https://apis.mapmyindia.com/advancedmaps/v1/ejls5j1jcdu6z9w1pabuytir9wwituo8/route_adv/driving/{},{};{},{}?steps=false&rtype=1".format(source_longitude, source_latitude, destination_longitude, destination_latitude)
    resp = requests.get(str)
    route = resp.json()
    geometry = route['routes'][0]['geometry']
    arr = {'square': geometry}
    arr = jsonify(arr)
    return arr

    # https://apis.mapmyindia.com/advancedmaps/v1/ejls5j1jcdu6z9w1pabuytir9wwituo8/distance_matrix_predictive/driving/77.5998448,12.5090914;77.5800417,12.5092973?dep_time=1531543500


    # str = "https://atlas.mapmyindia.com/api/places/textsearch/json?query={} phase 3&region=ind".format(source)
    # response_source = requests.get(str)
    # str = "https://atlas.mapmyindia.com/api/places/textsearch/json?query={} phase 3&region=ind".format(destination)
    # response_destination = requests.get(str)

    # source_longitude = response_source['suggestedLocations'][0]['longitude']
    # source_latitude = response_source['suggestedLocations'][0]['latitude']
    # destination_longitutde = response_destination['suggestedLocations'][0]['longitude']
    # destination_latitude = response_destination['suggestedLocations'][0]['latitude']
    #
    # print(source)
    # print(destination)
    #
    # str = "https://apis.mapmyindia.com/advancedmaps/v1/ejls5j1jcdu6z9w1pabuytir9wwituo8/route_adv/driving/77.131123,28.552413;77.113091,28.544649?steps=false&rtype=1"
    # response = requests.get(str)



if __name__ == '__main__':
    app.run(debug=True)