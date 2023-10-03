url = 'https://statecontracts.nebraska.gov/Search'

import mechanize
import pandas as pd
import itertools
import requests
from bs4 import BeautifulSoup

alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
keywords = [''.join(i) for i in itertools.product(alphabets, repeat = 2)]

url = r'https://statecontracts.nebraska.gov/Search'
request = mechanize.Request(url)
response = mechanize.urlopen(request)
forms = mechanize.ParseResponse(response, backwards_compat=False)
response.close()

form = forms[0]

form['ctl00$ContentPlaceHolder1$MainContentControl1$ctl00$txtLastName']='Smith'
form['ctl00$ContentPlaceHolder1$MainContentControl1$ctl00$txtPostalCode']='K1H'

print mechanize.urlopen(form.click()).read()


br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

data = list()

for key in keywords[0:5]:
    
  br.open(url)
  response = br.response()
  br.select_form(nr=0)
  br.form['Status'] = ["Active"]
  br.form['Type'] = ["Higher Education"]
  br.form['Entity'] = ['University of Nebraska Lincoln-051-002']
  br.form['DocType'] = ["Contract"]
  br.form["Vendor"] = key
  
  #Submit the information  
  br.submit()
  
  #Open up comment page
  r= br.response().read()
  res = pd.read_html(r, extract_links = "body")
  df = res[0]
  # df["doc_url"] = [link.url for link in br.links(url_regex = "/Search/SearchDocuments")]
  if df.shape[0] == 26:
    print("Multiple pages!")
    nums = ["/SearchResults?page=" + i for i in df.iloc[25,0].split() if i.isdigit()]
    for i in nums:
      br.open(url+i)
      r2= br.response().read()
      res2 = pd.read_html(r2, extract_links = "body")
      df2 = res2[0]
      if "First|Last|Next|Prev" in df2["Doc Number"].iloc[-1]:
        df2 = df2.iloc[:-1,:]
      # df2["doc_url"] = [link.url for link in br.links(url_regex = "/Search/SearchDocuments")]
      data.append(df2)
  else: 
    data.append(df)


full_data = pd.concat(data)
full_data = full_data.apply(lambda col: [v[0] if v[1] is None else f'{base_url}{v[1]}' for v in  col])
