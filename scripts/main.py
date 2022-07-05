import openpyxl
import util as util
import scraper
import video_cards
import data_handling
from multiprocessing import Process

video_cards_wb = r'C:\Users\dan_z\Documents\projects\WebScrapingVC2\files\videoCards.xlsx'
first_row = ['description', 'link', 'store', 'price']
csv_paths = [r'C:\Users\dan_z\Documents\projects\WebScrapingVC2\files\kabumResult.csv',
             r'C:\Users\dan_z\Documents\projects\WebScrapingVC2\files\pichauResult.csv',
             r'C:\Users\dan_z\Documents\projects\WebScrapingVC2\files\terabyteResult.csv',
             r'C:\Users\dan_z\Documents\projects\WebScrapingVC2\files\videoCards.csv']
ws_name = 'videoCards'


if __name__ == '__main__':
    for i in csv_paths:
        util.write_csv_file(i, first_row, 'w')

    p1 = Process(target=scraper.kabum_items, args=(csv_paths[0],))
    p1.start()
    print('Iniciando extração de placas de vídeo na Kabum...')

    p2 = Process(target=scraper.pichau_items, args=(csv_paths[1],))
    p2.start()
    print('Iniciando extração de placas de vídeo na Pichau...')

    p3 = Process(target=scraper.terabyte_items, args=(csv_paths[2],))
    p3.start()
    print('Iniciando extração placas de vídeo na Terabyte...\n')

    p1.join()
    p2.join()
    p3.join()

    csv_path = util.merges_all_csv()
    video_cards.creates_workbook(csv_path, video_cards_wb)
    workbook = openpyxl.load_workbook(video_cards_wb)
    worksheet = workbook[ws_name]
    for i in range(2, worksheet.max_row+1):
        data = data_handling.creates_data_dict(i, worksheet)
        video_cards.insert_data(i, worksheet, data)

    workbook.save(video_cards_wb)
