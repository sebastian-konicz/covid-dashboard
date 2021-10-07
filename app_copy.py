import pandas as pd
import geojson as gj
import plotly.express as px
import urllib.request

import dash
from dash import dcc
from dash import html
# import dash_core_components as dcc
# import dash_html_components as html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__)
server = app.server

# # # # # DATA # # # # # #
# loading dataframe - vaccinations
data_vac_path = 'https://github.com/sebastian-konicz/covid-dashboard/raw/main/data/interim/vaccination_data/vaccinations_county_20211003.xlsx'
data_vac = pd.read_excel(data_vac_path, engine='openpyxl')

# restricting dataframe
data_vac = data_vac[['teryt', 'powiat', '%_zaszczepieni']]
# reshaping teryt
data_vac['teryt'] = data_vac['teryt'].apply(lambda x: str(x).zfill(4))

# loading dataframe - covid_cases
data_cov_path = 'https://github.com/sebastian-konicz/covid-dashboard/raw/main/data/interim/covid_data/covid_county_month.xlsx'
data_cov = pd.read_excel(data_cov_path, engine='openpyxl')

# restricting dataframe
data_cov = data_cov[['teryt', 'powiat_miasto', 'zar_10k']]
# reshaping teryt
data_cov['teryt'] = data_cov['teryt'].apply(lambda x: str(x).zfill(4))

# loading geojson
jsonurl = 'https://github.com/sebastian-konicz/covid-dashboard/raw/main/data/interim/geo/geo_county.geojson'
with urllib.request.urlopen(jsonurl) as url:
    geojson = gj.load(url)

# # # # # # VACCINATION MAP # # # # # #
# get the maximum value to cap displayed values - vaccinations
max_log_vac = data_vac['%_zaszczepieni'].max()
min_val_vac = data_vac['%_zaszczepieni'].min()
max_val_vac = int(max_log_vac) + 1

fig_vac = px.choropleth_mapbox(data_vac,
                           geojson=geojson,
                           featureidkey='properties.JPT_KOD_JE',
                           locations='teryt',
                           color='%_zaszczepieni',
                           color_continuous_scale=px.colors.diverging.RdBu,
                           range_color=(min_val_vac, max_val_vac),
                           mapbox_style="carto-positron",
                           zoom=5, center={"lat": 52, "lon": 19},
                           opacity=0.5,
                           )
fig_vac.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      mapbox=dict(accesstoken='pk.eyJ1Ijoic2ViYXN0aWFua29uaWN6IiwiYSI6ImNrdWhjNGs0ZzE2bXAzMXJ0Y2RibmJ3OHMifQ.GRxIKFjuWBcrShcf6FCiJA'))

# # # # # # COVID CASES MAP # # # # # #
# get the maximum value to cap displayed values - vaccinations
max_log_cov = data_cov['zar_10k'].max()
min_val_cov = data_cov['zar_10k'].min()
max_val_cov = int(max_log_vac) + 1

fig_cov = px.choropleth_mapbox(data_cov,
                           geojson=geojson,
                           featureidkey='properties.JPT_KOD_JE',
                           locations='teryt',
                           color='zar_10k',
                           color_continuous_scale=px.colors.diverging.RdBu_r,
                           range_color=(min_val_cov, max_val_cov),
                           mapbox_style="carto-positron",
                           zoom=5, center={"lat": 52, "lon": 19},
                           opacity=0.5,
                           )
fig_cov.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      mapbox=dict(accesstoken='pk.eyJ1Ijoic2ViYXN0aWFua29uaWN6IiwiYSI6ImNrdWhjNGs0ZzE2bXAzMXJ0Y2RibmJ3OHMifQ.GRxIKFjuWBcrShcf6FCiJA'))

# # # # # LAYOUT # # # # # #
# app.layout = html.Div([
#     html.H1('Mapa szczepień na COVID-19 w Polsce ',
#             style={'textAlign': 'center'}),
#     html.Div([
#         dcc.Graph(
#                 id='vaccination_map',
#                 figure=fig_vac
#         ),
#         # dcc.Graph(
#         #         id='covid_cases_map',
#         #         figure=fig_cov
#         # ),
#     ]),
# ])

app.layout = dbc.Container([
            html.H1('Mapa szczepień na COVID-19 w Polsce ',
                    style={'textAlign': 'center'}),

            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(
                            id='vaccination_map',
                            figure=fig_vac
                        )
                    ),
                    dbc.Col(
                        dcc.Graph(
                            id='covid_cases_map',
                            figure=fig_cov
                        )
                    ),
                ],
            ),
        ],
        fluid=True,
    )

if __name__ == '__main__':
    app.run_server(debug=True)