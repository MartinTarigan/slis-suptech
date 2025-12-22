from flask import Blueprint, render_template_string, jsonify, request
from slis.matching import (
    normalize_name,
    calculate_advanced_name_score,
    parse_dob,
    calculate_dob_score_flexible,
    run_screening_engine,
)
from slis.tasks import run_screening_task
from slis.celery_app import celery_app as celery


main_bp = Blueprint("main", __name__)


@main_bp.route("/health")
def health():
    return jsonify({"status": "ok", "message": "SLIS Flask backend is running"}), 200


@main_bp.route("/")
def index():
    html = """
    <!doctype html>
    <html>
      <head>
        <title>SLIS - Flask Backend</title>
        <meta charset="utf-8">
        <style>
          body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            padding: 40px;
            background: #f5f5f5;
          }
          .card {
            max-width: 640px;
            margin: 0 auto;
            padding: 24px;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
          }
          h1 { margin-top: 0; }
          code {
            background: #f0f0f0;
            padding: 2px 4px;
            border-radius: 4px;
          }
        </style>
      </head>
      <body>
        <div class="card">
          <h1>SLIS Backend (Flask + Celery) 🛡️</h1>
          <p>Ini backend baru untuk <strong>Sanction List Intelligence Screening</strong>.</p>
          <p>Endpoint yang sudah ada:</p>
          <ul>
            <li><code>GET /health</code> — cek status service</li>
            <li><code>GET /</code> — halaman ini</li>
          </ul>
          <p>Celery & Redis sudah terintegrasi, nanti dipakai untuk job screening.</p>
        </div>
      </body>
    </html>
    """
    return render_template_string(html)

@main_bp.route("/api/test-name-match")
def test_name_match():
    """
    Contoh endpoint untuk menguji engine nama.
    Contoh:
    /api/test-name-match?name1=Mohammad+Ali&name2=Muhammad+Ali
    """
    name1 = request.args.get("name1", "")
    name2 = request.args.get("name2", "")

    score = calculate_advanced_name_score(name1, name2)
    return jsonify({
        "name1": name1,
        "name2": name2,
        "normalized_name1": normalize_name(name1),
        "normalized_name2": normalize_name(name2),
        "score": score,
    })


@main_bp.route("/api/test-dob-match")
def test_dob_match():
    """
    Contoh endpoint untuk menguji engine DOB.
    Contoh:
    /api/test-dob-match?cust=20%20Juli%201985&sanction=1985-07-20&source=DTTOT
    /api/test-dob-match?cust=1983-01-01&sanction=1980-1985&source=Australia
    """
    cust = request.args.get("cust", "")
    sanction = request.args.get("sanction", "")
    source = request.args.get("source", "")

    score, desc = calculate_dob_score_flexible(cust, sanction, source)
    return jsonify({
        "customer_dob": cust,
        "sanction_dob": sanction,
        "source_list": source,
        "score": score,
        "description": desc,
        "parsed_customer": parse_dob(cust),
    })

@main_bp.route("/api/screening/test-sync", methods=["POST"])
def screening_test_sync():
    """
    Endpoint uji coba screening (tanpa DB, tanpa Celery).
    Expects JSON:
    {
      "customers": [ {...}, {...} ],
      "sanctions": [ {...}, {...} ],
      "name_threshold": 70,
      "final_score_threshold": 75
    }
    """
    payload = request.get_json(silent=True) or {}
    customers = payload.get("customers", [])
    sanctions = payload.get("sanctions", [])
    name_threshold = float(payload.get("name_threshold", 70))
    final_score_threshold = float(payload.get("final_score_threshold", 75))

    if not customers or not sanctions:
        return jsonify({
            "error": "customers and sanctions must be non-empty lists",
            "received_customers": len(customers),
            "received_sanctions": len(sanctions),
        }), 400

    
    results = run_screening_engine(
        customers=customers,
        sanctions=sanctions,
        name_threshold=name_threshold,
    )

    
    filtered = [
        r for r in results
        if r["Final_Score"] >= final_score_threshold
    ]

    
    filtered.sort(key=lambda x: x["Final_Score"], reverse=True)

    return jsonify({
        "summary": {
            "customers_count": len(customers),
            "sanctions_count": len(sanctions),
            "raw_matches": len(results),
            "filtered_matches": len(filtered),
            "name_threshold": name_threshold,
            "final_score_threshold": final_score_threshold,
        },
        "results": filtered,
    })

@main_bp.route("/api/screening/async", methods=["POST"])
def screening_async():
    """
    Submit screening job secara async (Celery).
    Body JSON sama seperti test-sync:
    {
      "customers": [...],
      "sanctions": [...],
      "name_threshold": 70,
      "final_score_threshold": 75
    }
    """
    payload = request.get_json(silent=True) or {}
    customers = payload.get("customers", [])
    sanctions = payload.get("sanctions", [])
    name_threshold = float(payload.get("name_threshold", 70))
    final_score_threshold = float(payload.get("final_score_threshold", 75))

    if not customers or not sanctions:
        return jsonify({
            "error": "customers and sanctions must be non-empty lists",
            "received_customers": len(customers),
            "received_sanctions": len(sanctions),
        }), 400

    
    task = run_screening_task.delay(
        customers=customers,
        sanctions=sanctions,
        name_threshold=name_threshold,
        final_score_threshold=final_score_threshold,
    )

    return jsonify({
        "job_id": task.id,
        "state": task.state,
    }), 202

@main_bp.route("/api/screening/async/<job_id>", methods=["GET"])
def screening_async_status(job_id):
    """
    Cek status / hasil dari job async.
    """
    async_result = celery.AsyncResult(job_id)

    response = {
        "job_id": job_id,
        "state": async_result.state,   
    }

    if async_result.state == "PENDING":
        
        response["message"] = "Job is waiting to be processed."
    elif async_result.state == "STARTED":
        response["message"] = "Job is currently running."
    elif async_result.state == "SUCCESS":
        
        result = async_result.result or {}
        response["result"] = result
    elif async_result.state == "FAILURE":
        
        response["error"] = str(async_result.info)

    return jsonify(response)


