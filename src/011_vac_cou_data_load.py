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
    data_path = r'\data\raw\vaccination_data\poziom_wyszczepienia_mieszkańców_gmin_w_dniu_20211003_wskaźniki.csv'
    data = pd.read_csv(project_dir + data_path, encoding_errors='ignore', sep=';')

    # restricting dataframe to necessary columns
    data = data[['powiat_teryt', 'powiat_nazwa', 'liczba_ludnosci', 'w1_zaszczepieni_pacjenci']]

    # renaming columns
    data.rename(columns={'powiat_teryt': "teryt", "powiat_nazwa": "powiat",
                         'liczba_ludnosci': 'ludnosc', 'w1_zaszczepieni_pacjenci': 'zaszczepieni'}, inplace=True)

    # grouping by county
    data_aggr = pd.DataFrame(data.groupby(['teryt', 'powiat'])['ludnosc','zaszczepieni'].sum().reset_index())

    # calculating vaccination percent
    data_aggr['%_zaszczepieni'] = data_aggr.apply(lambda x: (x['zaszczepieni'] / x['ludnosc']) * 100, axis=1)

    # # reshaping data
    data_aggr['teryt'] = data_aggr['teryt'].apply(lambda x: str(x).zfill(4))

    print(data_aggr.head())

    # saving data
    print('saving data - all')
    data_save_path = r'\data\interim\vaccination_data\vaccinations_county_20211003'
    data_aggr.to_excel(project_dir + data_save_path + '.xlsx', index=False)
    data_aggr.to_csv(project_dir + data_save_path + '.csv', index=False)

    # population with teryt
    data_pop = data_aggr[['teryt', 'ludnosc']]

    print(data_pop.head())

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