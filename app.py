import pandas as pd
import geojson as gj
from pathlib import Path
import plotly.express as px

import dash
from dash import dcc
from dash import html

app = dash.Dash(__name__)
server = app.server

# project directory
project_dir = str(Path(__file__).resolve().parents[0])

# # # # # # DATA # # # # # #
# loading dataframe
# loading data
data_path = r'\data\interim\vaccination_data\vaccinations_county_20211003.xlsx'
data = pd.read_excel(project_dir + data_path)

# restricting dataframe
data = data[['teryt', 'powiat', '%_zaszczepieni']]

# reshaping teryt
data['teryt'] = data['teryt'].apply(lambda x: str(x).zfill(4))

# loading geojson
with open(project_dir + r'\data\interim\geo\geo_county.geojson') as file:
    geojson = gj.load(file)

# # get the maximum value to cap displayed values
#     max_log = data['%_zaszczepieni'].max()
#     min_val = data['%_zaszczepieni'].min()
#     max_val = int(max_log) + 1
#
#     fig = px.choropleth_mapbox(data,
#                                geojson=geojson,
#                                featureidkey='properties.JPT_KOD_JE',
#                                locations='teryt',
#                                color='%_zaszczepieni',
#                                color_continuous_scale=px.colors.diverging.RdBu,
#                                range_color=(min_val, max_val),
#                                mapbox_style="carto-positron",
#                                zoom=5, center={"lat": 52, "lon": 19},
#                                opacity=0.5,
#                                )
#     fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# # # # # # LAYOUT # # # # # #
app.layout = html.Div([
    html.H1('Mapa szczepień na COVID-19 w Polsce ',
            style={'textAlign': 'center'}),
    dcc.Graph(
            id='example-map',
            # figure=fig
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)