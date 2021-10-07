import pandas as pd
import geojson as gj
import plotly.express as px
import urllib.request

import dash
# from dash import dcc
# from dash import html
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)
server = app.server

# # # # # DATA # # # # # #
# loading dataframe
# lopip freeze > requirements.txtading data
data_path = 'https://github.com/sebastian-konicz/covid-dashboard/raw/main/data/interim/vaccination_data/vaccinations_county_20211003.xlsx'
data = pd.read_excel(data_path, engine='openpyxl')

# restricting dataframe
data = data[['teryt', 'powiat', '%_zaszczepieni']]

# reshaping teryt
data['teryt'] = data['teryt'].apply(lambda x: str(x).zfill(4))

# loading geojson
jsonurl = 'https://github.com/sebastian-konicz/covid-dashboard/raw/main/data/interim/geo/geo_county.geojson'
with urllib.request.urlopen(jsonurl) as url:
    geojson = gj.load(url)

# with open(jsonurl) as file:
#     geojson = gj.load(file)

# geojson = gj.load(geo_path)

# get the maximum value to cap displayed values
max_log = data['%_zaszczepieni'].max()
min_val = data['%_zaszczepieni'].min()
max_val = int(max_log) + 1

fig = px.choropleth_mapbox(data,
                           geojson=geojson,
                           featureidkey='properties.JPT_KOD_JE',
                           locations='teryt',
                           color='%_zaszczepieni',
                           color_continuous_scale=px.colors.diverging.RdBu,
                           range_color=(min_val, max_val),
                           mapbox_style="carto-positron",
                           zoom=5, center={"lat": 52, "lon": 19},
                           opacity=0.5,
                           )
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
fig.show()

# # # # # # LAYOUT # # # # # #
app.layout = html.Div([
    html.H1('Mapa szczepień na COVID-19 w Polsce ',
            style={'textAlign': 'center'}),
    dcc.Graph(
            id='example-map',
            figure=fig
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)