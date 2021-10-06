from pathlib import Path
import pandas as pd
import time
import glob

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of program
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[1])
    file_path = project_dir + r'\data\raw\covid_data\danehistorycznepowiaty'

    # empty file list
    cov_files = []

    # reading all files in folder
    for each_file in glob.glob(file_path + r'\*.csv'):
        df = pd.read_csv(each_file, encoding_errors='ignore', sep=';')
        cov_files.append(df)

    # concatenating all data
    print('concatenation')
    data = pd.concat(cov_files,  ignore_index=True)

    print('saving files - all')
    data_save_path = r'\data\interim\covid_data\covid_county_all'
    data.to_excel(project_dir + data_save_path + '.xlsx', index=False)
    data.to_csv(project_dir + data_save_path + '.csv', index=False)

    # data transformation
    # restricting dataframe to necessary columns
    data_transf = data[['teryt', 'powiat_miasto', 'liczba_przypadkow', 'zgony', 'stan_rekordu_na']].copy()

    # renaming columns
    data_transf.rename(columns={'liczba_przypadkow': "zarazenia", 'stan_rekordu_na': 'data'}, inplace=True)

    # changing teryt code
    data_transf['teryt'] = data_transf['teryt'].apply(lambda x: str(x)[1:])

    # filling nan values
    data_transf.fillna(value=0, inplace=True)

    print(data_transf.head())

    print('saving files - daily')
    data_save_path = r'\data\interim\covid_data\covid_county_daily'
    data_transf.to_excel(project_dir + data_save_path + '.xlsx', index=False)
    data_transf.to_csv(project_dir + data_save_path + '.csv', index=False)

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')
if __name__ == "__main__":
    main()