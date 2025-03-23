from datetime import datetime, timedelta
import os
import time

from flask import Blueprint, jsonify, redirect, render_template, send_from_directory
from flask_login import login_required, current_user

from services import database_service


index_bp = Blueprint("index_bp", __name__)


@index_bp.route("/", methods=["GET"])
@login_required
def get():
    return render_template("index.html"), 200  # single page application


@index_bp.route("/ping", methods=["GET"])
def ping_database():
    try:
        database_service.wake_up_database()
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
