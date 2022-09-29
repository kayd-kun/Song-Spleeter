import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory, jsonify
from werkzeug.utils import secure_filename # For File Uploads

from sleepter_separate import separate_vocals_instruments

# Configs
UPLOAD_FOLDER = "/home/kayd/cs/ai/embed_model_web/flask_spleeter/UploadedAudios"
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/",  methods=['GET', 'POST'])
def hello_world():
    # Check if post request has the file part
    if request.method == 'POST':
        # flash('No File Part')
        if 'file' not in request.files:
            flash('No File Part')
            return redirect(request.url)
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            print("============================")
            filename = secure_filename(file.filename)
            print(filename)
            audio_save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(audio_save_path)
            separate_audio(audio_save_path)
            flash('File Saved')
            
            # Return Vocal Audio Path and Instrument Audio Path
            to_segmented_dir_path = '/home/kayd/cs/ai/embed_model_web/flask_spleeter/SegmentedAudio/'
            file_without_ext = filename[:-4] # Remove .mp3 extension
            audio_path = to_segmented_dir_path + file_without_ext + "/"
            vocals_path = audio_path + "vocals.wav"
            accompaniment_path = audio_path + "accompaniment.wav"

            # New Trial
            vocals_path = "/SegmentedAudio/" + file_without_ext + "vocals.wav"
            accompaniment = "/SegmentedAudio/" + file_without_ext + "accompaniment.wav"

            return jsonify(song_name=file_without_ext)
    return render_template("david.html")

@app.route('/original/<path:audio_name>') # path: like string but also accepts slashes
def get_original(audio_name):
    print("=========================")
    audio_name = audio_name.replace("/","") + ".mp3"
    print(audio_name)
    # /home/kayd/cs/ai/embed_model_web/flask_spleeter/UploadedAudios
    file_dir = f"/home/kayd/cs/ai/embed_model_web/flask_spleeter/UploadedAudios/"
    return send_from_directory(file_dir, audio_name)

@app.route('/vocals/<path:audio_name>') # path: like string but also accepts slashes
def get_vocals(audio_name):
    print("=========================")
    audio_name = audio_name.replace("/","")
    # print(audio_name)
    file_dir = f"/home/kayd/cs/ai/embed_model_web/flask_spleeter/SegmentedAudio/{audio_name}/"
    return send_from_directory(file_dir, "vocals.wav")

@app.route('/accompaniment/<path:audio_name>') # path: like string but also accepts slashes
def get_acc(audio_name):
    print("=========================")
    audio_name = audio_name.replace("/","")
    # print(audio_name)
    file_dir = f"/home/kayd/cs/ai/embed_model_web/flask_spleeter/SegmentedAudio/{audio_name}/"
    return send_from_directory(file_dir, "accompaniment.wav")

def separate_audio(input_audio_path):
    output_dir = "/home/kayd/cs/ai/embed_model_web/flask_spleeter/SegmentedAudio/"
    input_file_path = input_audio_path
    separate_vocals_instruments(input_file_path, output_dir)