# %%
import argparse
import warnings
from utils import show_query_result

parser = argparse.ArgumentParser()
parser.add_argument('--task_type', type=str, default='load-data')
parser.add_argument('--data_file_path', type=str, default=r'C:\Users\42436\Desktop\project\yys_crawler\20241110')
parser.add_argument('--create_table_name', type=str, default='')

# Load Configuration
args = parser.parse_known_args()[0]
warnings.filterwarnings('ignore')


# %%
if __name__ == '__main__':
    show_query_result()

# %%
