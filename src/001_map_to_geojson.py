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

    # dictionary
    map_dict = {'Gminy': 'municipality',
                'Powiaty': 'county', 'Województwa': 'voivodeship'
                }

    for file, name in map_dict.items():
        print(file)
        print(name)

        # loading map data
        geo_path = r'\data\geo\admin\{file}.shp'.format(file=file)
        map = gpd.read_file(project_dir + geo_path)

        # restricting dataframe
        map = map[['JPT_KOD_JE', 'geometry']]
        map['JPT_KOD_JE'] = map['JPT_KOD_JE'].apply(lambda x: str(x))

        # simplifying geometry
        map.geometry = map.geometry.simplify(0.005)

        # saving geometry to geojson file
        map.to_file(project_dir + r'\data\final\geo\geo_{name}.geojson'.format(name=name), driver='GeoJSON')

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()