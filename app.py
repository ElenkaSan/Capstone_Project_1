import os
from flask import Flask, render_template, redirect, request, g, url_for, flash, session, jsonify, make_response, abort
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Recipe, Favorite
from forms import UserForm, LoginForm, UserEditForm
from sqlalchemy.exc import IntegrityError
from helper import diets, cuisines, do_logout, add_recipe_from_api_response
import requests
API_KEY = os.getenv("API_KEY")

CURR_USER_KEY = "user_id"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgres:///recipeTips')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1) or 'postgresql:///recipeTips'
# app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'is a secret')
app.config['SECRET_KEY'] = os.environ.get('API_KEY', 'is a secret')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

BASE_URL = "https://api.spoonacular.com/"

connect_db(app)
# --------------------------- User signup/login/logout 
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

    g.diets = [diet for diet in diets]
    g.cuisines = [cuisine for cuisine in cuisines]

def do_login(user):
    """Log in user."""
    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form.
    """

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

    form = UserForm()
    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                notes=form.notes.data)
            db.session.commit()
         
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)
        flash("Thank you! You successful created account.", 'success')
        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login."""
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid username/password.", 'danger')
    return render_template('users/login.html', form=form)


@app.route("/logout")
def logout():
    """Handle logout of user."""

    do_logout()
    flash("You have been logged out. Bye!", 'success')
    return redirect("/")


@app.route("/users/<int:user_id>")
def users_show(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)
    return render_template('users/show.html', user=user)

