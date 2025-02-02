from flask import render_template, request, jsonify, g
from flask_cas import login_required
from app import app, db, cas
from app.models import User

import datetime
import time
import yalies

yalies_api = yalies.API(app.config['YALIES_API_KEY'])

@app.before_request
def store_user():
    if request.method != 'OPTIONS':
        if cas.id:
            g.user = User.query.get(cas.id)
            timestamp = int(time.time())
            if not g.user:
                g.user = User(username=cas.username,
                              registered_on=timestamp)
                db.session.add(g.user)
            g.user.last_seen = timestamp
            db.session.commit()
            print('NetID: ' + cas.username)


@app.route('/')
def index():
    if not cas.username:
        return render_template('splash.html')
    options = yalies_api.filters()
    filters = {
        'Students': {
            'school': {
                'header': 'School',
            },
            'year': {
                'header': 'Year',
            },
        },
        'Undergraduate': {
            'college': {
                'header': 'College',
            },
            'major': 'Major',
            'leave': {
                'header': 'Took Leave?',
                'default': 'N/A'
            },
            'eli_whitney': {
                'header': 'Eli Whitney?',
                'default': 'N/A'
            },
            #'building_code': 'Building',
            #'entryway': 'Entryway',
            #'floor': 'Floor',
            #'suite': 'Suite',
            #'room': 'Room',
        },
        'Graduate': {
            'curriculum': {
                'Curriculum',
            },
        },
        'Staff': {
            'organization': {
                'header': 'Organization',
            },
            'unit': {
                'header': 'Organization Unit',
            },
            'office_building': {
                'header': 'Office Building',
            },
        },
    }
    return render_template('index.html', options=options, filters=filters)


@app.route('/query', methods=['POST'])
@login_required
def query():
    filters = request.get_json()
    people = yalies_api.people(filters=filters)
    return jsonify([person.email for person in people if person.email])
