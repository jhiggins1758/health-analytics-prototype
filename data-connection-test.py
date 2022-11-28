import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=hackathon.spdns.org;'
                      'Database=GlobalHealth;'
                      'Trusted_Connection=no;'
                      'uid=ServiceStreamlit;'
                      'pwd=Hack1234;')

cursor = conn.cursor()
cursor.execute('SELECT * FROM Data.HealthAnalytics')

for i in cursor:
    print(i)