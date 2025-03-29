from datetime import datetime, timedelta
import json
import os
import time

from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    Response,
    send_from_directory,
)
from flask_login import login_required, current_user

from app import csrf
from services.auth_service import admin_user_required
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


@index_bp.route("/database/dump", methods=["GET"])
@login_required
@admin_user_required
def dump_database():
    try:
        database = database_service.dump_database()
        filename = f"w4lkies_app ({datetime.now()}).json"
        return Response(
            database,
            mimetype="application/json",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@index_bp.route("/database/load", methods=["POST"])
# @login_required
# @admin_user_required
@csrf.exempt
def load_database():
    try:
        # Check if the post request has the file part
        if "file" not in request.files:
            return jsonify({"status": "error", "message": "No file part"}), 400
        file = request.files["file"]
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == "":
            return jsonify({"status": "error", "message": "No selected file"}), 400
        if file:
            # Read the file
            data = json.load(file)
            table_data = data
            database_service.load_database(table_data)
            return jsonify({"status": "ok"}), 200
        else:
            return (
                jsonify({"status": "error", "message": "No file uploaded are allowed"}),
                400,
            )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
