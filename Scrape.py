import mechanize
import pandas as pd
import itertools
import requests

alphabets = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
keywords = [''.join(i) for i in itertools.product(alphabets, repeat = 2)]

url = r'https://statecontracts.nebraska.gov/Search'

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

for key in keywords:
    
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
baseurl = r'https://statecontracts.nebraska.gov'
full_data["url"] = [pd.NA if pd.isna(i) else baseurl + i[1] for i in full_data["Doc Number"]]
full_data["Doc Number"] = [pd.NA if pd.isna(i) else i[0] for i in full_data["Doc Number"]]
full_data = full_data.loc[~full_data["Doc Number"].isin(["1", "F", "P", "N", "L"]),:]
full_data = full_data.loc[~pd.isna(full_data["Doc Number"])]
full_data["Type"] = [i[0] for i in full_data["Type"]]
full_data["Entity"] = [i[0] for i in full_data["Entity"]]
full_data["Entity Name"] = [i[0] for i in full_data["Entity Name"]]
full_data["Vendor"] = [i[0] for i in full_data["Vendor"]]
full_data["Amount"] = [i[0] for i in full_data["Amount"]]
full_data["Begin Date"] = [i[0] for i in full_data["Begin Date"]]
full_data["End Date"] = [i[0] for i in full_data["End Date"]]
full_data = full_data.drop_duplicates()
full_data.to_csv("Scraped_Contracts.csv")
