# Generated by Django 3.0.6 on 2020-06-02 12:25

from django.db import migrations
import pandas as pd
import os
from main.models import recipes

path = r"C:\Users\adsk1\Documents\Coding portfolio\food_app\main\python\main\\"

os.chdir(path)

recipe_df = pd.read_csv("recipes_df.csv")

os.chdir(r"C:\Users\adsk1\Documents\Coding portfolio\food_app")


def recipe_data(apps, schema_editor):

    #recipes = apps.get_model('main', 'recipes')
    
    entries = []
    
    for t in recipe_df['Title']:
    
        print(t)

        entries.append(recipes(title = recipe_df[recipe_df['Title'] == t]['Title'].iloc[0],
                               description = recipe_df[recipe_df['Title'] == t]['Description'].iloc[0],
                               preparation_time = recipe_df[recipe_df['Title'] == t]['Preparation time'].iloc[0],
                               serves = recipe_df[recipe_df['Title'] == t]['Serves'].iloc[0],
                               difficulty = recipe_df[recipe_df['Title'] == t]['Difficulty'].iloc[0],
                               ingredients = recipe_df[recipe_df['Title'] == t]['Ingredients'].iloc[0],
                               method = recipe_df[recipe_df['Title'] == t]['Method'].iloc[0],
                               image_url = recipe_df[recipe_df['Title'] == t]['Image'].iloc[0]))
        
        
    recipes.objects.bulk_create(entries)
    


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(recipe_data),
    ]