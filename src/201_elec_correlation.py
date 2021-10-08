from pathlib import Path
import pandas as pd
import time
from scipy.stats import pearsonr

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of program
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[1])

    # loading data
    # gettig the file with PNA data
    data_path = r'\data\interim\elections\elections_county.xlsx'
    data = pd.read_excel(project_dir + data_path)

     # loading dataframe - vaccinations
    data_vac_path = 'https://github.com/sebastian-konicz/covid-dashboard/raw/main/data/interim/vaccination_data/vaccinations_county_20211003.xlsx'
    data_vac = pd.read_excel(data_vac_path, engine='openpyxl')

        # restricting dataframe
    data_vac = data_vac[['teryt', 'powiat', '%_zaszczepieni']]
    # reshaping teryt
    data_vac['teryt'] = data_vac['teryt'].apply(lambda x: str(x).zfill(4))
    data['teryt'] = data['teryt'].apply(lambda x: str(x))

    data = data[['teryt', 'powiat', '%_glosy']]
    data_vac = data_vac[['teryt', '%_zaszczepieni']]

    data_merge = data.merge(data_vac, on='teryt')

    vacc = data_merge['%_zaszczepieni'].to_list()
    vote = data_merge['%_glosy'].to_list()

    # calculate Pearson's correlation
    corr, _ = pearsonr(vacc, vote)
    print('Pearsons correlation: %.3f' % corr)

    # # saving data
    # print('saving data - all')
    # data_save_path = r'\data\interim\elections\elections_corr'
    # data.to_excel(project_dir + data_save_path + '.xlsx', index=False)
    # data.to_csv(project_dir + data_save_path + '.csv', index=False)

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')
if __name__ == "__main__":
    main()