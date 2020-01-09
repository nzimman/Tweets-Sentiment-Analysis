from flask import Flask
from sqlalchemy import create_engine
import time as t
import pandas as pd

# Connect to postgres
USERNAME = 'postgres'
PASSWORD = 'postgres'
HOST = 'postgresdb_pipe' #127.0.0.1 --> IP address loop back
PORT = '5432'
DBNAME = 'tweets'


t.sleep(200)

# connection string
conn_string = f'postgres://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'
db = create_engine(conn_string)

app = Flask(__name__)

result = db.execute('SELECT * FROM tweet_imp order by date_tweet desc limit 10')
df = pd.DataFrame(result,columns=result.keys())

html = df.to_html()

@app.route('/')
def home():
        return html

app.run(host='0.0.0.0')
