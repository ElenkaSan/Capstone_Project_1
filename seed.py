"""Seed file create tables for deployment"""

# from models import User, Recipe, Favorite, db
from app import db
import os

# Create all tables
db.drop_all()
db.create_all()