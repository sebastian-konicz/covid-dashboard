import os
from pathlib import Path
import geopandas as gpd
import plotly.express as px

import dash
from dash import dcc
from dash import html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# # project directory
# project_dir = str(Path(__file__).resolve().parents[0])
#
# # loading geodataframe
# geo_path = r'\data\interim\geo\geo_vaccinations.geojson'
# geo_df = gpd.read_file(project_dir + geo_path)
#
# # get the maximum value to cap displayed values
# max_log = geo_df['%_vaccinated'].max()
# min_val = geo_df['%_vaccinated'].min()
# max_val = int(max_log) + 1
#
# fig = px.choropleth_mapbox(geo_df,
#                            geojson=geo_df.geometry,
#                            locations=geo_df.index,
#                            color='%_vaccinated',
#                            color_continuous_scale=px.colors.diverging.RdBu,
#                            range_color=(min_val, max_val),
#                            mapbox_style="carto-positron",
#                            zoom=5,
#                            center={"lat": 52, "lon": 19},
#                            opacity=0.5,
#                            )
#
# fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

app.layout = html.Div([
    html.H2('Mapa szczepień na COVID-19 w Polsce '),
    dcc.Graph(
            id='example-map',
            # figure=fig
    ),
])

if __name__ == '__main__':
    app.run_server(debug=True)