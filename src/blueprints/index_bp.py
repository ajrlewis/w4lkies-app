from datetime import datetime, timedelta
import os

from flask import Blueprint, redirect, render_template, send_from_directory
from flask_login import login_required, current_user

index_bp = Blueprint("index_bp", __name__)


@index_bp.route("/", methods=["GET"])
@login_required
def get():
    return render_template("index.html"), 200
