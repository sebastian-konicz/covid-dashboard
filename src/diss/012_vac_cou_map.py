from pathlib import Path
import pandas as pd
import plotly.express as px
import geopandas as gpd
import geojson as gj
import time

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[1])

    # loading map data
    geo_path = r'\data\geo\admin\Powiaty.shp'
    map = gpd.read_file(project_dir + geo_path)

    # restricting dataframe
    map = map[['JPT_KOD_JE', 'geometry']]
    map['JPT_KOD_JE'] = map['JPT_KOD_JE'].apply(lambda x: str(x))

    # loading data
    data_path = r'\data\interim\vaccination_data\vaccinations_county_20211003.xlsx'
    data = pd.read_excel(project_dir + data_path)

    # restricting dataframe
    data = data[['teryt', 'powiat', '%_zaszczepieni']]

    data['teryt'] = data['teryt'].apply(lambda x: str(x).zfill(4))

    # simplifying geometry
    map.geometry = map.geometry.simplify(0.005)

    # saving geometry to geojson file
    map.to_file(project_dir + r'\data\interim\geo\geo_county.geojson', driver='GeoJSON')

    # loading geojson
    with open(project_dir + r'\data\interim\geo\geo_county.geojson') as file:
        geojson = gj.load(file)

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

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()