import fake_headers
import lxml
import requests
import bs4
import re 
import json


headers_gen = fake_headers.Headers(browser='chrome', os='win')
responce = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers= headers_gen.generate())
main_html_data = responce.text
soup = bs4.BeautifulSoup(main_html_data, 'lxml')
main_tag = soup.find('main', class_="vacancy-serp-content")
vacancy_list = main_tag.find_all('div', class_ = 'serp-item')
vacancy_data_list = []
for vacancy in vacancy_list:
    a_tag = vacancy.find('a', class_ = 'serp-item__title')
    link = a_tag['href']
    responce_keywords = requests.get(link.strip(), headers= headers_gen.generate())
    html_data_keywords = responce_keywords.text
    soup_data_about_vacancy = bs4.BeautifulSoup(html_data_keywords, 'lxml')
    keywords_tag = soup_data_about_vacancy.find_all('span', class_ = 'bloko-tag__section bloko-tag__section_text')
    list_of_tags = []
    salary_data = soup_data_about_vacancy.find('div', class_ = 'vacancy-title').find('span', class_ = 'bloko-header-section-2 bloko-header-section-2_lite')
    if salary_data == None:
        salary_data = 'Не указано'
    else:
        salary_data = salary_data.get_text()
    
    name_data = soup_data_about_vacancy.find('div', class_ = 'vacancy-company-details').find('span', class_ = 'bloko-header-section-2 bloko-header-section-2_lite')
    name_data = name_data.get_text()
    
    vacancy_lacation = soup_data_about_vacancy.find('div', class_ = 'vacancy-company-redesigned').find('p')
    if vacancy_lacation == None:
        vacancy_lacation = 'Не указано'
    else:
        vacancy_lacation = vacancy_lacation.get_text()
    

   
    for keyword_text in keywords_tag:
        main_text = keyword_text.get_text()
        list_of_tags.append(main_text)
        

 
    def availability_check_1 (list_of_tags):
        for item in list_of_tags:
            if re.search(r"\bDjango\b", item):
                return True
            
            
        
    def availability_check_2 (list_of_tags):
        for item in list_of_tags:
            if re.search(r"\bGit\b", item):
                return True
                
    
    
    if availability_check_1 (list_of_tags) == True and availability_check_2 (list_of_tags) == True:
        vacancy_data_list.append({
            'Ссылка на вакансию' : link,
            'Зарплата' : salary_data,
            'Название компании' : name_data,
            'Город' : vacancy_lacation
        })
        
        

# print (vacancy_data_list)

with open('vacancy_data.json', 'a', encoding= 'utf-8') as file:
    json.dump(vacancy_data_list, file, indent=4, ensure_ascii=False)
    
# print(vacancy_list)
