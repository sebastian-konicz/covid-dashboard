from pathlib import Path
import pandas as pd
# import matplotlib.pyplot as plt
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
    data_path = r'\data\interim\vaccinations_municipality_20210929.xlsx'
    data = pd.read_excel(project_dir + data_path)

    # restricting dataframe
    data = data[['teryt', 'municipality', '%_vaccinated']]

    data['teryt'] = data['teryt'].apply(lambda x: str(x).zfill(7))

    # merging dataframes
    map = map.merge(data, left_on='JPT_KOD_JE', right_on='teryt')

    # simplifying geometry
    map.geometry = map.geometry.simplify(0.005)

    # changing data to GeoJSON
    map_geo = map.to_json()

    # creating folium map
    map_graph = folium.Map([52, 19], zoom_start=6)

    folium.Choropleth(geo_data=map_geo,
                      name='choropleth',
                      data=data,
                      columns=['teryt', '%_vaccinated'],
                      key_on='feature.properties.JPT_KOD_JE',
                      bins=9,
                      fill_color='YlGnBu', # ‘BuGn’, ‘BuPu’, ‘GnBu’, ‘OrRd’, ‘PuBu’, ‘PuBuGn’, ‘PuRd’, ‘RdPu’, ‘YlGn’, ‘YlGnBu’, ‘YlOrBr’, and ‘YlOrRd’
                      fill_opacity=0.7,
                      line_opacity=0.2,
                      highlight=True,
                      legend_name="Szczepienia w procentach").add_to(map_graph)

    # adding labels to map
    style_function = lambda x: {'fillColor': '#ffffff',
                                'color': '#000000',
                                'fillOpacity': 0.1,
                                'weight': 0.1}

    tooltip = folium.features.GeoJson(
        map_geo,
        style_function=style_function,
        control=False,
        tooltip=folium.features.GeoJsonTooltip(
            fields=['municipality', '%_vaccinated'],
            aliases=['nazwa', '%_zaszczepionych_pełną_dawką'],
            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;")
        ),
    )

    map_graph.add_child(tooltip)
    # map_graph.keep_in_front(tooltip)
    folium.LayerControl().add_to(map_graph)

    # saving map
    print('saving map')
    map_graph.save(project_dir + r'\data\final\vaccination_map.html')
    map_graph.save(project_dir + r'\templates\vaccination_map.html')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()