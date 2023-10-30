from flask import Blueprint, render_template, request, redirect, session, flash
from . import db
from .models import Usuarios


urls = Blueprint("urls", __name__)

@urls.route("/")
def index():
    if "Nome" in session:
        return render_template("index.html")     
    else:
        return render_template("index.html")
    

