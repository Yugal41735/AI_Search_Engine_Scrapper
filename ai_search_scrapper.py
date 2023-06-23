pip install pytrends

from datetime import datetime
import requests
import json
import html.parser
import time
import socket
from pytrends.request import TrendReq
import plotly.express as px
import streamlit as st

global counter
counter = 1


def search_data(inp):

    today_date = datetime.today().strftime("%Y-%m-%d")
    one_yr_bef = today_date[:2] + str(int(today_date[2:4])-1) + today_date[4:]

    class HTMLTextExtractor(html.parser.HTMLParser):
        def __init__(self):
            super(HTMLTextExtractor, self).__init__()
            self.result = [ ]

        def handle_data(self, d):
            self.result.append(d)

        def get_text(self):
            return ''.join(self.result)

    def html_to_text(html):

        s = HTMLTextExtractor()
        s.feed(html)
        return s.get_text()

    query_list = ['how','what','when','where','are', 'is', 'why', 'can']
    search_query = inp
    search_query_list = []
    for i in query_list:
        search_query_list.append(i+" "+search_query)
    for i in range(97,ord('z')+1):
        search_query_list.append(search_query + ' ' + chr(i))
    #print(search_query_list)

    # Dyanamic country code and language could be implemented
    language = "en"
    country_code ="IN"
    ###############################
    client = "gws-wiz"
    authuser = 0
    params = {
        'q':search_query_list[4],
        'cp':3,
        'client':client,
        'hl':"{0}-{1}".format(language, country_code),
        'authuser':0,
        'dpr':1,
        }
    headers = {
        'authority': 'ogs.google.com',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Chrome OS"',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 14388.52.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.91 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'x-chrome-connected': 'source=Chrome,mode=0,enable_account_consistency=true,supervised=false,consistency_enabled_by_default=false',
        'x-client-data': 'CJG2yQEIprbJAQipncoBCJbpygEIt6DLAQiTocsBCOvyywEInvnLAQiljswBCIGkzAE=',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-dest': 'iframe',
        'referer': 'https://www.google.com/',
        'accept-language': 'en-US,en;q=0.9',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'SID=KgipsdC3Yxa9m7JCFiSf9ERCriYX3tio-sdln7YpWH15A05EkNn3lzEaOxsxKB_j73HZ8Q.; __Secure-1PSID=KgipsdC3Yxa9m7JCFiSf9ERCriYX3tio-sdln7YpWH15A05EDjjIiujZe5PuNwI0jKTIUQ.; __Secure-3PSID=KgipsdC3Yxa9m7JCFiSf9ERCriYX3tio-sdln7YpWH15A05EgV9PEOK8KcjRZ-uQ-V6-3A.; HSID=A4EPy3YgwJXM51l6-; SSID=Ay5kAM2fDjIkfmpCX; APISID=Akv6x6eGTTq5dDC0/AMwo4EQGB5jsZRP11; SAPISID=Xdgah6CYZtLA1H0L/AlykPZRaBrmcFhebU; __Secure-1PAPISID=Xdgah6CYZtLA1H0L/AlykPZRaBrmcFhebU; __Secure-3PAPISID=Xdgah6CYZtLA1H0L/AlykPZRaBrmcFhebU; OTZ=6519179_34_34__34_; SEARCH_SAMESITE=CgQIwZUB; 1P_JAR=2022-05-25-06; NID=511=Vl8RZrmSnFRPwPAlCvStF4RZ5FRWrRCOngQ0jhVt8Lw5f-p8a-PyCbT_XdrJERuW932YfBn2AWGB6D_Msimu6gIBgM0eI47WAtWtHAiz6A3E3WoU8AaiRhsUlw3K9VBHTkS-DEXd6AEU96t60oe-ZIj9A9XVT1WKKIUdAsmHY5qhgRuqwst2Yif6s98aIFy8vMaoZ3K6rgU6hQCFbBU06M-hgy-ByRuvhph2V79vJBWXeT9Rcbh__pRmGnfv3K8Bh2oYngp2inVqlNxgxdqaFOvsrJWpFWIuC9JFJkCEAg; OGPC=19022519-1:; AEC=AakniGO1bomcWh2W_Hjby5dk15zIQE-zegTw55ljJQPb_rcF9eh_q2bycyM; SIDCC=AJi4QfHXY7354Db5dHXtuotnTXiDpiZeT500CGU_-gH7aV4aUGXrj6lieYU4l6U2tvWfhMWShA; __Secure-3PSIDCC=AJi4QfHU6C6zb0AcfqPm0l553V_uOB4y_wjFuhXD24na1ABfq53RoHU4_h1gW3rOAw0WAYzt6g',
        }

    resp = requests.get("https://www.google.com/complete/search", params = params, headers=headers)


    # Loop implemented to avoid multiple iteration for every query

    for query_index in range(len(search_query_list)):
        params = {
            'q':search_query_list[query_index],
            'cp':3,
            'client':client,
            'hl':"{0}-{1}".format(language, country_code),
            'authuser':0,
            'dpr':1,
            }
        resp = requests.get("https://www.google.com/complete/search", params = params, headers=headers, timeout = 5)
        from posixpath import sep
        json_suggestions1 = resp.text.replace("window.google.ac.h(", "")
        json_suggestions1 =  json_suggestions1[:-1]
        try:
            final_tuple = json.loads(html_to_text(json_suggestions1.encode('ascii').decode('unicode-escape')))
        except:
            pass
        #print(final_tuple)

        if(query_index == 0):
            f = open("myfile.txt", "w")
        else:
            f = open("myfile.txt", "a")
        #print(final_tuple[0][0][0])
        #print(len(final_tuple[0]))

        list_of_outs = []

        for val in final_tuple[0]:
            no_of_vals = len(val)
            for n in range(no_of_vals):
                req_val = final_tuple[0][n][0]
                list_of_outs += [req_val]

        #print(list_of_outs)
        for values in list_of_outs:
            sp_val = values.split(' </b>')
            new = ' '.join(sp_val)
            if(new[-4:] != '</b>'):
                list_of_outs[list_of_outs.index(values)] = new
            else:
                list_of_outs[list_of_outs.index(values)] = new[:-4]

        list_of_outs = list(set(list_of_outs))
        list_of_outs.sort()

        ind = 0


        #list_of_outs[0][:len(search_query_list[query_index])]==search_query_list[query_index]

        qer = ' '.join(search_query_list[query_index].split(inp)).strip()


        if(len(list_of_outs) > 0):
            if(len(qer)>1):
                if(qer in list_of_outs[0]):
                    st.write('**' + search_query_list[query_index] + '**')
                    #print('\n'+search_query_list[query_index]+'\n')
                    for out in list_of_outs:
                        if(out != search_query_list[query_index]):
                            st.write(''.join(out.split('</b>')))
                            #print(''.join(out.split('</b>')))
                        else:
                            pass
                else:
                    st.write('**' + search_query_list[query_index] + '**')
                    st.write('*' + 'NO RESULTS FOUND' + '*')
                    #print('\n'+search_query_list[query_index]+'\n')
                    #print('NO RESULTS FOUND')
            else:
                to_ch = list_of_outs[0].split(inp)[-1].strip()
                try:
                    if(to_ch[0] == qer):
                        st.write('**' + search_query_list[query_index] + '**')
                        #print('\n'+search_query_list[query_index]+'\n')
                        for out in list_of_outs:
                            st.write(''.join(out.split('</b>')))
                            #print(''.join(out.split('</b>')))
                    else:
                        st.write('**' + search_query_list[query_index] + '**')
                        st.write('*' + 'NO RESULTS FOUND' + '*')
                        #print('\n' + search_query_list[query_index] + '\n')
                        #print('NO RESULTS FOUND')
                except:
                    pass


