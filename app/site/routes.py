from flask import Blueprint, render_template, request, jsonify
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json


site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')


@site.route('/search', methods = ["GET", "POST"])
def search():
    #TRYING TO IMPLEMENT IN JS

    url = "https://api.spoonacular.com/food/menuItems/search?"
    #Grabbing the input from the HTML form
    item = request.form.get('inputsearch')
    print(f"A user searched for: {item}")

    parameters = {
        'query' :{item},
        'number' : 3,
        'apiKey' : '07607f40a346438790c194f4913ce4a3'
    }

    headers = {
        'Content-Type' : 'application/json'
    }
    session = Session()
    session.headers.update(headers)

    #trying to make the dictionary a global variable
   
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)

        global dict
        dict={}
        if 'dict' in globals():
            dict[item]= {
                'title': data["menuItems"][0]["title"],
                'image': data["menuItems"][0]["image"],
                'restaurant': data["menuItems"][0]["restaurantChain"],
                'id': data["menuItems"][0]["id"]
            }
        print(dict)
        # return dict[item]
        
    except (ConnectionError, Timeout, TooManyRedirects) as error:
        print(error)

    return render_template('search.html')


test = 'hello'