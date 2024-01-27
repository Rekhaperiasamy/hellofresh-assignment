import requests
import json
import re
from hf_bi_python_exercise.Recipe import Recipe
from hf_bi_python_exercise.Csv import Csv


def filter_recipes(recipes, ingredients):
    filtered_recipes = []
    for recipe in recipes:
        if search(ingredients, recipe['ingredients']):
            recipe['difficulty'] = get_difficulty(
                recipe['cookTime'], recipe['prepTime'])

            filtered_recipes.append(recipe)

    return filtered_recipes


def get_difficulty(prepTime, cookTime):
    total_time = extract_time_in_minutes(prepTime + cookTime)
    if total_time > 60:
        return "Hard"

    if total_time < 60 and total_time > 30:
        return "Medium"

    if total_time < 30:
        return "Easy"

    return "Unknown"


def extract_time_in_minutes(time_string):
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


def search(words, my_string):
    found_words = [word for word in words if word in my_string]
    return found_words


def get_average_time_for_difficulty(recipes):
    hard_total = 0
    hard_count = 0

    medium_total = 0
    medium_count = 0

    easy_total = 0
    easy_count = 0

    for recipe in recipes:
        if recipe["difficulty"] == "Hard":
            hard_total += extract_time_in_minutes(
                recipe['cookTime'] + recipe['prepTime'])
            hard_count += 1
            continue

        if recipe["difficulty"] == "Medium":
            medium_total += extract_time_in_minutes(
                recipe['cookTime'] + recipe['prepTime'])
            medium_count += 1
            continue

        if recipe["difficulty"] == "Easy":
            easy_total += extract_time_in_minutes(
                recipe['cookTime'] + recipe['prepTime'])
            easy_count += 1
            continue

    hard_average = hard_total // hard_count
    medium_average = medium_total // medium_count
    easy_average = easy_total // easy_count

    return hard_average, medium_average, easy_average


def write_dict_to_csv(recipes, file_path, separator='|'):
    columns = list(recipes[0].keys())

    with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(
            csv_file, fieldnames=columns, delimiter=separator)

        csv_writer.writeheader()

        for row in recipes:
            cleaned_row = {key: value.replace(
                '\n', ' ') for key, value in row.items()}
            csv_writer.writerow(cleaned_row)


def write_rows_to_csv(data, file_path, separator='|'):
    with open(file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=separator)
        csv_writer.writerows(data)


def download_recipes_file():
    URL = "https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json"
    response = requests.get(URL)

    if response.status_code == 200:
        json_lines = response.text.strip().split('\n')
        data_list = [json.loads(line) for line in json_lines]
        return data_list
    else:
        raise "Failed to download JSON"


if __name__ == "__main__":
    recipe = Recipe()
    csv = Csv()

    data = recipe.download_recipes_file(
        "https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json")
    filtered_recipes = recipe.filter_recipes(data, ['Chilies', 'Chiles'])
    csv.write_dict_to_csv(filtered_recipes, "Chilies.csv", "|")

    hard_avg, medium_avg, easy_avg = recipe.get_average_time_for_difficulty(
        filtered_recipes)

    csv.write_list_to_csv(
        [
            ["HARD", "AverageTotalTime", hard_avg],
            ["MEDIUM", "AverageTotalTime", medium_avg],
            ["EASY", "AverageTotalTime", easy_avg]
        ],
        "Results.csv"
    )