@app.route("/users/<int:user_id>/update", methods=["GET", "POST"])
def update_profile(user_id):
    """Update profile for current user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get(user_id)
    form = UserEditForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.notes = form.notes.data
        db.session.commit()
        flash(f"You made your account update!", 'success')
        return redirect(f"/users/{user.id}")

    return render_template('users/edit.html', form=form, user_id=user.id)

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()
    session.pop(CURR_USER_KEY)
    flash(f"{g.user.username}'s account has been deleted!", 'secondary')
    return redirect('/')

#--------------------------------------------------------------------

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/execise")
def ex():
    """show ex pics"""
    return render_template("execise.html")

@app.route("/joke")
def jokepage():
    joke_response = requests.get(f"{BASE_URL}/food/jokes/random", params={ "apiKey": API_KEY })
    data = joke_response.json()
    jo = str((data)['text'])
    if len(jo) == 0:
        flash("Sorry, search limit reached!", "warning")
        return render_template("index.html")
    return render_template('joke.html', joke=jo)

@app.route("/foody") 
def leftfood_recipes():
    """This is a "what's in your fridge" API endpoint.
    Show search like Greek yogurt or apples,flour,sugar"""
    if (str(request.args['ingridients']).strip() != ""):
        response = requests.get(f"{BASE_URL}/recipes/findByIngredients", params={ "apiKey": API_KEY, "number": 12,"ranking": 1 ,"ignorePantry": False, "ingredients":request.args['ingridients'] })
        data = response.json()
    if len(data) == 0:
        flash("Sorry, you have a typo or search limit reached!", "warning")
        return render_template("index.html")

    if g.user:
        recipe_ids = [r.id for r in g.user.recipes]
    else:
        recipe_ids = []
    favorites = [f['id'] for f in data if f['id'] in recipe_ids]
    return render_template('/foods/foody.html', recipes=data, recipe_ids=recipe_ids, favorites=favorites)

@app.route("/random")
def show_recipes():
    """Show random recipes auto populated"""
    res = requests.get(f"{BASE_URL}/recipes/random", params={ "apiKey": API_KEY, "number": 8 })
    data = res.json()
   
    if data.get('recipes') == 0:
        flash("Sorry, search limit reached!", "warning")
        return render_template("index.html")
    recipes = data['recipes']

    if g.user:
        recipe_ids = [r.id for r in g.user.recipes]
    else:
        recipe_ids = []
    favorites = [f['id'] for f in recipes if f['id'] in recipe_ids]
    return render_template("/foods/random.html", recipes=recipes, recipe_ids=recipe_ids, favorites=favorites)


@app.route("/search")
def search_recipe():
    """Inside random recipes show refine search by diets and cuisines"""
    query = request.args.get('query', "")
    cuisine = request.args.get('cuisine', "")
    diet = request.args.get('diet', "")
    offset = request.args.get('offset')
    number = 8
    if request.args:
        res = requests.get(f"{BASE_URL}/recipes/complexSearch", params={ "apiKey": API_KEY, "diet": diet, "cuisine": cuisine, "query": query, "number": number, "offset": offset })
        data = res.json()
   
    if data.get('result') == 0:
        flash("Sorry, search limit reached!", "warning")
        render_template("/foods/random.html")
    
    path = f"/search?query={query}&cuisine={cuisine}&diet={diet}"
    recipes = data['results']
    if g.user:
        recipe_ids = [r.id for r in g.user.recipes]
    else:
        recipe_ids = []
    favorites = [f['id'] for f in recipes if f['id'] in recipe_ids]
    return render_template("/foods/recipes.html", recipes=recipes, recipe_ids=recipe_ids, favorites=favorites, url=path, offset=offset)

@app.route("/find")
def search():
    """Show recipes in navbar search, where user can write detailed information for search
    such as vegan, pescetarian, grain free, dairy free, high protein, low sodium, low carb etc. 
    In the future inside 'complexSearch' will be refine search by diets and cuisines"""
    query = request.args.get('query', "")
    offset = request.args.get('offset')
    number = 9
    cuisine = request.args.get('cuisine', "")
    diet = request.args.get('diet', "")
    if request.args:
        res = requests.get(f"{BASE_URL}/recipes/complexSearch", params={ "apiKey": API_KEY, "query": query, "number": number, "offset": offset, "diet": diet, "cuisine": cuisine })
        data = res.json()
    if data.get('result') == 0:
        flash("Sorry, search limit reached!", "warning")
        render_template("/foods/random.html")
    
    path = f"/find?query={query}&cuisine={cuisine}&diet={diet}"
    recipes = data['results']

    if g.user:
        recipe_ids = [r.id for r in g.user.recipes]
    else:
        recipe_ids = []

    favorites = [f['id'] for f in recipes if f['id'] in recipe_ids]
    return render_template("/foods/search.html", recipes=recipes, favorites=favorites, recipe_ids=recipe_ids,  offset=offset, url=path)



@app.route("/recipes/<int:id>")
def show_recipe(id):
    res = requests.get(f"{BASE_URL}/recipes/{id}/information", params={ "apiKey": API_KEY, "includeNutrition": False })
    data = res.json()
    return render_template("foods/details.html", recipes=data)

# ----------------------------------------

@app.route("/favorites")
def show_favorites():
    if not g.user:
        flash("You must be logged in to view favorites", "danger")
        return redirect("/login")
    
    user_res = g.user.recipes
    recipe_ids = [r.id for r in user_res]

    return render_template("foods/favorites.html", recipe_ids=recipe_ids)



@app.route("/api/favorite/<int:id>", methods=["POST"])
def aad_favorite(id):
    """Add to favorites"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    recipe = Recipe.query.filter_by(id=id).first()
    if not recipe:
        res = requests.get(f"{BASE_URL}/recipes/{id}/information", params={ "apiKey": API_KEY, "includeNutrition": False })
        data = res.json()
        recipe = add_recipe_from_api_response(data)

        g.user.recipes.append(recipe)
        db.session.commit()
    else:
        g.user.recipes.append(recipe)
        db.session.commit()
        
    # flash("You add recipe to favorite!", "sucsess")
    return jsonify(recipe=recipe.serialize())

  
@ app.route("/api/favorite/<int:id>", methods=['DELETE'])
def remove_favorite(id):
    """ Unfavorite a recipe """
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    favorite = Favorite.query.filter_by(user_id=g.user.id,recipe_id=id).first()

    try:
       db.session.delete(favorite)
       db.session.commit()

    except Exception as e:
        print("RECIPE ERROR", e)
        return jsonify(errors=str(e))
    
    # flash("Recipe removed from favorites", "danger")
    return {"outcome":"success"}


@app.errorhandler(404)
def error_page(error):
    """Show 404 ERROR page if page NOT FOUND"""
    return render_template("error.html"), 404


@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers["Cache-Control"] = "public, max-age=0"
    return req


if __name__ == '__main__':
  app.run()
