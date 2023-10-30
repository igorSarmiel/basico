from flask import Blueprint, render_template, request, redirect, flash
from . import db
from .models import Usuarios


questoes = Blueprint("questoes", __name__, url_prefix='/questoes')