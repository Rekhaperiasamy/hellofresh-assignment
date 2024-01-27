import requests
import json
import re


class Recipe:

    def download_recipes_file(self, url):
        """
        Download recipes data from the specified URL and return recipes as a list of dictionaries.

        Parameters:
        - url (str): The URL from which to download the recipes data.

        Returns:
        - list: A list of dictionaries representing the recipes data.

        Raises:
        - Exception: If the HTTP request fails or the response status code is not 200,
        an exception is raised with the message "Failed to download JSON".
        """
        response = requests.get(url)

        if response.status_code == 200:
            json_lines = response.text.strip().split('\n')
            data_list = [json.loads(line) for line in json_lines]
            return data_list
        else:
            raise "Failed to download JSON"

    def filter_recipes(self, recipes, ingredients):
        """
        Filter a list of recipes based on specified ingredients.
        Also adds 'difficulty' to the recipe based on the prep time and cook time

        Parameters:
        - recipes (list): A list of dictionaries representing recipes.
        - ingredients (list): A list of ingredients to filter recipes.

        Returns:
        - list: A filtered list of dictionaries containing recipes that contains the specified ingredients.
        """
        filtered_recipes = []
        for recipe in recipes:
            if self.is_ingredient_in_recipe(ingredients, recipe['ingredients']):
                recipe['difficulty'] = self.get_difficulty(
                    recipe['cookTime'], recipe['prepTime'])

                filtered_recipes.append(recipe)

        return filtered_recipes

    def is_ingredient_in_recipe(self, ingredients, recipe):
        """
        Takes a list of words and a string and tries to find if atleast one of the words present in the string

        Parameters:
        - ingredients (list): A list of words representing ingredients.
        - recipe (str): A string that contains all ingredients of a recipe

        Returns:
        - Boolean: True if at least one of the words present in the string else False
        """
        found_words = [word for word in ingredients if word in recipe]
        if found_words:
            return True
        return False

    def get_difficulty(self, prepTime, cookTime):
        total_time = self.extract_time_in_minutes(prepTime + cookTime)
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
                hard_total += self.extract_time_in_minutes(
                    recipe['cookTime'] + recipe['prepTime'])
                hard_count += 1
                continue

            if recipe["difficulty"] == "Medium":
                medium_total += self.extract_time_in_minutes(
                    recipe['cookTime'] + recipe['prepTime'])
                medium_count += 1
                continue

            if recipe["difficulty"] == "Easy":
                easy_total += self.extract_time_in_minutes(
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

    def extract_time_in_minutes(self, time_string):
        time_pattern = re.compile(r'(\d+)([HM])')

        total_minutes = 0

        matches = time_pattern.findall(time_string)

        for value, unit in matches:
            value = int(value)
            if unit == 'H':
                total_minutes += value * 60
            elif unit == 'M':
                total_minutes += value

        return total_minutes
