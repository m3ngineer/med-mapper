import pandas as pd
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

    search = ZipcodeSearchEngine()

    for npi in hp_dict:
        lats.append(search.by_zipcode(hp_dict[npi]['zip']).Latitude)
        longs.append(search.by_zipcode(hp_dict[npi]['zip']).Longitude)
        zips.append(hp_dict[npi]['zip'])
        npis.append(npi)
        names.append(hp_dict[npi]['last_name'] + ', ' + hp_dict[npi]['first_name'])
        names_zips.append(hp_dict[npi]['last_name'] + ', ' + hp_dict[npi]['first_name'] + ', ' + str(hp_dict[npi]['zip']))

    zipcode_df = pd.DataFrame({'npi': npis, 'name': names, 'zip': zips, 'name_zip': names_zips, 'latitude': lats, 'longitude': longs})

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
            #title = 'Locations of Predicted Physicians for Imbruvica',
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

def get_cohort_stats(high_prob_npis, medicare_data):
    '''
    Input: Takes in npis for high_prescribing_doctors and medicare data for past year
    Output: Returns total spending for all of drug, and proportion sold by this group of high prescribing physicians
    '''

    prescriber_data = pd.read_csv(medicare_data, delimiter='\t')
    cohort_stats = []

    high_prescribers_target = prescriber_data[(prescriber_data['drug_name'] == 'IMBRUVICA') & (prescriber_data['npi'].isin(high_prob_npis))]
    all_prescribers_target = prescriber_data[prescriber_data['drug_name'] == 'IMBRUVICA']

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
