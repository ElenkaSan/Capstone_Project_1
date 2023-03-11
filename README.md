# Recipe Tips
### *Try the app [Recipe Tips](https://recipe-tips.onrender.com/)* I did small updates :) Enjoy!

The website `Recipe Tips` is designed for people who would like to know what they can cook 
from what "in the fridge left" / any food left, can see milkshakes, yogurts. Users can also see random search and allows to search food by name, 
or make complex search for recipes using natural language queries,
such as “gluten free brownies without sugar” or “low fat vegan cupcakes” or
write detailed information such as vegan, vegetarian, pescetarian, gluten free, grain free,
dairy free, high protein, low sodium, low carb etc.
  
That can help to create special diets/dietary requirements for users. 
Good for mothers and fathers who would like to create healthy recipe lists for their kids. 
Can print recipes. 

And after creating an account able to make a list of favorite recipes for every day or for every week etc. 
Even warm up with some food jokes and repeat exercises from random pictures like stay in touch with sport.


### Data
For this CP database that takes food-related information from the [Spooncular database](https://spoonacular.com/food-api)

`DB schema:`
  - user table
  - recipe table
  - favorite recipe table

### Local Environment
To get the code on your local machine, create a PostgreSQL database, and set up a virtual environment in Python, and get an API key from Data API.
```sh
> git clone https://github.com/ElenkaSan/Capstone_Project_1.git
> python3 -m venv venv
> pip3 install -r requirements.txt
> source venv/bin/activate
```
Sign up [here](https://spoonacular.com/food-api) to use the Data API.
  Save your API key in a file called dotenv using this format:
```sh
API_KEY="YOURKEYHERE"
```
Create database 'recipeTips' in the Terminal:

1)
```sh
$ createdb recipeTips
```
2)
```sh
$ ipython
In [1]: run seed.py
In [2]: db.create_all()
In [1]: quit()
```
Run the app:
```sh
$ flask run
```
You can now navigate to `http://127.0.0.1:5000/` to start exploring Recipe Tips.

<img width="1440" alt="Screen Shot 2022-06-04 at 11 08 28 PM" src="https://user-images.githubusercontent.com/75818489/172033707-8df5b309-a733-4a40-98ac-1d21e6728a69.png">

<img width="1440" alt="Screen Shot 2022-06-04 at 11 12 44 PM" src="https://user-images.githubusercontent.com/75818489/172033712-2f8a7399-3d11-48e0-89d8-e7b9cf8dbd00.png">

<img width="1274" alt="Screen Shot 2022-08-05 at 4 31 36 PM" src="https://user-images.githubusercontent.com/75818489/183158310-4f9e66f6-232b-4b20-9a31-fc02dab4a066.png">

<img width="983" alt="Screen Shot 2022-08-05 at 4 35 19 PM" src="https://user-images.githubusercontent.com/75818489/183158749-464e5acd-abd5-40ea-985f-c14e16ae378b.png">

### Future-Features
  - The recipe feature with favorite food:
    - Automatically calculate the nutritional information for any recipe, analyze recipe costs, visualize ingredient lists
    - Compute an entire meal plan
    - Expanding on the recipe search filter (e.g. dietary restrictions, calories, etc.)
  - More functionality exercise info or tips with images and video
  - Create app on the phone

*Stretch goals:*
  - Share favorite recipes lists with other users on the site. Good for family members, that they can add this list to their account.
  
Frontend:
  - HTML templates using Jinja and WTForms for forms
  - Design and interaction using JavaScript, Bootstrap, Font Awesome and raw CSS
  
Backend:
  - Routes and Models using Python3 and Flask
  - SQLAlchemy as a database ORM
  - Database using PostgreSQL
  - AJAX requests using Axios
  -RESTful APIs

Deployment:
  - Deployed on [Render Server](https://render.com/)

Feel free to improve or contribute. Pull requests are always welcome!


Author [Elena Nurullina](https://github.com/ElenkaSan/)
