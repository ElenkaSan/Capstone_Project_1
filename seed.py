"""Seed file create tables for deployment"""

from models import db, connect_db, User, Recipe, Favorite
from forms import UserForm, LoginForm, UserEditForm
import os

# Create all tables
db.drop_all()
db.create_all()