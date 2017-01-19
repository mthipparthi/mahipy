import  requests
from lxml import html
from lxml import etree
import re
import threading

BASE_URL = "http://agmarknet.nic.in/agnew/NationalBEnglish/comm_market_dist.aspx"
file_lock = threading.Lock()

def form_a_list(market_price_data):
    prev = 0
    list_of_m_c=[]
    range_length = len(market_price_data)//8 + 1
    for i in range(1, range_length):
        list_of_m_c.append(market_price_data[ prev : prev+8])
        prev = i*8+i
    return list_of_m_c

def process_by_district_commodity(district, commodity):

    payload = {'state1': 'TL', 'district1': str(district), 'commodity1':str(commodity)}
    resp = requests.get(BASE_URL, payload)

    if resp.ok :
        tree = html.fromstring(resp.text)

        state = ""
        category = ""
        date = ""

        date_txt = [el.text for el in tree.xpath('//*[@id="lblTitle"]/center')]
        if len(date_txt):
            match = re.search("(\d+/\d+/\d+)", date_txt[0])
            if match:
                date= match.group(1)


        state_commodity_data = [el.text for el in tree.xpath('//table/tr/td/font/b')]
        if len(state_commodity_data) > 3:
            state = state_commodity_data[3]
            category = state_commodity_data[2]

        market_price_data = [el.text for el in tree.xpath('//*[@id="GridView1"]/tr/td/font')]
        if len(market_price_data): 
            district = market_price_data[3] if len(market_price_data) > 3 else None
            
            for i in form_a_list(market_price_data[4:]):
                if len(i) > 7:
                    market_center = i[0]
                    arrivals = i[1]
                    unit_of_arrivals = i[2]
                    variety = i[3]
                    minimum_price = i[4] 
                    maximum_price = i[5] 
                    modal_price =i[6]
                    unit_of_rice = i[7]

                    with file_lock, open("./market_data.csv", 'a+') as f:
                        print(state,category,date,district,market_center,arrivals,unit_of_arrivals,variety,minimum_price,maximum_price,modal_price,unit_of_rice, sep=",", file=f)

def process_by_district(district):
    for commodity in range(1,17):
        process_by_district_commodity(district, commodity)

if __name__ == "__main__":
    dts = [3,4,5,6,7,8,10,11]
    threads = []
    for dt_code in dts:
        t = threading.Thread(target=process_by_district,args=(dt_code,))
        threads.append(t)
        t.start()
