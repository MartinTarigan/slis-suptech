from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime

from slis.db import SessionLocal
from slis.services.sanctions import import_sanction_file

sanctions_bp = Blueprint("sanctions", __name__)


@sanctions_bp.route("/import", methods=["POST"])
def import_sanction():
    
    source_code = request.form.get("source_code")
    if not source_code:
        return jsonify({"error": "source_code is required"}), 400

    if "file" not in request.files:
        return jsonify({"error": "file is required"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "empty filename"}), 400

    filename = secure_filename(file.filename)
    version_label = request.form.get("version_label") or filename
    effective_date_str = request.form.get("effective_date")

    effective_date = None
    if effective_date_str:
        try:
            effective_date = datetime.strptime(effective_date_str, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "invalid effective_date format, use YYYY-MM-DD"}), 400

    db = SessionLocal()
    try:
        snapshot, _ = import_sanction_file(
            db=db,
            source_code=source_code,
            file_obj=file,
            filename=filename,
            version_label=version_label,
            effective_date=effective_date,
        )

        return jsonify(
            {
                "snapshot_id": snapshot.id,
                "source_code": source_code,
                "version_label": snapshot.version_label,
                "record_count": snapshot.record_count,
                "raw_file_name": snapshot.raw_file_name,
            }
        )

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()
