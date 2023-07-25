import requests
from datetime import datetime, timedelta


api_key = 'qJdjK7G77DZMcVA2tZzZfA(('
base_url = 'https://api.stackexchange.com/2.3/'


def get_top_trending_tags():

    monthsByNo = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
    today = datetime.today()
    start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_date = (today.replace(day=28, hour=23, minute=59, second=59, microsecond=999) + timedelta(days=4)).replace(day=1)
    print("start Date :",start_date,"\nEnd Date :",end_date)
    url = f'{base_url}tags'
    params = {
        'site': 'stackoverflow',
        'key': api_key,
        'fromdate': int(start_date.timestamp()),
        'todate': int(end_date.timestamp()),
        'order': 'desc',
        'sort': 'popular',
    }

    response = requests.get(url, params=params)
    data = response.json()
    monthName = monthsByNo[today.month]
    dataToReturn = []
    for item in data['items']:
        dataToReturn.append({"month":monthName,"tag":item['name'],"count":item['count']})

    return dataToReturn

def get_most_common_languages_tagged_this_year(year):

    languages = ["python","c++","java","javascript","c#","ruby","php","swift","kotlin","go","typescript","rust","r","scala","perl","objective-c","dart","lua","haskell"]
    base_url = "https://api.stackexchange.com/2.3/questions"
    site = "stackoverflow"
    order = "desc"
    sort = "votes"
    pagesize = 50
    fromdate = int(datetime.datetime(year, 1, 1).timestamp())
    todate = int(datetime.datetime(year, 12, 31).timestamp())

    query_params = {
        "site": site,
        "order": order,
        "sort": sort,
        "pagesize": pagesize,
        "fromdate": fromdate,
        "todate": todate,
        "tagged": ""
    }

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Encoding": "gzip",
        "Authorization": f"Bearer {api_key}"
    }

    dataToRetrun = {}
    for lang in languages:
        query_params["tagged"] = lang


        response = requests.get(base_url, params=query_params, headers=headers)
        data = response.json()

        if "items" in data:
            dataToRetrun[lang] = 0
            for item in data["items"]:
                for tag in item["tags"]:
                    if tag.startswith(lang):
                        dataToRetrun[lang] += 1
        else:
            print("Error: Unable to fetch data from Stack Overflow API.")
    
    return dataToRetrun