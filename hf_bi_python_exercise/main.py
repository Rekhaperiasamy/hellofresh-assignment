from src.Recipe import Recipe
from src.Csv import Csv

if __name__ == "__main__":
    recipe = Recipe()
    csv = Csv()

    URL = "https://bnlf-tests.s3.eu-central-1.amazonaws.com/recipes.json"
    RESULTS_DIR = "recipes-etl"

    data = recipe.download_recipes_file(URL)
    filtered_recipes = recipe.filter_recipes(data, ['Chilies', 'Chiles'])
    csv.write_dict_to_csv(filtered_recipes, RESULTS_DIR + "/Chilies.csv", "|")

    hard_avg, medium_avg, easy_avg = recipe.get_average_time_for_difficulty(
        filtered_recipes)
    csv.write_list_to_csv(
        [
            ["HARD", "AverageTotalTime", hard_avg],
            ["MEDIUM", "AverageTotalTime", medium_avg],
            ["EASY", "AverageTotalTime", easy_avg]
        ],
        RESULTS_DIR + "/Results.csv",
        "|"
    )
