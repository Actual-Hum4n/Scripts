#!/usr/bin/python3

"""
Why does this exist:
To find the well known 16Shop Phishing pages easier. Get these sites shut down quicker.

TODO:
*better way to determine if site is 16shop or not(check for specific 16shop files?)
*pretty sure I can declutter this..
*option to create new output.txt or use pre-existing one.
"""
#python imports
import requests
import objectpath

#startup
print('Gathering possible Apple phishing sites')
url = 'https://urlscan.io/api/v1/search/'
params = dict(
	q = 'PhishTank OR OpenPhish OR CertStream-Suspicious',
	size = '1000')
response = requests.get(url=url, params=params).json()

#parsing the json for domain values
results_tree = objectpath.Tree(response['results'])
domain_search = tuple(results_tree.execute('$..domain'))

#searching if any apple related words in domain, if so print
#add more search keys
with open('Output.txt' , 'w') as file:
	for i in domain_search:
		if ('apple') in i:
			file.write(i + '\n')
		elif ('icloud') in i:
			file.write(i + '\n')
print('Done, domains in Output.txt')

#checking if domain is registered with 16Shop C2
print('Checking domains against known 16Shop C2s')
bad_actor = []
with open('Output.txt') as domains:
	lines = [line.rstrip() for line in domains]
	shopUrl = 'http://128.199.154.155/api/setting/get_setting.php'
	for domainz in lines:
		shopParams = dict(
			domain = domainz)
		shopResponse = requests.post(url=shopUrl, data=shopParams).json()
		if shopResponse['email_result'] is None:
			print(domainz + " is null")
		else:
			print(shopResponse['email_result'] + " " + domainz)
		
