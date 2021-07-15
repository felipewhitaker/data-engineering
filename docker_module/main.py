import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://root:root@localhost/test_db")

df = pd.read_sql_query("SELECT * FROM happiness LIMIT 10", engine)

print(df.head())
