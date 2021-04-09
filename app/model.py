import os
import jwt
import base64
import random
from app import db
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datatime, timedelta
class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }

        return data

substances = db.Table('herb_substances',
    db.Column('herb_id', db.Integer, db.ForeignKey('herb.id'), \
        primary_key=True),
    db.Column('substances_id', db.Integer, db.ForeignKey('substance.id'), \
        primary_key=True)
)

bioactivities = db.Table('substances_bioactivity',
    db.Column('substances_id', db.Integer, db.ForeignKey('substance.id'), \
        primary_key=True),
    db.Column('bioactivity_id', db.Integer, db.ForeignKey('bioactivity.id')\
        , primary_key=True)
)

class Bioactivity(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cell_line = db.Column(db.String(50))
    compound = db.Column(db.String(50))
    ic50 = db.Column(db.String(50))
    note = db.Column(db.String(200))

    def to_dict(self):
        data = {
            'id': self.id,
            'cell_line': self.cell_line,
            'compound': self.compound,
            'ic50': self.ic50,
            'note': self.note,
            '_link': {
                'self': url_for('get_bioactivity', id=self.id),
                'substances': url_for('get_substances_by_bioactivity',
                    id=self.id)
            }
        }

        return data

    def from_dict(self, data):
        for field in ['id', 'cell_line', 'compound', 'ic50', 'note']:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return '<bioactivity {}>'.format(self.id)

    @staticmethod
    def get_substances_data_for_jsonify(id, page, per_page):
        data = Substance.to_collection_dict(Substance.query.join(
            bioactivities, 
            (Substance.id == bioactivities.c.substances_id))
            .filter(id == bioactivities.c.bioactivity_id)
        , page, per_page, 'get_bioactivities_by_substance', id=id)
        return data

class Substance(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    structure_path = db.Column(db.String(200))
    brutto_formula = db.Column(db.String(50))
    mocecular_weight = db.Column(db.String(50))
    trivial_name = db.Column(db.String(50))
    specie = db.Column(db.String(50))
    synonyms = db.Column(db.String(50))
    part_of_plant = db.Column(db.String(50))
    cas_no = db.Column(db.String(50))
    toxicity_ld50 = db.Column(db.String(50))
    ddsage = db.Column(db.String(50))
    systematic_name = db.Column(db.String(50))
    detail = db.Column(db.String(200))
    bioactivities = db.relationship('Bioactivity', secondary=bioactivities,
        backref=db.backref('substances', lazy='subquery'), lazy='subquery')

    def to_dict(self):
        data = {
            'id': self.id,
            'structure_path': self.structure_path,
            'brutto_formula': self.brutto_formula,
            'mocecular_weight': self.mocecular_weight,
            'trivial_name': self.trivial_name,
            'specie': self.specie,
            'synonyms': self.synonyms,
            'part_of_plant': self.part_of_plant,
            'cas_no': self.cas_no,
            'toxicity_ld50': self.toxicity_ld50,
            'ddsage': self.ddsage,
            'systematic_name': self.systematic_name,
            'detail': self.detail,
            '_link': {
                'self': url_for('get_substance', id=self.id),
                'herbs': url_for('get_herbs_by_substance', id=self.id),
                'bioactivities': url_for('get_bioactivities_by_substance',
                    id=self.id)
            }
        }

        return data

    def from_dict(self, data):
        for field in ['id', 'structure_path', 'brutto_formula', \
            'mocecular_weight', 'specie', 'synonyms', 'part_of_plant', \
            'cas_no', 'toxicity_ld50', 'ddsage', 'systematic_name', \
            'detail', 'trivial_name']:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        return '<substances {}>'.format(self.id)

    @staticmethod
    def get_bioactivities_data_for_jsonify(id, page, per_page):
        data = Bioactivity.to_collection_dict(Bioactivity.query.join(
            bioactivities, 
            (Bioactivity.id == bioactivities.c.bioactivity_id))
            .filter(id == bioactivities.c.substances_id)
        , page, per_page, 'get_bioactivities_by_substance', id=id)
        return data

    def get_herbs_data_for_jsonify(id, page, per_page):
        data = Bioactivity.to_collection_dict(Bioactivity.query.join(
            substances, 
            (Bioactivity.id == substances.c.herb_id))
            .filter(id == substances.c.substances_id)
        , page, per_page, 'get_bioactivities_by_substance', id=id)
        return data

class Herb(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    science_name = db.Column(db.String(50))
    vietnamese_name = db.Column(db.String(50))
    familia = db.Column(db.String(50))
    genus = db.Column(db.String(50))
    plant_image_path = db.Column(db.String(100))
    substances = db.relationship('Substance', secondary=substances,
        backref=db.backref('herbs', lazy='subquery'), lazy='subquery')

    def to_dict(self):
        data = {
            'id': self.id,
            'science_name': self.science_name,
            'vietnamese_name': self.vietnamese_name,
            'familia': self.familia,
            'genus': self.genus,
            'plant_image_path': self.plant_image_path,
            '_link': {
                'self': url_for('get_herb', id=self.id)
            },
        }
        
        return data

    def from_dict(self, data):
        for filed in ['id', 'science_name', 'vietnamese_name', 'familia',\
            'genus', 'plant_iamge_path']:
            if filed in data:
                setattr(self, filed, data[filed])

    def __repr__(self):
        return '<herb {}>'.format(self.id)

class Admin(PaginatedAPIMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return 'Admin {}'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_token(self, expires_in=3600):
        """

        
        """
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        
        token_payload = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token = jwt.encode(
            {'token_payload': f'{token_payload}'},
            app.config['SECRET_KEY'], algorithm='HS256'
        )

        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datatime.utcnow() - timedelta(seconds=1)
    
    def email_suppport_token(self, expires_in=600):
        """
        Add zero padded id with a list of numbers
        Encode new numbers to token
        """
        ambiguous_numbers = config.['AMBIGUOUS_NUMBERS'] 
        paddied_admin_id = [chr(int(x) + y) for x, y in zip(f'{self.id:03}.', ambiguous_numbers)]
        admin_id_ascii = ''.join(paddied_admin_id).encode('ascii')
        admin_id_base64 = base64.b64encode(admin_id_ascii).decode('utf-8')
        token_payload1 = base64.b64encode(os.urandom(6)).decode('utf-8')
        token_payload2 = base64.b64encode(os.urandom(9)).decode('utf-8')

        return = jwt.encode(
            {'token_payload': f'{token_payload1}{admin_id_base64}{token_payload2}',
            'id': random.randint(1, 999), 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def check_token(token):
        admin = Admin.query.filter_by(token=token).first()
        if user in None or user.token_expiration < datetime.utcnow():
            return None
        return admin

    @staticmethod   
    def verify_email_support_token(token):
        try:
            encoded_id = jwt.decode(token, app.config['SECRET_KEY'],
                algorithms=['HS256'])['token_payload'][8:12]

            encoded_id = base64.b64decode(encoded_id.encode('utf-8'))
            id = 0
            i = 100
            for x, y in zip(encoded_id, app.config['AMBIGUOUS_NUMBERS']):
                i /= 10
                id += (x - y) * i
        except:
            return            
        return User.query.get(id)