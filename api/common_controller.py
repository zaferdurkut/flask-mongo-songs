from flask import jsonify, Blueprint

blueprint_common = Blueprint("/api/common", __name__, url_prefix="/api/common")


@blueprint_common.route("/status", methods=["GET"])
def status():
    return jsonify({"status": True})
