import pandas as pd
import numpy as np
import json
import plotly
import plotly.graph_objs as go # delete just for example code
import plotly.plotly as py

def create_zipcode_df(hp_dict):
    '''
    Input: Takes in dictionary of high-prescribing physicians with 'npi' as keys and 'zip' as a value
    Output: Returns dataframe of longitudes and latitudes for zipcodes of interest
    '''
    from uszipcode import ZipcodeSearchEngine

    lats = []
    longs = []
    zips = []
    names = []
    npis = []
    names_zips = []
    densities = []

    search = ZipcodeSearchEngine()

    for npi in hp_dict:
        lats.append(search.by_zipcode(hp_dict[npi]['zip']).Latitude)
        longs.append(search.by_zipcode(hp_dict[npi]['zip']).Longitude)
        zips.append(hp_dict[npi]['zip'])
        npis.append(npi)
        names.append(hp_dict[npi]['last_name'] + ', ' + hp_dict[npi]['first_name'])
        names_zips.append(hp_dict[npi]['last_name'] + ', ' + hp_dict[npi]['first_name'] + ', ' + str(hp_dict[npi]['zip']))
        densities.append(search.by_zipcode(hp_dict[npi]['zip']).Density)

    zipcode_df = pd.DataFrame({'npi': npis, 'name': names, 'zip': zips, 'name_zip': names_zips, 'latitude': lats, 'longitude': longs, 'density': densities})

    return zipcode_df

def show_map(hp_dict):
    '''
    Input: Takes in dataframe of longitudes and latitudes for each zipcode
    Output: Returns dataframe of longitudes and latitudes for each zipcode
    '''
    zipcode_df = create_zipcode_df(hp_dict)

    data = [ dict(
            type = 'scattergeo',
            locationmode = 'USA-states',
            lon = zipcode_df['longitude'],
            lat = zipcode_df['latitude'],
            #text = df['text'],
            mode = 'markers',
            ids=zipcode_df['zip'],
            text=zipcode_df['name_zip'],
            hoverinfo='text',
            marker = dict(
                size = 8,
                opacity = 0.6,
                reversescale = True,
                autocolorscale = False,
                symbol = 'circle',
                line = dict(
                    width=1,
                    color='rgba(102, 102, 102)'
                )),
            )]

    layout = dict(
            #title = 'Locations of Predicted Physicians for drug',
            colorbar = False,
            autosize=True,
            width=500,
            height=300,
            margin = dict(
                l=5,
                r=5,
                b=0,
                t=0,
                pad=0
            ),
            displayModeBar = False,
            xaxis = dict(
                fixedrange = True
                ),
            yaxis = dict(
                fixedrange = True
            ),
            dragmode = 'pan',
            geo = dict(
                scope='usa',
                projection=dict( type='albers usa' ),
                showland = True,
                landcolor = "rgb(250, 250, 250)",
                subunitcolor = "rgb(217, 217, 217)",
                countrycolor = "rgb(217, 217, 217)",
                countrywidth = 0.5,
                subunitwidth = 0.5
            ),
        )

    fig = dict( data=data, layout=layout )
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder) #encode in JSON for flask template

    # return py.iplot( fig, validate=False, filename='location_physicians' )
    return graphJSON # use this return for embedding in flask and above for ipython

