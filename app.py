import pandas as pd
import geojson as gj
import plotly.express as px
import urllib.request

import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# # # # # VARIABLES # # # # # #
date = '2021-10-06'

# # # # # DATA # # # # # #
# loading dataframe - vaccinations
data_vac_path = 'https://github.com/sebastian-konicz/covid-dashboard/raw/main/data/interim/vaccination_data/vaccinations_county_all.xlsx'
data_vac = pd.read_excel(data_vac_path, engine='openpyxl')

# setting date
data_vac = data_vac[data_vac['data'] == date]

# restricting dataframe
data_vac = data_vac[['teryt', 'powiat', '%_zaszczepieni']]
# reshaping teryt
data_vac['teryt'] = data_vac['teryt'].apply(lambda x: str(x).zfill(4))

# loading dataframe - covid_cases
data_cov_path = 'https://github.com/sebastian-konicz/covid-dashboard/raw/main/data/interim/covid_data/covid_county_all.xlsx'
data_cov = pd.read_excel(data_cov_path, engine='openpyxl')

# setting date
data_cov = data_cov[data_cov['data'] == date]

# restricting dataframe
data_cov = data_cov[['teryt', 'powiat', 'zarazenia']]
# reshaping teryt
data_cov = data_cov[data_cov['teryt'] != 0]
data_cov['teryt'] = data_cov['teryt'].apply(lambda x: str(x).zfill(4))

# loading geojson files
# municipality
jsonurl_mun = 'https://github.com/sebastian-konicz/covid-dashboard/raw/main/data/final/geo_municipality.geojson'
with urllib.request.urlopen(jsonurl_mun) as url:
    geojson_mun = gj.load(url)
# county
jsonurl_cou = 'https://github.com/sebastian-konicz/covid-dashboard/raw/main/data/final/geo_county.geojson'
with urllib.request.urlopen(jsonurl_cou) as url:
    geojson_cou = gj.load(url)
# county
jsonurl_voi = 'https://github.com/sebastian-konicz/covid-dashboard/raw/main/data/final/geo_voivodeship.geojson'
with urllib.request.urlopen(jsonurl_voi) as url:
    geojson_voi = gj.load(url)

# # # # # # VACCINATION MAP # # # # # #
# get the maximum value to cap displayed values - vaccinations
max_log_vac = data_vac['%_zaszczepieni'].max()
min_val_vac = data_vac['%_zaszczepieni'].min()
max_val_vac = int(max_log_vac) + 1

fig_vac = px.choropleth_mapbox(data_vac,
                           geojson=geojson_cou,
                           featureidkey='properties.JPT_KOD_JE',
                           locations='teryt',
                           hover_name='powiat',
                           # hover_data='%_zaszczepieni',
                           color='%_zaszczepieni',
                           title='procent osób zaszczepionych',
                           color_continuous_scale=px.colors.diverging.RdBu,
                           range_color=(min_val_vac, max_val_vac),
                           mapbox_style="carto-positron",
                           zoom=5, center={"lat": 52, "lon": 19},
                           opacity=0.5,
                           )
fig_vac.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# # # # # # COVID CASES MAP # # # # # #
# get the maximum value to cap displayed values - vaccinations
max_log_cov = data_cov['zarazenia'].max()
min_val_cov = data_cov['zarazenia'].min()
max_val_cov = int(max_log_vac) + 1

fig_cov = px.choropleth_mapbox(data_cov,
                           geojson=geojson_cou,
                           featureidkey='properties.JPT_KOD_JE',
                           locations='teryt',
                           color='zarazenia',
                           color_continuous_scale=px.colors.diverging.RdBu_r,
                           range_color=(min_val_cov, max_val_cov),
                           mapbox_style="carto-positron",
                           zoom=5, center={"lat": 52, "lon": 19},
                           opacity=0.5,
                           )
fig_cov.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# # # # # LAYOUT # # # # # #
width = 6

app.layout = dbc.Container([
                html.H1('Mapa szczepień na COVID-19 w Polsce ',
                        style={'textAlign': 'center'}),
                dbc.Row([
                    dbc.Col(
                        dcc.Markdown('''
                            ##### Procent osób zaszczepionych przeciwko COVID19 w powiatach 
                            **Źródło**: Oficjalne dane dot. zaszczepienia przeciwko COVID19 w gminach z portalu [Otwarte dane](https://dane.gov.pl/pl/dataset/2476)  
                            **Uwagi**: Dane źródłowe zostały zagregowane z poziomu gmin do powiatów
                            '''),
                        width=width),
                    dbc.Col(
                        dcc.Markdown('''
                            ##### Liczba przypadków COVID-19 w podziale na powiaty 
                            **Źródło**: Oficjalne dane dot. zaszczepienia przeciwko COVID19 w gminach z portalu  [Otwarte dane]((https://dane.gov.pl/en/dataset/2477))
                             
                            '''),
                        width=width),
                ]),
                dbc.Row(
                    [
                        dbc.Col([
                            dcc.Graph(
                                id='vaccination_map',
                                figure=fig_vac
                            )
                        ], width=width),
                        dbc.Col([
                            dcc.Graph(
                                id='covid_cases_map',
                                figure=fig_cov
                            )
                        ], width=width),
                    ],
                ),
            ], fluid=True,
        )

if __name__ == '__main__':
    app.run_server(debug=True)