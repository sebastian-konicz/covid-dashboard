from pathlib import Path
import pandas as pd
import time

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def main():
    # start time of program
    start_time = time.time()

    # project directory
    project_dir = str(Path(__file__).resolve().parents[1])

    # loading data
    # gettig the file with PNA data
    data_path = r'\data\raw\poziom_wyszczepienia_mieszkańców_gmin_w_dniu_20210929_wskaźniki.csv'
    data = pd.read_csv(project_dir + data_path, encoding_errors='ignore', sep=';')

    # restricting dataframe to necessary columns
    data = data[['gmina_teryt', 'gmina_nazwa', '%_zaszczepionych_pen_dawk']]

    # renaming columns
    data.rename(columns={'gmina_teryt': "teryt", "gmina_nazwa": "municipality", '%_zaszczepionych_pen_dawk': '%_vaccinated'}, inplace=True)

    print(data.head(10))

    # reshaping data
    data['teryt'] = data['teryt'].apply(lambda x: str(x).zfill())
    data['%_vaccinated'] = data['%_vaccinated'].apply(lambda x: float(str(x).replace(',', ".")))

    print(data.head(10))
    print(data.dtypes)

    data_save_path = r'\data\interim\vaccinations_municipality_20210929'
    data.to_excel(project_dir + data_save_path + '.xlsx', index=False)
    data.to_csv(project_dir + data_save_path + '.csv', index=False)

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')

if __name__ == "__main__":
    main()