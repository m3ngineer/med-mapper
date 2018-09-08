from flask import Flask, render_template, url_for, request
import pickle
from sklearn.externals import joblib
from src.model import *
from src.dashboard import *

import dash
import dash_core_components as dcc
import dash_html_components as html

server = Flask(__name__)
app = dash.Dash(__name__, server=server, url_base_pathname='/dummypath/')

@server.route('/')
def home():
    return render_template('index.html')

@server.route('/results', methods=['GET', 'POST'])
def results():

    if request.method == 'POST':

        selection = request.form['selection']
        print(selection)
    #load model
    filename = 'src/models/model_' + selection.lower() + '.pkl'
    clf = pickle.load(open(filename, 'rb'))

    #load npi_dictionary for 2016
    npi_dict_16 = pickle.load(open('src/dashboard/npi_2016.pkl', 'rb'))

    #get current year test data by target drug (currently set to imbruvica)
    #X = clean_data('data/heme-onc_d_16.csv') #replaced with pickled clean data for efficiency
    X = pickle.load(open('src/dashboard/data_heme-onc_d_16_clean.pkl', 'rb'))

    #predict y values and probabilities of being a high prescriber
    predictions = clf.predict(X)
    prob_hp = clf.predict_proba(X)[:, 1]

    # get npis that are high confidence high prescribers
    high_prob_npis = X[prob_hp > 0.75].index.values

    # Create dictionary of predicted high prescribers
    hp_dict = {k: npi_dict_16[k] for k in high_prob_npis}

    # Include probabilities of high prescriber in dictionary
    prob_hp_arr = np.concatenate([X.index.values.reshape(-1,1), prob_hp.reshape(-1,1)], axis=1)
    prob_hp_dict = {npi_prob[0]: npi_prob[1] for npi_prob in prob_hp_arr}

    for npi in high_prob_npis:
        if npi in prob_hp_dict:
            hp_dict[npi]['prob'] = "{:.2f}%".format(prob_hp_dict[npi] * 100)

    # Create map visualizing zipcodes of predicted prescribers
    # graphJSON = show_map(hp_dict)
    filename = 'src/dashboard/dashboard_graphJSON_17_' + selection.lower() + '.pkl'
    graphJSON = pickle.load(open(filename, 'rb')) # Predicted for Imbruvica 2017

    # Generate cohort statistics
    # cohort_stats = get_cohort_stats(high_prob_npis, 'https://s3.amazonaws.com/medmappr-data/heme-onc_d_16.csv')
    filename = 'src/dashboard/dashboard_cohort_stats_17_' + selection.lower() + '.pkl'
    cohort_stats = pickle.load(open(filename, 'rb'))

    # Create histogram of claims per specialty
    filename = 'src/dashboard/dashboard_histJSON_17_' + selection.lower() + '.pkl'
    histJSON = pickle.load(open(filename, 'rb'))

    # Create bar graphs of ratios between drug claims and claims of related drugs
    filename = 'src/dashboard/dashboard_ratioJSON_17_' + selection.lower() + '.pkl'
    ratioJSON = pickle.load(open(filename, 'rb'))

    return render_template('results.html',
        selection=selection,
        hp_dict=hp_dict,
        graphJSON=graphJSON,
        cohort_stats=cohort_stats,
        histJSON=histJSON,
        ratioJSON=ratioJSON
        )

# Dash app ------------------
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])

if __name__ == '__main__':
    server.run(host="0.0.0.0", port=8000, debug=True)
