from datetime import datetime, timedelta
import os

from flask import Blueprint, redirect, render_template, send_from_directory

index_bp = Blueprint("index_bp", __name__)


@index_bp.route("/", methods=["GET"])
def get():
    return render_template("index.html"), 200
