from django.shortcuts import render
from .forms import Company
from .models import StockData
from datetime import datetime, timedelta
import pandas as pd
import pandas_datareader as pdr
import os.path
import csv

# Create your views here.
def index(request):
    path = 'C:/Users/sehunKim/Desktop/Project/CapstonDesign/reference/companylist.csv'
    stock_path = 'C:/Users/sehunKim/Desktop/Project/CapstonDesign/capstone_project/main/data/'
    company_dataFrame = pd.read_csv(path)
    data = []
    date = []
    date_list = []
    data_min = 0
    data_max = 0
    today = datetime.today().date()
    company_name = ''
    data_duration = ''

    if request.method == 'POST':
        form = Company(request.POST)

        if form.is_valid():
            company_name = form.cleaned_data['company_name_text']
            data_duration = form.cleaned_data['duration_option']
            stock_code = getCompanyStockCode(company_dataFrame, company_name)

            # 데이터 크롤링 기간 설정
            option = today - timedelta(int(data_duration))
            option_weight = 1
            data_duration_flag = False

            # 주가 정보 크롤링
            dataFrame = pdr.get_data_yahoo(stock_code)

            # 만약 해당 주가 정보 파일(csv)가 존재하지 않을 경우에 csv 파일 생성 및 저장 이후 해당 파일을 불러옴으로서 로딩 시간 단축
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
                date_list.append(row[0])

            stock_file.close()

            # 주식장이 주말 또는 공휴일일 경우를 대비한 날짜 수정
            while str(option) not in date_list:
                option = today - timedelta(int(data_duration) + option_weight)
                option_weight += 1

            stock_file = open(stock_path + company_name + '.csv')
            stock_data = csv.reader(stock_file)

            # 수정된 날자를 바탕으로 해당 날자부터 데이터를 저장
            for row in stock_data:
                if row[0] == str(option):
                    data_duration_flag = True

                if data_duration_flag:
                    data.append(row[4])
                    date.append(row[0])

            stock_file.close()

            data = list(map(float, data))
            data_max = max(data) + 1000
            data_min = min(data) - 5000

            StockData.objects.bulk_create(stockdata_list)
    else:
        form = Company()

    return render(request, 'capstone_project/index.html', {
        'form': form,
        'data': data,
        'label': date,
        'max': data_max,
        'min': data_min,
    })

def getCompanyStockCode(dataframe, company_name):
    code = dataframe.query("name == '{}'".format(company_name))['code'].to_string(index=False)
    code = code.strip()
    return code
