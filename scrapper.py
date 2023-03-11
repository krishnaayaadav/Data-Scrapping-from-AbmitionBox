import requests, time
from bs4 import BeautifulSoup
from csvfiles_hanlder import CSVHandlers


class CompanySraper:

    def __init__(self, target_url:str):
        self.url = target_url
    
    def get_soup_data(self,url=None):
        """This method will return beautiful soup object of requested page.
           Which is parsed as lxml ok.
        """

        if url is None:
            url = self.url 

        # user client headers
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
        
        # making request and getting response as html page
        try:
            web_page = requests.get(url = url, headers = headers)
        except:
            print('Error: While making request to targeted url')
        else:
            # data parsing using beautifulsoup
            soup     = BeautifulSoup(web_page.content, 'lxml') 
            return soup
    
    def soup_data_extractor(self,soup=None):
        """This method will scrapp company data and extract means make/find structured data"""

        if soup is None:
            soup = self.get_soup_data() 
        
        if soup is not None: # means soup having some data as html

            # getting all list of companies
            cards = soup.find('div', attrs={'id': 'cards-list'})
            companies = cards.find('div', attrs={'itemscope': 'itemscope'}).find_all('div', attrs={'itemprop': 'itemListElement', 'itemscope':"itemscope"})

            all_companies = [] # empty list to store all company
           
            company_labels = ['comp_name', 'comp_type','comp_headq', 'how_old','comp_no_emp', 'comp_review', 'open_jobs', 'comp_services','comp_logo', 'comp_description' ]

            
            for com in companies:
                # company name or title
                try:
                    title = com.find('h2', attrs='company-name bold-title-l').text.strip()
                except:
                    pass
                
                # company review
                try: 
                    review = com.find(attrs = {'class':"review-count sbold-Labels"}).text.strip()
                except:
                    pass
                
                # company logo image link hai
                try:
                    logo   = com.find('img')['data-src']
                except:
                    pass

                # company services
                try:
                    comp_service = com.find_all('a', attrs = {'class':"ab_chip body-medium"})
                except:
                    pass

                
                # company services

                try:
                    services = [srv.text.strip() for srv in comp_service]
                except:
                    pass

                
                # basic info
                try:
                    basic_info = com.find_all('p', attrs = {'class':"infoEntity sbold-list-header"})

                    if len(basic_info)>3:
                        types,headq, no_emp, old = [basic_info[info].text.strip() for info in range(len(basic_info)) ]
                    else:
                        types,headq, no_emp = [basic_info[info].text.strip() for info in range(len(basic_info)) ]
                except:
                    pass


                # company description here
                try:
                    desc = com.find('p', attrs={'class':"description body-small"})
                    if desc is not None:
                        desc = desc.text.strip()
                except:
                    pass


                # open jobs
                try:
                    jobs  = com.find('ul', attrs = {'class': "company-action-center"})
                    jobs = jobs.find_all(attrs= {'class':"caption-subdued-large"})[-1].text.strip()
                except:
                    pass


                # making company dict with all data

                
                try:
                    compDict = {
                    'comp_name':     title,
                    'comp_type':     types,
                    'comp_headq':    headq,
                    'how_old'   :    old,
                    'comp_no_emp':   no_emp,
                    'comp_review':   review,
                    'open_jobs'  :   jobs,
                    'comp_services': services,
                    'comp_logo'     : logo,
                    'comp_description': desc,


                   }
                except:
                    pass
                else:
                    # print(compDict)
                    all_companies.append(compDict)


                # comp_detail = [title, types, headq, old, no_emp, review, jobs, services, desc, logo]

                # all_companies.append(comp_detail)

           
            return company_labels,all_companies
    

def scrappe_pages(no_page:int):
    for i in range(1,no_page+1):
            
        URL = f'https://www.ambitionbox.com/list-of-companies?page={i}'
        c1 = CompanySraper(target_url=URL)
        keys, dictdata = c1.soup_data_extractor()  

        filename = 'top_companies_list.csv'
        mode = 'a'
        initial = False
        if i == 1:
            initial = True

        csv = CSVHandlers(filename=filename, mode=mode)
        csv.dict_csv_writer(keys=keys, dict_datas=dictdata, is_initial=initial)

scrappe_pages(33)


# filename = 'top_companies_list.csv'

# csv = CSVHandlers(filename=filename, mode='r')
# csv.dict_csv_reader()