import requests
from lxml import html
from lxml import etree

import plotly.plotly as py
from plotly.graph_objs import *

import datetime

def chunks(l, n):
    n = max(1, n)
    return [l[i:i + n] for i in range(0, len(l), n)]

def get_data(list,pos):
	return_list = [ item[pos] for item in list]
	return return_list[1:]

def get_dates_data(list):
	return get_data(list,0)

def get_energydemand_data(list):
	return get_data(list,1)

def get_energysupply_data(list):
	return get_data(list,2)

def get_genco_data(list):
	return get_data(list,6)

def get_centralsupply_data(list):
	return get_data(list,7)

def get_others_data(list):
	return get_data(list,9)

def get_apgenco_data(list):
	return get_data(list,10)

def get_grandtotal_data(list):
	return get_data(list,11)

def get_data_from_tstransco_website():

	govt_base_url = "http://59.144.72.4:8080/tsreports/jsp/formatoneahistory.htm?state=TG"

	to_day = datetime.date.today().strftime("%d-%m-%Y")
	from_day = (datetime.date.today() + datetime.timedelta(days=-7)).strftime("%d-%m-%Y")

	payload = "&option=default&reportdate1="+from_day+"&reportdate2="+to_day+"&generate=Show"

	page = requests.get(govt_base_url+payload)

	tree = html.fromstring(page.content)
	td_data = [td.text for td in tree.xpath("//td")]

	is_not_thing = lambda x: x is not None
	cleaned_data = filter(is_not_thing, td_data)

	formatted_data=[]
	formatted_data.append(chunks(cleaned_data,15))

	return formatted_data[0]

def plot_graph():
	raw_data = get_data_from_tstransco_website()
	x_data = get_dates_data(raw_data)

	strace1 = Bar(
    	x=x_data,
    	y=get_genco_data(raw_data),
    	name='TS Genco(MU)'
	)
	
	strace2 = Bar(
    	x=x_data,
    	y=get_centralsupply_data(raw_data),
    	name='Central Power(MU)'
	)

	strace3 = Bar(
    	x=x_data,
    	y=get_apgenco_data(raw_data),
    	name='AP Genco(MU)'
	)

	strace4 = Bar(
    	x=x_data,
    	y=get_others_data(raw_data),
    	name='Others(MU)'
	)

	strace5 = Bar(
    	x=x_data,
    	y=get_energysupply_data(raw_data),
    	name='Total Supply(MU)'
	)

	dtrace1 = Bar(
    	x=x_data,
    	y=get_energydemand_data(raw_data),
    	name='Electricy Demand(MU)'
	)

	data = Data([strace1, strace2, strace3, strace4, strace5, dtrace1 ])
	layout = Layout(
    	barmode='stacked'
	)


	fig = Figure(data=data, layout=layout)
	plot_url = py.plot(fig, filename='Telangana State Electricy Demand Supply')


if __name__ == "__main__":
	plot_graph()
