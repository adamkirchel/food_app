from nltk.stem.lancaster import LancasterStemmer
from main.models import recipes
stemmer = LancasterStemmer()


def shopping_basket(larderItems,Event):
    
    ingredients_list = []
    decision_list = []
    ingredients_list_stemmed = []
    shopping_list = []
    
    recipe_list = [d['title'] for d in list(Event.objects.values('title'))]

    for recipe in recipe_list:
        
        x = eval(list(recipes.objects.filter(title = recipe).values('ingredients'))[0]['ingredients'])
        
        ingredients = []
        
        for key in x.keys():
            
            ingredients.extend(x[key])

        ingredients_list.extend(ingredients)

        # remove repeats
        
    for ingredient in ingredients_list:
        ingredient = ingredient.replace(',','')
        phrase = ingredient.split(' ')
        phrase_list = [stemmer.stem(w.lower()) for w in phrase]
        ingredients_list_stemmed.append(phrase_list)

    larder_list = [d['item'] for d in list(larderItems.objects.values('item'))]

    larder_list_stemmed = [stemmer.stem(w.lower()) for w in larder_list]
    
    print(len(ingredients_list))
    print(len(ingredients_list_stemmed))

    for i,ingredient in enumerate(ingredients_list_stemmed):
        
        for sub_ingredient in ingredient:
            if sub_ingredient in larder_list_stemmed:
                
                break
        
            elif sub_ingredient == ingredient[-1]:
                shopping_list.append(ingredients_list[i]);
                
            else:
            
                pass

                

    return shopping_list
                
                
                
    
