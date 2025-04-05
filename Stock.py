!pip install yfinance
!pip install bs4
!pip install nbformat
!pip install --upgrade plotly

import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
pio.renderers.default = "iframe"
import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        subplot_titles=("Historical Share Price", "Historical Revenue"), 
        vertical_spacing=0.3
    )

    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']

    fig.add_trace(go.Scatter(
        x=pd.to_datetime(stock_data_specific.Date), 
        y=stock_data_specific.Close.astype("float"), 
        name="Share Price"
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=pd.to_datetime(revenue_data_specific.Date), 
        y=revenue_data_specific.Revenue.astype("float"), 
        name="Revenue"
    ), row=2, col=1)

    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)

    fig.update_layout(
        showlegend=False,
        height=900,
        title=stock,
        xaxis_rangeslider_visible=True
    )

    fig.show()


tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max")
tesla_data.reset_index(inplace=True)
print(tesla_data.head())


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
html_data = requests.get(url).text
soup = BeautifulSoup(html_data, "html.parser")
tesla_table = soup.find_all("tbody")[1]
tesla_dates = []
tesla_revenues = []

for row in tesla_table.find_all("tr"):
    columns = row.find_all("td")
    if len(columns) > 1:
        date = columns[0].text.strip()
        revenue = columns[1].text.strip()
        tesla_dates.append(date)
        tesla_revenues.append(revenue)

tesla_revenue = pd.DataFrame({
    "Date": tesla_dates,
    "Revenue": tesla_revenues
})


tesla_revenue["Revenue"] = tesla_revenue["Revenue"].astype(str)

tesla_revenue["Revenue"] = tesla_revenue["Revenue"].str.replace(',|\$', '', regex=True)

tesla_revenue = tesla_revenue[tesla_revenue["Revenue"] != ""]
tesla_revenue.dropna(inplace=True)

tesla_revenue["Revenue"] = tesla_revenue["Revenue"].astype(float)

tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

print(tesla_revenue.tail())


gme = yf.Ticker("GME")
gme_data = gme.history(period="max")
gme_data.reset_index(inplace=True)
print(gme_data.head())


url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data_2 = requests.get(url).text
soup = BeautifulSoup(html_data_2, "html.parser")
gme_table = soup.find_all("tbody")[1]
gme_dates = []
gme_revenues = []

for row in gme_table.find_all("tr"):
    cols = row.find_all("td")
    if len(cols) > 1:
        date = cols[0].text.strip()
        revenue = cols[1].text.strip()
        gme_dates.append(date)
        gme_revenues.append(revenue)

gme_revenue = pd.DataFrame({
    "Date": gme_dates,
    "Revenue": gme_revenues
})

gme_revenue["Revenue"] = gme_revenue["Revenue"].str.replace(',|\$', "", regex=True)

gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue["Revenue"] != ""]
print(gme_revenue.tail())


make_graph(tesla_data, tesla_revenue, 'Tesla')
make_graph(gme_data, gme_revenue, 'GameStop')