def trends_data(inp):

    global counter
    counter += 1

    if(counter == 800):

        crt = datetime.now().strftime("%H:%M")
        req_crt = int(crt[:2])*60 + int(crt[3:])
        if(req_crt < req_time):
            counter = 0
            req_time = req_crt
        else:
            if((req_crt - req_time)//60 <3.5):
                time.sleep(150)
                req_time = req_crt
                counter = 1
            else:
                counter = 400
                req_time = req_crt

    # connect to google

    from pytrends.request import TrendReq

    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    time.sleep(5)

    try:
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), retries = 2, backoff_factor=0.1)

    except:
        pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25),proxies=['https://'+IPAddr,'https://34.203.233.13:80','https://35.201.123.31:880','https://174.70.1.210','https://139.162.252.174','https://204.2.218.145','https://130.41.101.105','https://85.92.119.65'], retries=3, backoff_factor=0.1, requests_args={'verify':False})


    kw_list = [inp] # list of keywords to get data

    pytrends.build_payload(kw_list, cat=0, timeframe='today 12-m')
    try:
        data_for_related_topics = pytrends.related_topics()
        rising_title = list(data_for_related_topics[inp]['rising']['topic_title'])
        rising_type = list(data_for_related_topics[inp]['rising']['topic_type'])

        #print("\n\nRelated Topic Titles And Types With Rising Interest\n\n")
        st.write("**Related Topic Titles And Types With Rising Interest**")

        for i in range(len(rising_title)):
            #print(rising_title[i] + ' - ' + rising_type[i])
            st.write(rising_title[i] + ' - ' + rising_type[i])

        top_title = list(data_for_related_topics[inp]['top']['topic_title'])
        top_type = list(data_for_related_topics[inp]['top']['topic_type'])

        #print('\n\nTop Searched Related Topic Titles and Types\n\n')
        st.write('**Top Searched Related Topic Titles and Types**')

        for i in range(len(top_title)):
            #print(top_title[i] + ' - ' + top_type[i])
            st.write(top_title[i] + ' - ' + top_type[i])
    except:
        pass

    try:
        data_for_related_queries = pytrends.related_queries()
        rising_query = list(data_for_related_queries[inp]['rising']['query'])
        rising_query_val = list(data_for_related_queries[inp]['rising']['value'])

        #print("\n\nRelated Queries With Rising Interest And Their Search Values\n\n")
        st.write("**Related Queries With Rising Interest And Their Search Values**")

        for i in range(len(rising_query)):
            #print(rising_query[i] + ' - ' + str(rising_query_val[i]))
            st.write(rising_query[i] + ' - ' + str(rising_query_val[i]))

        top_query = list(data_for_related_queries[inp]['top']['query'])
        top_query_val = list(data_for_related_queries[inp]['top']['value'])

        #print('\n\nTop Searched Related Queries And Search Values\n\n')
        st.write('**Top Searched Related Queries And Search Values**')

        for i in range(len(top_query)):
            #print(top_query[i] + ' - ' + str(top_query_val[i]))
            st.write(top_query[i] + ' - ' + str(top_query_val[i]))

        #print('\n\n')

    except:
        pass

    data = pytrends.interest_over_time()
    data = data.reset_index()

    import plotly.express as px

    fig = px.line(data, x="date", y=inp, title='Keyword Web Search Interest Over Time')
    fig.update_traces(line_color = 'magenta')
    st.write(fig)


input_val = st.text_input('Keyword to search (in lower case)','')

col1, col2 = st.columns(2)

with col1:
    if st.button('Search Data'):
        try:
            search_data(input_val.lower())
        except:
            st.write("**Unusually high traffic !!! Please try again in some time. Sorry for inconvenience**")

with col2:
    if st.button('Trends Data'):
        trends_data(input_val.lower())
