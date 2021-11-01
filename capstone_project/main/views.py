import csv
import json
from django.shortcuts import render
import pandas as pd
import pandas_datareader as pdr
import os.path
from .forms import Company
from .models import StockData

# Create your views here.
def index(request):
    path = 'C:/Users/sehunKim/Desktop/Project/CapstonDesign/reference/companylist.csv'
    stock_path = 'C:/Users/sehunKim/Desktop/Project/CapstonDesign/capstone_project/main/data/'
    company_dataFrame = pd.read_csv(path)
    data = []
    count = 0
    data_min = 0
    data_max = 0
    company_name = ''

    if request.method == 'POST':
        form = Company(request.POST)

        if form.is_valid():
            company_name = form.cleaned_data['company_name']
            stock_code = getCompanyStockCode(company_dataFrame, company_name)

            dataFrame = pdr.get_data_yahoo(stock_code)

            if not os.path.isfile(stock_path + company_name + '.csv'):
                dataFrame.to_csv(stock_path + company_name + '.csv', encoding='utf-8-sig')

            stock_file = open(stock_path + company_name + '.csv')
            stock_data = csv.reader(stock_file)

            stockdata_list = []

            for row in stock_data:
                stockdata_list.append(StockData(
                    date = row[0],
                    value_high = row[1],
                    value_low = row[2],
                    value_market_open = row[3],
                    value_market_close = row[4],
                ))

                # 종가 데이터 수집 이후 chart.js로 보내야함
                if row[4] != 'Close':
                    data.append(row[4])

            data = list(map(float, data))
            data_max = max(data)
            data_min = min(data)

            StockData.objects.bulk_create(stockdata_list)
    else:
        form = Company()

    return render(request, 'capstone_project/index.html', {
        'form': form,
        'data': data,
        'max': data_max,
        'min': data_min,
    })

def getCompanyStockCode(dataframe, company_name):
    code = dataframe.query("name == '{}'".format(company_name))['code'].to_string(index=False)
    code = code.strip()
    return code
