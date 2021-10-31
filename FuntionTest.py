import pandas as pd
import pandas_datareader as pdr
from matplotlib import pyplot as plt

stock_type = {
    'kospi': 'stockMkt',
    'kosdaq': 'kosdaqMkt'
}

# 회사 이름을 이용하여 해당 회사의 주식 종목 코드를 받을 수 있는 함수
def getStockCode(dataFrame, name):
    code = dataFrame.query("name == '{}'".format(name))['code'].to_string(index=False)
    code = code.strip()
    return code

# download url 조합
def getDownloadStock(market_type = None):
    market_type = stock_type[market_type]
    download_link = 'http://kind.krx.co.kr/corpgeneral/corpList.do'
    download_link = download_link + '?method=download'
    download_link = download_link + '&marketType=' + market_type

    dataframe = pd.read_html(download_link, header=0)[0]

    return dataframe

def getDownloadKospi():
    dataframe = getDownloadStock('kospi')
    dataframe = dataframe.rename(columns={'회사명': 'name', '종목코드': 'code'}) # colum attribute 이름 수정

    dataframe.code = dataframe.code.map('{:06d}.KS'.format)

    return dataframe

def getDownloadKosdaq():
    dataframe = getDownloadStock('kosdaq')
    dataframe = dataframe.rename(columns={'회사명': 'name', '종목코드': 'code'}) # colum attribute 이름 수정

    dataframe.code = dataframe.code.map('{:06d}.KQ'.format)

    return dataframe

kospi_dataframe = getDownloadKospi()
kosdaq_dataframe = getDownloadKosdaq()

code_dataframe = pd.concat([kospi_dataframe, kosdaq_dataframe])
code_dataframe = code_dataframe[['name', 'code']]

# 입력 스트링
company_input = input()
data_start = input()
data_end = input()

code = getStockCode(code_dataframe, company_input)

# 해당 회사의 주가 데이터
df = pdr.get_data_yahoo(code, start=data_start, end=data_end)

# graph 출력단
df['Close'].plot()
plt.show()