def show_specialty_hist(high_prob_npis, medicare_data, drug):
    '''
    Take in list of number of claims for each specialty ('Hematology-Oncology', 'Medical Oncology', 'Hematology')
    Returns JSON for plotting histogram
    '''

    prescriber_data = pd.read_csv(medicare_data, delimiter='\t')

    specialties = ['Hematology-Oncology', 'Medical Oncology', 'Hematology']

    claims = []
    for i, specialty in enumerate(specialties, 1):
        claims_specialty = prescriber_data.loc[(prescriber_data['npi'].isin(high_prob_npis)) &
                               (prescriber_data['drug_name'] == drug) &
                               (prescriber_data['specialty_description'] == specialty),
                               'total_claim_count'].values

        claims.append(claims_specialty)

    data = []
    colors = [#'rgb(178,24,43)',
     'rgb(214,96,77)',
     #'rgb(244,165,130)',
     #'rgb(253,219,199)',
     #'rgb(209,229,240)',
     'rgb(146,197,222)',
     #'rgb(67,147,195)',
     'rgb(33,102,172)']

    for i, specialty_claims in enumerate(claims):
        trace = go.Histogram(
            x=specialty_claims,
            #opacity=1,
            name=specialties[i],
            xbins=dict(
                start=0,
                end=156,
                size=5
            ),
            autobinx=False,
            marker=dict(
                color=colors[i]
            ),
        )

        data.append(trace)

    updatemenus = list([
        dict(type="buttons",
             buttons=list([
                dict(label = 'Stack',
                     method = 'relayout',
                     args = ['barmode', 'stack']
                     ),
                dict(label = 'Overlay',
                     method = 'relayout',
                     args = ['barmode', 'overlay']
                     ),
                ]),
            pad = {'r': 10, 't': 10},
            showactive = True,
            x = 1.25,
            xanchor = 'right',
            y = 0.7,
            yanchor = 'top'
            )
        ])

    layout = go.Layout(barmode='stack',
                       updatemenus=updatemenus,
                       xaxis=dict(
                        title='Total Number of Claims'
                       ),
                       yaxis=dict(
                        title='Number of Providers')
                       )
    fig = dict( data=data, layout=layout )
    histJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return histJSON

def show_ratio_bars(high_prob_npis, medicare_data_y1, medicare_data_y2, drug):
    '''
    Input:

        high_prob_npis: list of recommended physician NPI
        medicare_data_y1: filename of medicare data from previous year
        medicare_data_y2: filename of medicare data from current year
        drug: drug name
    Output:
        Returns JSON for plotting bar graphs of ratio of claims of drug to claims of related drugs
    '''

    # Load data
    y1 = pd.read_csv(medicare_data_y1, delimiter='\t')
    y2 = pd.read_csv(medicare_data_y2, delimiter='\t')

    # Create pivot tables of NPI x Drug claim counts
    y1_claims = y1.loc[:, ['npi', 'total_claim_count', 'drug_name']]
    y1_claims_drugs = pd.pivot_table(y1_claims, index='npi', columns='drug_name', values='total_claim_count', fill_value=0)
    y2_claims = y2.loc[:, ['npi', 'total_claim_count', 'drug_name']]
    y2_claims_drugs = pd.pivot_table(y2_claims, index='npi', columns='drug_name', values='total_claim_count', fill_value=0)

    # Create transformed table with difference in claims from 2015 to 2016
    delta_claims_y1y2 = (((y2_claims_drugs + 1) - (y1_claims_drugs + 1)) / (y1_claims_drugs + 1))
    delta_claims_y1y2.fillna(0, inplace=True)

    # Plot ratios of Imbruvica prescriptions to other related drugs in high prescribers vs all prescribers

    related_drugs_full = [
                    "RITUXAN",
                    "CYCLOPHOSPHAMIDE",
                    "TREANDA",
                    #"BENDEKA",
                    "PREDNISONE",
                    'DEXAMETHASONE',
                    'NEUPOGEN',
                    #'GAZYVA',
                    'NEULASTA',
                    'ZYDELIG',
                    'VENCLEXTA',
                    'LEUKERAN',
                    'DOXORUBICIN HCL',
                    #'DOXORUBICIN HCL LIPOSOME',
                    'ALLOPURINOL'
                  ]

    labels = ('High prescribers', 'All prescribers')
    data_avg = []
    data_hp = []
    for i, related_drug in enumerate(related_drugs_full[1:], 1):
        if y2_claims_drugs.loc[:, related_drug.upper()].mean() > 0:
            if y2_claims_drugs.loc[high_prob_npis, related_drug.upper()].mean() > 0:
                data_avg.append(y2_claims_drugs.loc[:, drug.upper()].mean() / y2_claims_drugs.loc[:, related_drug.upper()].mean())
                data_hp.append(y2_claims_drugs.loc[high_prob_npis, drug.upper()].mean() / y2_claims_drugs.loc[high_prob_npis, related_drug.upper()].mean())

    #scale ratio data to be between 0 and 1 to fit on same graph
    data_max = np.vstack((data_avg, data_hp)).max(axis=0)
    data_avg_scale = data_avg / data_max
    data_hp_scale = data_hp / data_max

    ratio_avg = go.Bar(
        x=related_drugs_full,
        y=data_avg,
        #text=data_avg,
        textposition = 'auto',
        marker=dict(
            color='rgb(214,96,77)',
            ),
        opacity=0.9,
        name='Average'
    )

    ratio_hp = go.Bar(
        x=related_drugs_full,
        y=data_hp,
        #text=y2,
        textposition = 'auto',
        marker=dict(
            color='rgb(33,102,172)',
            ),
        opacity=0.9,
        name='Recommended'
    )

    ratio_avg_scale = go.Bar(
        x=related_drugs_full,
        y=data_avg_scale,
        #text=data_avg,
        textposition = 'auto',
        marker=dict(
            color='rgb(214,96,77)',
            ),
        opacity=0.9,
        name='Average',
        visible=False
    )

    ratio_hp_scale = go.Bar(
        x=related_drugs_full,
        y=data_hp_scale,
        #text=y2,
        textposition = 'auto',
        marker=dict(
            color='rgb(33,102,172)',
            ),
        opacity=0.9,
        name='Recommended',
        visible=False
    )

    updatemenus=list([
        dict(
            buttons=list([
                dict(
                    args=['visible', [True, True, False, False]],
                    label='Normal Data',
                    method='restyle'
                ),
                dict(
                    args=['visible', [False, False, True, True]],
                    label='Scaled Data',
                    method='restyle'
                )
        ]),
            #direction = 'left',
            pad = {'r': 10, 't': 10},
            showactive = True,
            type = 'buttons',
            x = 1.25,
            xanchor = 'right',
            y = 0.75,
            yanchor = 'top'
            ),
    ])

    data = [ratio_avg, ratio_hp, ratio_avg_scale, ratio_hp_scale]

    ytitle = 'Ratio ' + drug.capitalize() + ' : Drug'
    layout = go.Layout(updatemenus=updatemenus,
                       xaxis=dict(),
                       yaxis=dict(
                        title=ytitle)
    )

    fig = dict( data=data, layout=layout)
    ratioJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return ratioJSON


