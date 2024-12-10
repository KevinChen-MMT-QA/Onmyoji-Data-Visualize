import os
import pandas as pd
import pymysql
import yaml
from sqlalchemy import create_engine
from query_templates import normal_query
from collections import defaultdict
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import json

db_config = {
    'user': 'root',
    'password': 'chenjian',
    'host': 'localhost',
    'port': 3306,
    'database': 'common'
}

def parse_query_config(yaml_file_path):
    with open(yaml_file_path, 'r', encoding='utf-8') as stream:
        config = yaml.safe_load(stream)
    B = config['ban']
    M = [shishen['name'] for shishen in config['team_m']]
    yuhun_M = [shishen['yuhun'] for shishen in config['team_m']]
    D = [shishen['name'] for shishen in config['team_d']]
    yuhun_D = [shishen['yuhun'] for shishen in config['team_d']]
    start_time, end_time = config['start_time'], config['end_time']
    return B, M, yuhun_M, D, yuhun_D, start_time, end_time

def report_result(M, D, result):
    M = list(filter(lambda x: x is not None, M))
    D = list(filter(lambda x: x is not None, D))
    win_dict, tot_dict = defaultdict(int), defaultdict(int)
    result_list = []
    for record in result:
        M_result, D_result, win = sorted(record[10: 15]), sorted(record[21: 26]), record[8]
        for m in M: 
            # if m is not None: 
            M_result.remove(m)
        for d in D: 
            # if d is not None: 
            D_result.remove(d)
        M_result, D_result = tuple(M_result), tuple(D_result)
        win_dict[(M_result, D_result)] += win
        tot_dict[(M_result, D_result)] += 1
    for m, d in win_dict.keys():
        result_list.append([list(M)+list(m), list(D)+list(d), win_dict[(m, d)], tot_dict[(m, d)]])
    return result_list

def execute_query(query):
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    return result

def get_image(M, D):
    shishen = json.loads(open('files/shishen.json', 'rb').read())
    name_to_id = {}
    for id in shishen.keys():
        name_to_id[shishen[id]['name']] = id
    M_image_file = ['./icon/icon_square/%s.jpg' %(name_to_id[name]) for name in list(filter(lambda x: x is not None, M))]
    D_image_file = ['./icon/icon_square/%s.jpg' %(name_to_id[name]) for name in list(filter(lambda x: x is not None, D))]

    M_image = np.array(Image.open(M_image_file[0]).convert('RGB'))
    D_image = np.array(Image.open(D_image_file[0]).convert('RGB'))
    for i in range(1, 5):
        M_image = np.concatenate((M_image, np.array(Image.open(M_image_file[i]).convert('RGB'))), axis=1)
        D_image = np.concatenate((D_image, np.array(Image.open(D_image_file[i]).convert('RGB'))), axis=1)

    return M_image, D_image

def excel2db(args=None):
    engine = create_engine(f'mysql+pymysql://{db_config["user"]}:{db_config["password"]}@{db_config["host"]}:{db_config["port"]}/{db_config["database"]}')
    if args is None:
        excel_directory = r'C:\Users\42436\Desktop\project\yys_crawler\20241208'
    else:
        excel_directory = args['saved_data_dir']
    table_name = 'yw_djzwj'

    for filename in os.listdir(excel_directory):
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            excel_file_path = os.path.join(excel_directory, filename)
            df = pd.read_excel(excel_file_path, index_col=0)
            df.to_sql(table_name, engine, if_exists='append', index=False)
            print(f"{filename} 已成功导入")

def show_query_result():
    B, M, yuhun_M, D, yuhun_D, start_time, end_time = parse_query_config('config/query_config.yaml')
    raw_result = execute_query(normal_query(B, M, yuhun_M, D, yuhun_D, start_time, end_time))
    clean_result = report_result(M, D, raw_result)
    clean_result.sort(key=lambda x: (x[-1], x[2]/x[3]), reverse=True)

    report_num = 40
    plt.figure(figsize=(report_num / 4, report_num / 2))
    for id, result in enumerate(clean_result[:report_num]):
        try:
            M_image, D_image = get_image(result[0], result[1])
        except:
            print('Error:', result)
            continue
        plt.subplot(report_num, 3, 3*id+1)
        plt.imshow(M_image)
        plt.axis('off')
        plt.subplot(report_num, 3, 3*id+2)
        plt.imshow(D_image)
        plt.axis('off')
        plt.subplot(report_num, 3, 3*id+3)
        plt.text(0, .4, '%d/%d' % (result[-2], result[-1]), fontsize=8)
        plt.axis('off')

    fig = plt.gcf()
    fig.set_size_inches(report_num / 5, report_num / 2)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0.1)
    plt.show()

if __name__ == '__main__':
    # excel2db()
    # sql = f'select * from dws_retail_cust_dj where '
    # show_query_result()
    B, M, yuhun_M, D, yuhun_D, start_time, end_time = parse_query_config('config/query_config.yaml')
    print(normal_query(B, M, yuhun_M, D, yuhun_D, start_time, end_time))