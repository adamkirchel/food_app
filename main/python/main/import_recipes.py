import pandas as pd
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

url = "https://foodnetwork.co.uk"

def get_url(url):

    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None
        
def is_good_response(resp):

    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)
            
def log_error(e):

    print(e)
    
    
def get_recipe_urls(url):

    print(url)

    raw_html = get_url(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    div_list = html.find_all("div", class_="card recipepage")
    
    recipe_list = []
    
    for div in div_list:
        for a in div.select('a'):
            
            recipe_list.append(a['href'])
            
    return(recipe_list)
            
            
def get_category_urls(url):

    print(url)

    raw_html = get_url(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    div_list = html.find_all("ul", class_="secLvMenu")
    
    category_list = []
    
    for a in div_list[0].select('a'):
        
        category_list.append(a['href'])
            
    return(category_list)
    
def get_properties(url):

    print(url)

    raw_html = get_url(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    
    header = html.find_all("section", class_="article-head")
    
    title = header[0].select('h1')[0].text
    try:
        description = header[0].select('h2')[0].text
    except:
        description = 'N/A'
    
    recipe_head = html.find_all("ul", class_="recipe-head")
    
    prep_time = 'N/A'
    cooking_time = 'N/A'
    serves = 'N/A'
    difficulty = 'N/A'
    
    for li in recipe_head[0].select('li'):
        if li.select('span')[0].text == 'Preparation Time':
            prep_time = li.select('strong')[0].text
        elif li.select('span')[0].text == 'Cooking Time':
            cooking_time = li.select('strong')[0].text
        elif li.select('span')[0].text == 'Serves':
            serves = li.select('strong')[0].text
        elif li.select('span')[0].text == 'Difficulty':
            difficulty = li.select('strong')[0].text
        else:
            pass
            
    ingredients_tab = html.find_all("div", class_="recipe-tab-container")
    
    ingredients_dict = {}
    
    ingredients_list = []
    
    tag_type = type(ingredients_tab[0].find())
    
    key = 'All'    
    for tag in ingredients_tab[0].contents:
        
        if isinstance(tag, tag_type):
            
            if tag.name == 'h4':
                
                if len(ingredients_list) > 0:
                
                    ingredients_dict.update({key : ingredients_list})
                
                ingredients_list = []
                
                key = tag.text
                
                
            elif tag.name == 'div' and tag['class'][0] == 'ingredient':
            
                ingredients_list.append(tag.text)
                
        
    ingredients_dict.update({key : ingredients_list})
    
    method = html.find_all("div", class_="recipe-text")[0]
    
    image = html.find_all("picture")[0]
    image_link = image.find_all("img")[0]
    image_url = image_link['srcset']
    
    
    return {'Title':title,
            'Description':description,
            'Preparation time':prep_time,
            'Serves':serves,
            'Difficulty':difficulty,
            'Ingredients':ingredients_dict,
            'Method':method,
            'Image':image_url}
    
        
    
    
def full_parse(url):

    category_list = get_category_urls(url)
    
    url_list = []
    recipe_df = pd.DataFrame()
    
    for category in category_list:
    
        category_url = url + category
        
        recipe_urls = get_recipe_urls(category_url)
        print(recipe_urls)
        
        try:
            url_list = url_list + recipe_urls
        except:
            pass
    
        
    for recipe_url in url_list:
        
        recipe_url = url + recipe_url
        properties = get_properties(recipe_url)
        
        recipe_df = recipe_df.append(properties,
                                     ignore_index=True)
                                     
    
    return recipe_df   
    
    
   
recipe_df = full_parse(url)

print(recipe_df)  

recipe_df.to_csv("recipes_df.csv")

    
   