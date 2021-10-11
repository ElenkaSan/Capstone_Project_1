"""Seed file create tables for deployment"""

from models import db
import os

# Create all tables
db.drop_all()
db.create_all()