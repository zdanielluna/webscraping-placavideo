import glob
import pandas as pd
import csv
import os


def write_csv_file(path, data, mode='a'):
    try:
        with open(path, mode, newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(data)
    except:
        print(f'ocorreu um erro ao tentar criar o arquivo em {path} com os dados {data}')


def merges_all_csv(path=r'C:\Users\dan_z\Documents\projects\WebScrapingVC2\files'):
    os.chdir(path)
    new_file = 'videoCards.csv'
    extension = 'csv'
    try:
        all_filenames = [i for i in glob.glob(f'*.{extension}')]
        combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
        combined_csv.to_csv(new_file, index=False, encoding='utf-8')
    except:
        print(
            f'Ocorreu um erro ao mesclar os arquivos em: "{path}" - Verifique a integridade dos arquivos e seus cabeçalhos')

    return os.path.join(path, new_file)

# def create_worksheet(name, workbook_path):
#     workbook = openpyxl.load_workbook(workbook_path)
#     if name not in workbook.sheetnames:
#         try:
#             workbook.create_sheet(name)
#             workbook.save(workbook_path)
#         except:
#             print(f'ocorreu um erro ao tentar criar a sheet {name} em {workbook_path}')

# def create_workbook(csv_file, wb_path):
#     workbook = pd.ExcelFile(wb_path)
#     file_name = os.path.basename(csv_file).replace('.csv', '')
#     writer = pd.ExcelWriter(wb_path, mode='a', if_sheet_exists='replace')
#     read_file = pd.read_csv(csv_file)
#     read_file.to_excel(writer, sheet_name=file_name, index=False, header=False)


# def csv_to_multiple_sheets(csv_files, wb_path):
#     workbook = pd.ExcelFile(wb_path)
#     writer = pd.ExcelWriter(wb_path, mode='a', if_sheet_exists='replace')

#     for file in csv_files:
#         file_name = os.path.basename(file).replace('.csv', '')
#         if file_name in workbook.sheet_names:
#             read_file = pd.read_csv(file)
#             read_file.to_excel(writer, sheet_name=file_name, index=False, header=False)

#     writer.save()
