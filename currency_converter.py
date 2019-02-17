from bs4 import BeautifulSoup
import requests
import re
from decimal import Decimal


def convert(amount, cur_from, cur_to, date):
	"""
	To that function you should transfer amount of value that you have, name of the currency that you have and name of the currency that you want to transfer
	to (according to the abbreviations of Central Bank of Russian Federation API) and, finally, the date for which you want to get the calclulation. This function can help you to get accurate calculationfor your daily tasks
	
	"""
	page = requests.get('http://www.cbr.ru/scripts/XML_daily.asp', params = {
'date_req':date
})
	soup = BeautifulSoup(page.content, 'xml')
	if cur_from=="RUR":
		nominal_from, value_from = '1', '1'
	else:
		value_from = soup.find('CharCode', text=cur_from).find_next_sibling('Value').string
		nominal_from = soup.find('CharCode', text=cur_from).find_next_sibling('Nominal').string
	if cur_to=="RUR":
		nominal_from, value_from='1', '1'
	else:
		value_to = soup.find('CharCode', text=cur_to).find_next_sibling('Value').string
		nominal_to = soup.find('CharCode', text=cur_to).find_next_sibling('Nominal').string
	value_from = re.sub(',', '.', value_from)
	value_to = re.sub(',', '.', value_to)
	price_from = Decimal(value_from)/Decimal(nominal_from)
	price_to = Decimal(value_to)/Decimal(nominal_to)
	money_rur = Decimal(price_from)*Decimal(amount)
	money_cur_to = money_rur/price_to
	return money_cur_to.quantize(Decimal("0.0001"))