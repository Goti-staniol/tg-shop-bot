import yaml
import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
db_url = os.getenv('DB_URL')

html = 'HTML'

with open('data/texts.yaml', 'r', encoding='utf-8') as f:
    texts = yaml.safe_load(f)