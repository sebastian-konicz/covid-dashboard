from pathlib import Path
import pandas as pd
import time
import glob
import re
from datetime import datetime

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of program
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[1])
    file_path = project_dir + r'\data\raw\vaccination_data'

    # empty file list
    cov_files = []

    # reading all files in folder
    for each_file in glob.glob(file_path + r'\*.csv'):
        df = pd.read_csv(each_file, encoding_errors='ignore', sep=';')

        # extracting date form file name
        pattern_date = re.compile("([0-9])+")
        date = re.search(pattern_date, each_file).group()
        # converting string to date
        date = datetime.strptime(date, '%Y%m%d')
        date = datetime.strftime(date, '%Y-%m-%d')
        # adding column to dataframe
        df['data'] = date
        cov_files.append(df)

    # concatenating all data
    print('concatenation')
    data = pd.concat(cov_files,  ignore_index=True)

    # restricting dataframe to necessary columns
    data = data[['powiat_teryt', 'powiat_nazwa', 'liczba_ludnosci', 'w1_zaszczepieni_pacjenci', 'data']]

    # renaming columns
    data.rename(columns={'powiat_teryt': "teryt", "powiat_nazwa": "powiat",
                         'liczba_ludnosci': 'ludnosc', 'w1_zaszczepieni_pacjenci': 'zaszczepieni'}, inplace=True)

    # grouping by county
    data_aggr = pd.DataFrame(data.groupby(['data', 'teryt', 'powiat'])['ludnosc','zaszczepieni'].sum().reset_index())

    # calculating vaccination percent
    data_aggr['%_zaszczepieni'] = data_aggr.apply(lambda x: (x['zaszczepieni'] / x['ludnosc']) * 100, axis=1)

    # # reshaping data
    data_aggr['teryt'] = data_aggr['teryt'].apply(lambda x: str(x).zfill(4))

    print(data_aggr.head())

    # saving data
    print('saving data - all')
    data_save_path = r'\data\interim\vaccination_data\vaccinations_county_all'
    data_aggr.to_excel(project_dir + data_save_path + '.xlsx', index=False)
    data_aggr.to_csv(project_dir + data_save_path + '.csv', index=False)

    # population with teryt
    data_pop = data_aggr[data_aggr['data'] == '2021-08-07']
    data_pop = data_pop[['teryt', 'ludnosc', 'data']]

    # saving data
    print('saving data - population')
    data_save_path = r'\data\interim\covid_data\population_county'
    data_pop.to_excel(project_dir + data_save_path + '.xlsx', index=False)
    data_pop.to_csv(project_dir + data_save_path + '.csv', index=False)

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()