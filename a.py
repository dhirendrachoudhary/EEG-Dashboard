import os
import pandas as pd
import numpy as np
import sys
import os, fnmatch
import time
import plotly
import tensorflow as tf
from tensorflow.python.keras.layers import  Input, Embedding, Dot, Reshape, Dense
from tensorflow.python.keras.models import load_model
import plotly.graph_objs as go
import numpy as np
import json
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import json, json2html


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['csv', 'xlsx', 'xls'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/home')
@app.route('/')
def home():
        bar = create_plot()
        if bar is not None:
            lst = []
            for x in bar:
                lst.append(x[0])
            label = [x for x in range(len(lst))]
            return render_template('home.html', val = lst,labels = label)
        else:
            return redirect(url_for('upload'))

def create_plot():
    model = load_model('model/model.h5')
    for file in os.listdir('./uploads'):
        if file.endswith(".csv"):
            df = pd.read_csv("./uploads" + "/" + file,sep=",")
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            pred = model.predict(df.iloc[1:512,:14])
            os.remove("./uploads" + "/" + file)
            return pred

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    mod_lst = get_model(models)
    print(mod_lst)
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('home'))
    return render_template('upload.html',model_list =mod_lst)

models= []
def get_model(models):
    models=[]
    listOfFiles = os.listdir('./model')
    pattern = "*.h5"
    for entry in listOfFiles:
        if fnmatch.fnmatch(entry, pattern):
                models.append(entry)
    return models


@app.route("/test" , methods=['GET', 'POST'])
def test():
    select = request.form.get('list_status')
    return(str(select)) # just to see what select is

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000,debug = True)