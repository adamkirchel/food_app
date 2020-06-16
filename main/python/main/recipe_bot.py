import pandas as pd
import nltk
nltk.download('popular')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import random
import json
import pickle
import os
from food_app.settings import PYTHON_DIR

#os.chdir(r"C:\Users\adsk1\Documents\Coding portfolio\food_app\main\python\main")

recipe_df = pd.read_csv(PYTHON_DIR + "recipes_df.csv")

#os.chdir(r"C:\Users\adsk1\Documents\Coding portfolio\food_app")

def title_training():

    if os.path.exists(PYTHON_DIR + "title_data.pickle"):
        with open(PYTHON_DIR + "title_data.pickle", "rb") as f:
            words, labels, training, output = pickle.load(f)

    else:
        
        words = []
        labels = []
        docs_x = []
        docs_y = []
        
        for recipe in recipe_df["Title"]:

            title = recipe
            
            tokenized_title = []
            
            for w in title:
            
                wrds = nltk.word_tokenize(title)
                words.extend(wrds)
                tokenized_title.extend(wrds)
                
            docs_x.append(tokenized_title)
            docs_y.append(recipe)  
            
            labels.append(recipe)

        words = [stemmer.stem(w.lower()) for w in words if w != "?"]
        words = sorted(list(set(words)))  

        training = []
        output = []
            
        out_empty = [0 for _ in range(len(labels))]

        for x, doc in enumerate(docs_x):
            
            bag = []
            
            wrds = [stemmer.stem(w.lower()) for w in doc]

            for w in words:
                if w in wrds:
                    bag.append(1)
                else:
                    bag.append(0)
                    
            output_row = out_empty[:]
            output_row[labels.index(docs_y[x])] = 1
            
            training.append(bag)
            output.append(output_row)
        
        
        training = numpy.array(training)
        output = numpy.array(output)
        
        with open(PYTHON_DIR + "title_data.pickle", "wb") as f:
            pickle.dump((words, labels, training, output), f)
            
    return words, labels, training, output

def ingredients_training():

    if os.path.exists(PYTHON_DIR + "title_data.pickle"):
        with open(PYTHON_DIR + "title_data.pickle", "rb") as f:
            words, labels, training, output = pickle.load(f)

    else:
        
        words = []
        labels = []
        docs_x = []
        docs_y = []
        
        for recipe in recipe_df["Title"]:

            ingredients_list = eval(recipe_df[recipe_df["Title"] == recipe]["Ingredients"].iloc[0])

            full_ingredients = list(ingredients_list.values())[0]
            
            tokenized_ingredients = []
            
            for ingredient in full_ingredients:
            
                wrds = nltk.word_tokenize(ingredient)
                words.extend(wrds)
                tokenized_ingredients.extend(wrds)
                
            docs_x.append(tokenized_ingredients)
            docs_y.append(recipe)  
            
            labels.append(recipe)

        words = [stemmer.stem(w.lower()) for w in words if w != "?"]
        words = sorted(list(set(words)))  

        training = []
        output = []
            
        out_empty = [0 for _ in range(len(labels))]

        for x, doc in enumerate(docs_x):
            
            bag = []
            
            wrds = [stemmer.stem(w.lower()) for w in doc]

            for w in words:
                if w in wrds:
                    bag.append(1)
                else:
                    bag.append(0)
                    
            output_row = out_empty[:]
            output_row[labels.index(docs_y[x])] = 1
            
            training.append(bag)
            output.append(output_row)
        
        
        training = numpy.array(training)
        output = numpy.array(output)
        
        with open(PYTHON_DIR + "data.pickle", "wb") as f:
            pickle.dump((words, labels, training, output), f)
            
    return words, labels, training, output

def bag_of_words(s,words):
    bag = [0 for _ in range(len(words))]
    
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
                
    return numpy.array(bag)
    
    


def find_recipe(inp):

    words, labels, training, output = ingredients_training()
    testing = bag_of_words(inp,words)
    recipes_mag = []
    i=0

    for set in training:
        try:
            testing_same = testing & set
            amount = sum(testing_same)
            
            i +=1
            recipes_mag.append(amount)
        except:
            pass
          
    list = sorted(enumerate(recipes_mag), key=lambda i: i[1])
    results_index = list[-15:-1]
    recipe_list = []
    image_list = []
        
    for n in results_index:
    
        index = n[0]
        sub_list = [labels[index],recipe_df["Image"][index]]
        recipe_list.append(sub_list)  
    
    return recipe_list
    
def find_recipe_types(inp):

    words, labels, training, output = title_training()
    
    testing = bag_of_words(inp,words)
    recipes_mag = []
    i=0

    for set in training:
        try:
            testing_same = testing & set
            amount = sum(testing_same)
            
            i +=1
            recipes_mag.append(amount)
        except:
            pass
          
    list = sorted(enumerate(recipes_mag), key=lambda i: i[1])
    results_index = list[-15:-1]
    recipe_list = []
   
    for n in results_index:
    
        index = n[0]
        sub_list = [labels[index],recipe_df["Image"][index]]
        recipe_list.append(sub_list)  
    
    return recipe_list
    
