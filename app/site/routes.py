from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from bs4 import BeautifulSoup
import json
import re
from bs4 import BeautifulSoup
from jinja2 import Environment
from models import User, SavedRecipes, db

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')



@site.route('/profile')
def profile():
    return render_template('profile.html')



@site.route('/search', methods = ["GET", "POST"])
def search():
    url = "https://api.spoonacular.com/recipes/complexSearch?"
    #Grabbing the input from the HTML form
    item = request.form.get('inputsearch')
    print(f"A user searched for: {item}")

    parameters = {
        'query' :{item},
        'number' : 10,
        'apiKey' : '07607f40a346438790c194f4913ce4a3'
    }

    headers = {
        'Content-Type' : 'application/json'
    }
    session = Session()
    session.headers.update(headers)
   
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        print(data['results'])

        for food in data['results']:
            print(food)
            food = {
                'title':food['title'],
                'id': food['id'],
                'image': food['image']
            }
            #Hoping to make this a global variable so I may access this in another function.
            global id
            id = food['id']
            global title
            title = food['title']
            global image
            image = food['image']

    except (ConnectionError, Timeout, TooManyRedirects) as error:
        print(error)

    return render_template('search.html', dict=dict, item=item, data=data, food=food, id=id)



@site.route('/recipe', methods = ["GET", "POST"])
def recipeinfo():
    # global id
    # global id only grabs the last item from the query, not the corresponding so:
    id = request.args.get('id')
    print(f"Recipe ID: {id}")
    #For the summary, but we need the actaul recipe steps
    # url = f'https://api.spoonacular.com/recipes/{id}/summary?'
    url=f'https://api.spoonacular.com/recipes/{id}/information?'

    parameters = {
        'apiKey' : '07607f40a346438790c194f4913ce4a3'
    }

    headers = {
        'Content-Type' : 'application/json'
    }
    session = Session()
    session.headers.update(headers)
    # dont need this anymore
    # print(url)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        # print(response)
        # print(data)

        # create an empty array to store the ingredients
        ingredients = []
        for ingredient in data['extendedIngredients']:
            # access the value of the 'original' field for each ingredient
            original = ingredient['original']
            ingredients.append(original)
            print(original)
        # ITS SOUP TIME
        # Cleaning data'instructions' since the response includes html tags that I do not want
        soup = BeautifulSoup(data['instructions'], 'html.parser')
        # extract the instructions text from the parsed data
        instructions = soup.get_text()
        newinstructions = instructions.replace(re.escape('.'), '.\n')

        recipeitems={}
        recipeitems={
            'title': data['title'],
            'preptime': data['preparationMinutes'],
            'cooktime':data['cookingMinutes'],
            'servings':data['servings'],
            'image':data['image'],
            'instructions': newinstructions
        }
        print(recipeitems)

    except (ConnectionError, Timeout, TooManyRedirects) as error:
        print(error)

    return render_template('recipe.html', recipeitems=recipeitems, ingredients=ingredients)



@site.route('/recipe/save', methods=["GET", "POST"])
@login_required
def save_recipe():
    pass
    # #import global variables of title and id into this function
    # global id
    # global title
    # global image

    # if request.method == "POST":
    #     # Insert the record into the recipebook table
    #     recipe = SavedRecipes(title=title, img_url=image, user_id=current_user.id)
    #     db.session.add(recipe)
    #     db.session.commit()
    #     return jsonify({'message': 'Recipe added successfully'})
    # else:
    #     # The user_id does not exist in the user table
    #     return jsonify({'message': 'Error: user_id does not exist in the user table'})