def get_cohort_stats(high_prob_npis, medicare_data, drug):
    '''
    Input: Takes in npis for high_prescribing_doctors and medicare data for past year
    Output: Returns total spending for all of drug, and proportion sold by this group of high prescribing physicians
    '''

    prescriber_data = pd.read_csv(medicare_data, delimiter='\t')
    cohort_stats = []

    high_prescribers_target = prescriber_data[(prescriber_data['drug_name'] == drug) & (prescriber_data['npi'].isin(high_prob_npis))]
    all_prescribers_target = prescriber_data[prescriber_data['drug_name'] == drug]

    # find summary percent greater statistics than mean
    hp_target_means = high_prescribers_target[['total_claim_count', 'nonlis_drug_cost', 'pdp_drug_cost', 'mapd_drug_cost', 'brand_drug_cost', 'generic_drug_cost', 'total_drug_cost']].mean()
    ap_target_means = all_prescribers_target[['total_claim_count', 'nonlis_drug_cost', 'pdp_drug_cost', 'mapd_drug_cost', 'brand_drug_cost', 'generic_drug_cost', 'total_drug_cost']].mean()
    stats = ((hp_target_means - ap_target_means) / ap_target_means * 100).round(1)
    cohort_stats.append(stats)

    # find summary statistics on percentage of total_claims and total_drug_costs for drug that these physicians made
    hp_target_sums = high_prescribers_target[['total_claim_count', 'nonlis_drug_cost', 'pdp_drug_cost', 'mapd_drug_cost', 'brand_drug_cost', 'generic_drug_cost', 'total_drug_cost']].sum()
    ap_target_sums = all_prescribers_target[['total_claim_count', 'nonlis_drug_cost', 'pdp_drug_cost', 'mapd_drug_cost', 'brand_drug_cost', 'generic_drug_cost', 'total_drug_cost']].sum()
    stats = (hp_target_sums/ap_target_sums * 100)[['total_claim_count', 'total_drug_cost']].round(2)
    cohort_stats.append(stats)

    return cohort_stats
