import sqlite3 as sq
import pandas as pd
   
connection = sq.connect('data.db')

curs = connection.cursor()

curs.execute("create table if not exists consumer" +
             "(TicketID INTEGER PRIMARY KEY , Form TEXT NOT NULL, Method TEXT NOT NULL, Issue TEXT NOT NULL, City TEXT NOT NULL, State TEXT NOT NULL, Zip INTEGER)")

student = pd.read_csv('sdata.csv')

student.to_sql('consumer', connection, if_exists='replace', index=False)

curs.execute('select * from consumer')
 
records = curs.fetchall()

for row in records:
    print(row)
     
connection.close()