from flask import Flask, render_template, url_for, request
import pickle
from sklearn.externals import joblib
from src.model import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results', methods=['GET', 'POST'])
def results():

    #load model
    clf = pickle.load(open('src/model_imbruvica.pkl', 'rb'))

    #load npi_dictionary for 2015
    npi_dict_15 = pickle.load(open('src/npi_2015.pkl', 'rb'))

    #get current year test data by target drug (currently set to imbruvica)
    X = clean_data('data/heme-onc_d_15.csv')

    #predict X values
    predictions = clf.predict(X)

    # get npis that are high confidence high prescribers
    high_prob_npis = X[clf.predict_proba(X)[:, 1] > 0.75].index.values

    # Create dictionary of predicted high prescribers
    hp_dict = {k: npi_dict_15[k] for k in high_prob_npis}

    if request.method == 'POST':

        selection = request.form['selection']

    return render_template('results.html', selection=selection, hp_dict=hp_dict)

if __name__ == '__main__':
    app.run(debug=True)
