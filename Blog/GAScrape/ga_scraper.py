from bs4 import BeautifulSoup
import pandas as pd
import requests, json
import numpy as np
import matplotlib.pyplot as plt

#Function to scrape GA site
def scrape_ga(location):
    error_dict = {}
    #Prepares URL to be scraped http://www.pythonforbeginners.com/python-on-the-web/web-scraping-with-beautifulsoup/
    url = "https://generalassemb.ly/education?where=%s" % (location)
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')
    
    #Creates a list of dictionaries based on site's JSON. Data captured is event title, date, event format, url, city
    dataframe_list = []
    for item in soup.find_all("script"):
        if "window.EDUCATIONAL_OFFERINGS_JSON" in str(item):
            json_list = str(item).split(";\n")
            for item in json_list:
                if "window.EDUCATIONAL_OFFERINGS_JSON" in item:
                    try:
                        edu_offering_data = json.loads(item.split("= ",1)[1])
                        for item2 in edu_offering_data:
                            dataframe_list.append({"title":item2["title"], "date":item2["starts"], "format":item2["format"],"url":item2["url"],"location":location})
                    except:
                        error_dict[location] = item.split("= ",1)[1]
    
    #Plugs the list of dictionaries into a dataframe
    df = pd.DataFrame(dataframe_list)
    return df, error_dict

#Combines on dataframes into master dataframe
def create_master_df(location_list):
    list_of_dataframes = []
    dict_of_error_dicts = {}
    for loc in location_list:
        df, error_dict = scrape_ga(loc)
        list_of_dataframes.append(df)
        dict_of_error_dicts[loc] = error_dict
    master_df = pd.concat(list_of_dataframes).drop_duplicates(subset = ["date", "location", "url", "title"])
    master_df.to_csv("master_df.csv", encoding = "utf-8")
    return master_df, dict_of_error_dicts

#Plots bar chart of events by location http://matplotlib.org/examples/pylab_examples/barchart_demo.html
def barchart(index, count, title, xlabel, ylabel):
    fig, ax = plt.subplots()
    len_count = np.arange(len(count))
    bar_width = 0.80
    opacity = 0.4
    rects1 = plt.bar(len_count, count, bar_width, alpha=opacity)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title, fontweight = "bold")
    plt.xticks(len_count + bar_width/2, index, rotation = 90)
    plt.style.use('ggplot')
    plt.show()

location_list = ["atlanta", "washington-dc", "austin", "boston", "chicago", "denver", "los-angeles", "new-york-city", "providence", "san-francisco", "seattle", "london", "hong-kong", "singapore", "brisbane", "melbourne", "sydney"]
master_df, dict_of_errors = create_master_df(location_list)
barchart(master_df.location.value_counts().index, master_df.location.value_counts(),"SF's Most Happening: GA Events by Location","Location","Events")