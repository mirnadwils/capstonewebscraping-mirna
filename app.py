from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url = 'https://www.coingecko.com/en/coins/ethereum/historical_data/?start_date=2020-01-01&end_date=2021-06-30' #masukkan link url
url_get = requests.get(url, headers = { 'User-Agent': 'Popular browser\'s user-agent', }) 
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('tbody')
Data = table.find_all('th', attrs={'class':'font-semibold text-center'})

row_length = len(Data)

temp = [] #initiating a list 

for table in soup.find_all('tr')[1:]:

    #Scrapping Date 
    date = table.find_all('th', attrs={'class':'font-semibold text-center'})
    dates = date[0].text

    #Scrapping Volume
    volum = table.find_all('td')
    volume = volum[1].text.strip()
    
    temp.append((dates,volume)) #gabungkan hasil scrapping date dan volume
    
temp

#change into dataframe
df = pd.DataFrame(temp, columns = ('date','volume'))

#insert data wrangling here
df['volume'] = df['volume'].str.replace(",","") #hapus koma dari data volume
df['volume'] = df['volume'].str.replace("$","") #hapus '$' dari data volume
df['volume'] = df['volume'].astype('float64') #ubah tipe data volume dari object menjadi float
df['date'] = df['date'].astype('datetime64') #ubah tipe data date dari object menjadi datetime
df = df.set_index('date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df["volume"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = df.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)