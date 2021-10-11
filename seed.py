"""Seed file create tables for deployment"""
import os
from models import User, Recipe, Favorite, db
from app import app

# Create all tables
db.drop_all()
db.create_all()