from pathlib import Path
import pandas as pd
import plotly.express as px
import geopandas as gpd
import folium
import time
from folium import IFrame

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of function
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[1])

    # loading map data
    geo_path = r'\data\geo\admin\Gminy.shp'
    map = gpd.read_file(project_dir + geo_path)

    # restricting dataframe
    map = map[['JPT_KOD_JE', 'geometry']]
    map['JPT_KOD_JE'] = map['JPT_KOD_JE'].apply(lambda x: str(x))

    # loading unemployment data
    data_path = r'\data\interim\vaccination_data\vaccinations_municipality_20210929.xlsx'
    data = pd.read_excel(project_dir + data_path)

    # restricting dataframe
    data = data[['teryt', 'municipality', '%_vaccinated']]

    data['teryt'] = data['teryt'].apply(lambda x: str(x).zfill(7))

    # # merging dataframes
    # map = map.merge(data, left_on='JPT_KOD_JE', right_on='teryt')

    # simplifying geometry
    map.geometry = map.geometry.simplify(0.005)

    # merging dataframe
    geo_df = map.merge(data, left_on="JPT_KOD_JE", right_on='teryt').set_index("teryt")

    # get the maximum value to cap displayed values
    max_log = geo_df['%_vaccinated'].max()
    min_val = geo_df['%_vaccinated'].min()
    max_val = int(max_log) + 1

    # prepare the range of the colorbar
    values = [i for i in range(max_val)]
    ticks = [10 * i for i in values]

    fig = px.choropleth_mapbox(geo_df,
                               geojson=geo_df.geometry,
                               locations=geo_df.index,
                               color='%_vaccinated',
                               color_continuous_scale=px.colors.diverging.RdBu,
                               range_color=(min_val, max_val),
                               mapbox_style="open-street-map",
                               zoom=5, center={"lat": 52, "lon": 19},
                               opacity=0.5,
                               )
    # fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.show()


    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

    return fig

if __name__ == "__main__":
    main()