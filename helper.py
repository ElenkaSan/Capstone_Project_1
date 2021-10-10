from flask import session
from models import db, User, Recipe, Favorite
import os

CURR_USER_KEY = "user_id"

def do_logout():
    """Logout user."""
    if CURR_USER_KEY in session:
      session.pop(CURR_USER_KEY)

diets = ['lacto vegetarian', 'ovo vegetarian', 'pescetarian', 'vegan', 'vegetarian']

cuisines = ['american', 'asian', 'african', 'british', 'cajun', 'chinese', 'caribbean', 
            'eastern european', 'french', 'greek', 'german',  'indian', 'irish', 
            'italian', 'japanese', 'jewish', 'korean', 'latin american', 'mexican', 
            'mediterranean', 'middle eastern', 'native american', 'nordic', 'spanish', 
            'southern', 'thai', 'vietnamese']


def add_recipe_from_api_response(recipe):
    """Add recipe to likes tables in the DB"""
    id = recipe.get('id', None)
    title = recipe.get('title', None)
    image = recipe.get('image', None)
    readyInMinutes = recipe.get('readyInMinutes', None)
    servings = recipe.get('servings', None)
    sourceName = recipe.get('sourceName', None)
    sourceUrl = recipe.get('sourceUrl', None)
    
    favorite = Recipe(id=id, title=title, image=image, readyInMinutes=readyInMinutes, sourceName=sourceName, sourceUrl=sourceUrl, servings=servings)
    try:
        db.session.add(favorite)
        db.session.commit()

    except Exception:
        db.session.rollback()
        print("Exception", str(Exception))
        return "Sorry, Error, Please try again later", str(Exception)
    return favorite


