from flask import Blueprint, jsonify, request
from slis.db import SessionLocal
from sqlalchemy.orm import scoped_session

db_session = scoped_session(SessionLocal)

from slis.models import GeoRiskCategory, GeoRiskCountry
# Import engine supaya bisa kita refresh cachenya setelah update data
from slis.matching.geo import geo_engine 

geo_bp = Blueprint('geo', __name__, url_prefix='/api/geo')

# --- 1. KATEGORI RISIKO (Misal: "Sanctioned", "Tax Haven") ---

@geo_bp.teardown_request
def remove_session(ex=None):
    db_session.remove()

@geo_bp.route('/categories', methods=['GET'])
def get_categories():
    cats = db_session.query(GeoRiskCategory).all()
    return jsonify([{
        'id': c.id, 'name': c.name, 
        'risk_score': c.risk_score, 
        'count': len(c.countries)
    } for c in cats])

@geo_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.json
    try:
        new_cat = GeoRiskCategory(
            name=data['name'], 
            risk_score=data.get('risk_score', 1.0),
            description=data.get('description', '')
        )
        db_session.add(new_cat)
        db_session.commit()
        return jsonify({'message': 'Category created', 'id': new_cat.id})
    except Exception as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 400

# --- 2. MAPPING NEGARA (Misal: Masukkan "KP" ke "Sanctioned") ---

@geo_bp.route('/countries', methods=['GET'])
def get_countries():
    mapped = db_session.query(GeoRiskCountry).all()
    return jsonify([{
        'id': c.id, 
        'code': c.country_code, 
        'name': c.country_name,
        'category': c.category.name if c.category else 'Uncategorized'
    } for c in mapped])

@geo_bp.route('/countries', methods=['POST'])
def add_country_risk():
    data = request.json
    try:
        # Cek duplikasi (Opsional, biar data bersih)
        exists = db_session.query(GeoRiskCountry).filter_by(country_code=data['code'].upper()).first()
        if exists:
            # Update existing atau reject? Di sini kita reject/timpa saja
            db_session.delete(exists)
            db_session.flush()

        new_c = GeoRiskCountry(
            category_id=data['category_id'],
            country_code=data['code'].upper(),
            country_name=data.get('name', '')
        )
        db_session.add(new_c)
        db_session.commit()
        
        # PENTING: Refresh cache di engine biar data baru langsung efek
        geo_engine.reload_risks()
        
        return jsonify({'message': 'Country mapped successfully'})
    except Exception as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500

@geo_bp.route('/countries/<int:id>', methods=['DELETE'])
def remove_country_risk(id):
    try:
        item = db_session.query(GeoRiskCountry).get(id)
        if item:
            db_session.delete(item)
            db_session.commit()
            geo_engine.reload_risks() # Refresh cache
            return jsonify({'message': 'Deleted'})
        return jsonify({'error': 'Not found'}), 404
    except Exception as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500