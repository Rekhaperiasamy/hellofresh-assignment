import requests
import json
from hf_bi_python_exercise.Utils import Utils


class Recipe:

    def download_recipes_file(self, url):
        response = requests.get(url)

        if response.status_code == 200:
            json_lines = response.text.strip().split('\n')
            data_list = [json.loads(line) for line in json_lines]
            return data_list
        else:
            raise "Failed to download JSON"

    def filter_recipes(self, recipes, ingredients):
        filtered_recipes = []
        for recipe in recipes:
            if self.is_ingredient_in_recipe(ingredients, recipe['ingredients']):
                recipe['difficulty'] = self.get_difficulty(
                    recipe['cookTime'], recipe['prepTime'])

                filtered_recipes.append(recipe)

        return filtered_recipes

    def is_ingredient_in_recipe(self, words, my_string):
        found_words = [word for word in words if word in my_string]
        if found_words:
            return True
        return False

    def get_difficulty(self, prepTime, cookTime):
        total_time = Utils.extract_time_in_minutes(prepTime + cookTime)
        if total_time > 60:
            return "Hard"

        if total_time <= 60 and total_time >= 30:
            return "Medium"

        if total_time < 30 and total_time > 0:
            return "Easy"

        return "Unknown"

    def get_average_time_for_difficulty(self, recipes):
        hard_total = 0
        hard_count = 0
        hard_average = 0

        medium_total = 0
        medium_count = 0
        medium_average = 0

        easy_total = 0
        easy_count = 0
        easy_average = 0

        for recipe in recipes:
            if recipe["difficulty"] == "Hard":
                hard_total += Utils.extract_time_in_minutes(
                    recipe['cookTime'] + recipe['prepTime'])
                hard_count += 1
                continue

            if recipe["difficulty"] == "Medium":
                medium_total += Utils.extract_time_in_minutes(
                    recipe['cookTime'] + recipe['prepTime'])
                medium_count += 1
                continue

            if recipe["difficulty"] == "Easy":
                easy_total += Utils.extract_time_in_minutes(
                    recipe['cookTime'] + recipe['prepTime'])
                easy_count += 1
                continue

        if hard_total > 0:
            hard_average = hard_total // hard_count
        if medium_total > 0:
            medium_average = medium_total // medium_count
        if easy_total > 0:
            easy_average = easy_total // easy_count

        return hard_average, medium_average, easy_average
