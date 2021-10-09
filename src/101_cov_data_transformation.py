from pathlib import Path
import pandas as pd
import time
from datetime import datetime
import glob

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of program
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[1])

    # loading data
    print('loading data')
    data = pd.read_excel(project_dir + r'\data\interim\covid_data\covid_county_daily.xlsx')

    print(data.head())
    # getting rid of zero values in date column
    data = data[data['data'] != 0]

    # changing to date
    data['data'] = data['data'].apply(lambda x: datetime.strptime(str(x),'%Y-%m-%d'))

    # restricting data frame to month
    data = data[(data['data'] >= datetime.strptime('2021-09-03','%Y-%m-%d')) & (data['data'] <= datetime.strptime('2021-10-03','%Y-%m-%d'))]

    # # getting ridd of 0 values in teryt
    # data = data[data['teryt'] != 0]

    # grouping by data
    data_aggr = pd.DataFrame(data.groupby(['teryt', 'powiat_miasto'])['zarazenia', 'zgony'].sum().reset_index())

    # population data
    print('loading data')
    pop = pd.read_excel(project_dir + r'\data\interim\covid_data\population_county.xlsx')

    # merging with population data
    data_merge = data_aggr.merge(pop, on='teryt')

    data_merge['zar_10k'] = data_merge.apply(lambda x: (x['zarazenia'] / x['ludnosc']) * 10000, axis=1)
    data_merge['zgon_100k'] = data_merge.apply(lambda x: (x['zgony'] / x['ludnosc']) * 100000, axis=1)

    print(data_merge.head())
    print(data_merge.dtypes)

    print('saving files')
    data_save_path = r'\data\interim\covid_data\covid_county_month'
    data_merge.to_excel(project_dir + data_save_path + '.xlsx', index=False)
    data_merge.to_csv(project_dir + data_save_path + '.csv', index=False)

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')
if __name__ == "__main__":
    main()