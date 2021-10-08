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
    data_path = r'\data\raw\elections\wyniki_gl_na_listy_po_powiatach_sejm.xlsx'
    data = pd.read_excel(project_dir + data_path)

    # restricting dataframe to necessary columns
    data = data[['Kod TERYT', 'Powiat',
                 'Liczba głosów ważnych oddanych łącznie na wszystkie listy kandydatów',
                 'KOMITET WYBORCZY PRAWO I SPRAWIEDLIWOŚĆ - ZPOW-601-9/19']]

    # renaming columns
    data.rename(columns={'Kod TERYT': "teryt", "Powiat": "powiat",
                         'Liczba głosów ważnych oddanych łącznie na wszystkie listy kandydatów': 'glosy',
                         'KOMITET WYBORCZY PRAWO I SPRAWIEDLIWOŚĆ - ZPOW-601-9/19': 'pis'}, inplace=True)


    # reshaping teryt
    data['teryt'] = data['teryt'].apply(lambda x: str(x).zfill(6)[:4])

    # calculating votes %
    data['%_glosy'] = data.apply(lambda x: (x['pis']/x['glosy']) * 100 ,axis=1)

    # restricting dataframe to necessary columns
    data = data[['teryt', 'powiat', '%_glosy']]
    print(data)

    # saving data
    print('saving data - all')
    data_save_path = r'\data\interim\elections\elections_county'
    data.to_excel(project_dir + data_save_path + '.xlsx', index=False)
    data.to_csv(project_dir + data_save_path + '.csv', index=False)

    # end time of program + duration
    end_time = time.time()
    execution_time = int(end_time - start_time)
    print('\n', 'exectution time = ', execution_time, 'sec')
if __name__ == "__main__":
    main()