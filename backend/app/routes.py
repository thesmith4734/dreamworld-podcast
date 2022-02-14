from flask.helpers import send_file, send_from_directory
from itsdangerous import json
from app import app, db
import os
from flask import jsonify, request
from flask_marshmallow import Marshmallow
from app.models import Podcast, PodcastSchema
from app.audio import getAudioFile

### Test Config access
@app.route('/testconfig')
def testConfig():
    getAudioFile("Test_Outro.mp3")
    return jsonify({
        'success': 'Data deleted.'
    })

########################
### Database Endpoints #
########################

### Add a podcast
@app.route('/api/podcasts', methods=['POST'])
def createPodcast():
    if request.form['title'] and request.form['description'] and request.form['s3_foldername']:
        podcast = Podcast(title=request.form['title'], description=request.form['description'], s3_foldername=request.form['s3_foldername'])
        podschema = PodcastSchema()
        db.session.add(podcast)
        db.session.commit()
        return podschema.jsonify(podcast), 201
    else:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Title, Description, or S3 Folder not given'
        }), 400


### List all podcasts
@app.route('/api/podcasts', methods=['GET'])
def listPodcasts():
    podcast = Podcast.query.all()
    podschema = PodcastSchema(many=True)
    return(podschema.dumps(podcast))

### Get Singular Podcast by title
@app.route('/api/podcast', methods=['GET'])
def listPodcast():
    if request.form['title']:
        podcast = Podcast.query.filter_by(title=request.form['title'])
        podschema = PodcastSchema()
        return(podschema.dumps(podcast))
    else:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Title not given'
        }), 400

### Update a podcast
@app.route('/api/podcast/<id>', methods=['PUT'])
def updatePodcast(id):
    if request.form['title'] and request.form['description'] and request.form['s3_foldername']:
        podcast = Podcast.query.get(id)
        podschema = PodcastSchema()
        podcast.title = request.form['title']
        podcast.description = request.form['description']
        podcast.s3_foldername = request.form['s3_foldername']
        db.session.commit()
        return(podschema.dumps(podcast))
    else:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Title, Description, or S3 Folder not given'
        }), 400

### Remove a podcast
@app.route("/api/podcast/<id>", methods=["DELETE"])
def deletePodcast(id):
    podcast = Podcast.query.get(id)
    podschema = PodcastSchema()
    db.session.delete(podcast)
    db.session.commit()
    return jsonify({
        'success': 'Data deleted.'
    })

#########################
### Podcast Creation
#########################

### Fetch Podcast
@app.route("/api/podcast/<id>/generate", methods=["GET"])
def assemblePodcast(id):
    podcast = Podcast.query.get(id)

    ### fetch podcast audio from s3


    
    filename = 'test_output.mp3'
    return send_from_directory(app.config['SLEEPCAST_DIRECTORY'], filename, conditional=True)

    ### Call the assembler with specified podcast

    ### Return a full podcast file to user
