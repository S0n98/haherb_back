from app import app, db
from app.model import Bioactivity, Herb, Substance
from flask import jsonify, request, json, url_for, abort
from app.errors import bad_request

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return "<p>test API</p>"

@app.route('/api/substance/<int:id>', methods=['GET'])
def get_substance(id):
    return jsonify(Substance.query.get_or_404(id).to_dict())

@app.route('/api/herb/<int:id>', methods=['GET'])
def get_herb(id):
    return json.dumps(Herb.query.get_or_404(id).to_dict(), ensure_ascii=False)

@app.route('/api/bioactivity/<int:id>', methods=['GET'])
def get_bioactivity(id):
    return jsonify(Bioactivity.query.get_or_404(id).to_dict())

@app.route('/api/herbs', methods=['GET'])
def get_herbs():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type(int)), 100)
    data = Herb.to_collection_dict(Herb.query, page, per_page, 'get_herbs')
    return json.dumps(data, ensure_ascii=False)

@app.route('/api/bioactivities', methods=['GET'])
def get_bioactivites():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type(int)), 100)
    data = Bioactivity.to_collection_dict(Bioactivity.query,
        page, per_page, 'get_bioactivities')
    return jsonify(data)

@app.route('/api/substances', methods=['GET'])
def get_substances():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type(int)), 100)
    data = Substance.to_collection_dict(Substance.query,
        page, per_page, 'get_substances')
    return jsonify(data)

@app.route('/api/substance/<int:id>/bioactivities', methods=['GET'])
def get_bioactivities_by_substance(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type(int)), 100)
    data = Substance.get_bioactivities_data_for_jsonify(id, page, per_page)
    return jsonify(data)

@app.route('/api/bioactivity/<int:id>/substances', methods=['GET'])
def get_substances_by_bioactivity(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type(int)), 100)
    data = Bioactivity.get_substances_data_for_jsonify(id, page, per_page)
    return jsonify(data)

@app.route('/api/substance/<int:id>/herbs', methods=['GET'])
def get_herbs_by_substance(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type(int)), 100)
    data = Substance.get_herbs_data_for_jsonify(id, page, per_page)
    return json.dumps(data, ensure_ascii=False)

@app.route('/api/bioactivity', methods=['POST'])
def create_bioactivity():
    data = request.get_json() or {}
    if 'cell_line' not in data or 'compound' not in data\
        or 'ic50' not in data or 'note' not in data:
        return bad_request('must fill full all the field')
    bio = Bioactivity()
    bio.from_dict(data)
    db.session.add(bio)
    db.session.commit()
    response = jsonify(bio.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('get_bioactivity', id=bio.id)
    return response

@app.route('/api/herb', methods=['POST'])
def create_herb():
    data = request.get_json() or {}
    if 'science_name' not in data or 'vietnamese_name' not in data\
        or 'familia' not in data or 'genus' not in data\
        or 'plant_image_path' not in data:
        return bad_request('must fill full all the field')
    herb = Herb()
    herb.from_dict(data)
    db.session.add(herb)
    db.session.commit()
    response = json.dumps(herb.to_dict(), ensure_ascii=False)()
    response.status_code = 201
    response.headers['Location'] = url_for('get_herb', id=herb.id)
    return response

@app.route('/api/substance', methods=['POST'])
def create_substance():
    data = request.get_json() or {}
    if 'structure_path' not in data or 'brutto_formula' not in data\
        or 'mocecular_weight' not in data or 'trivial_name' not in data\
        or 'specie' not in data or 'synonyms' not in data\
        or 'part_of_plant' not in data or 'cas_no' not in data\
        or 'toxicity_ld50' not in data or 'ddsage' not in data\
        or 'systematic_name' not in data:
        return bad_request('must fill full all the field')
    substance = Substance()
    substance.from_dict(data)
    db.session.add(substance)
    db.session.commit()
    response = jsonify(substance.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('get_substance', id=substance.id)
    return response

@app.route('/api/substance/<int:substance_id>', methods=['PUT'])
def update_substance(substance_id):
    substance = Substance.query.get(substance_id)
    if substance == None:
        abort(404)
    if not request.json:
        abort(404)
    for field in ['id', 'structure_path', 'brutto_formula', \
        'mocecular_weight', 'specie', 'synonyms', 'part_of_plant', \
        'cas_no', 'toxicity_ld50', 'ddsage', 'systematic_name', \
        'detail', 'trivial_name']:
        if field in request.json and not isinstance(request.json[field], type(u"")):
            abort(404)
    for field in ['id', 'structure_path', 'brutto_formula', \
        'mocecular_weight', 'specie', 'synonyms', 'part_of_plant', \
        'cas_no', 'toxicity_ld50', 'ddsage', 'systematic_name', \
        'detail', 'trivial_name']:
        if field in request.json[field]:
            setattr(substance, field, request.json[field])

    db.session.commit()
    return jsonify(substance.to_dict())

@app.route('/api/bioactivity/<int:bioactivity_id>', methods=['PUT'])
def update_bioactivity(bioactivity_id):
    bio = Bioactivity.query.get(bioactivity_id)
    if bio == None:
        abort(404)
    if not request.json:
        abort(404)
    for field in ['id', 'cell_line', 'compound', 'ic50', 'note']:
        if field in request.json and not isinstance(request.json[field], type(u"")):
            abort(404)

    for field in ['id', 'cell_line', 'compound', 'ic50', 'note']:
            if field in request.json:
                setattr(bio, field, request.json[field])
    db.session.commit()
    return jsonify(bio.to_dict())
           
@app.route('/api/herb/<int:herb_id>', methods=['PUT'])
def update_herb(herb_id):
    herb = Herb.query.get(herb_id)
    if herb == None:
        abort(404)
    if not request.json:
        abort(404)
    for field in ['id', 'science_name', 'vietnamese_name', 'familia',\
        'genus', 'plant_iamge_path']:
        if field in request.json and not isinstance(request.json[field], type(u"")):
            abort(404)

    for field in ['id', 'science_name', 'vietnamese_name', 'familia',\
        'genus', 'plant_iamge_path']:
        if field in data:
            setattr(herb, field, request.json[field])
    
    db.session.commit()
    return json.dumps(bio.to_dict(), ensure_ascii=False)

@app.route('/api/substance/<int:substance_id>', methods=['DELETE'])
def delete_substance(substance_id):
    sub = Substance.query.get(substance_id)
    if sub == None:
        abort(404)
    db.session.delete(sub)
    db.session.commit()
    return jsonify({'result': True})

@app.route('/api/bioactivity/<int:bioactivity_id>', methods=['DELETE'])
def delete_bioactivity(bioactivity_id):
    bio = Bioactivity.query.get(bioactivity_id)
    if bio == None:
        abort(404)
    db.session.delete(bio)
    db.session.commit()
    return jsonify({'result': True})

@app.route('/api/herb/<int:herb_id>', methods=['DELETE'])
def delete_herb(substance_id):
    herb = herb.query.get(herb_id)
    if herb == None:
        abort(404)
    db.session.delete(herb)
    db.session.commit()
    return jsonify({'result': True})
