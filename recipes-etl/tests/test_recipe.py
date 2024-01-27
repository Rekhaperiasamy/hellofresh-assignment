import pytest
from mock import patch, Mock
from hf_bi_python_exercise.Recipe import Recipe


@pytest.fixture
def setup_data():
    recipes = [
        {"name": "Easter Leftover Sandwich", "ingredients": "12 whole Hard Boiled Eggs\n1/2 cup Mayonnaise\n3 Tablespoons Grainy Dijon Mustard\n Salt And Pepper, to taste\n Several Dashes Worcestershire Sauce\n Leftover Baked Ham, Sliced\n Kaiser Rolls Or Other Bread\n Extra Mayonnaise And Dijon, For Spreading\n Swiss Cheese Or Other Cheese Slices\n Thinly Sliced Red Onion\n Avocado Slices\n Sliced Tomatoes\n Lettuce, Spinach, Or Arugula",
            "url": "http://thepioneerwoman.com/cooking/2013/04/easter-leftover-sandwich/", "image": "http://static.thepioneerwoman.com/cooking/files/2013/03/leftoversandwich.jpg", "cookTime": "PT", "recipeYield": "8", "datePublished": "2013-04-01", "prepTime": "PT15M", "description": "Got leftover Easter eggs?    Got leftover Easter ham?    Got a hearty appetite?    Good! You've come to the right place!    I..."},
        {"name": "Pasta with Pesto Cream Sauce", "ingredients": "3 Egg 3/4 cups Fresh Basil Leaves\n1/2 cup Grated Parmesan Cheese\n3 Tablespoons Pine Nuts\n2 cloves Garlic, Peeled\n Salt And Pepper, to taste\n1/3 cup Extra Virgin Olive Oil\n1/2 cup Heavy Cream\n2 Tablespoons Butter\n1/4 cup Grated Parmesan (additional)\n12 ounces, weight Pasta (cavitappi, Fusili, Etc.)\n2 whole Tomatoes, Diced",
         "url": "http://thepioneerwoman.com/cooking/2011/06/pasta-with-pesto-cream-sauce/", "image": "http://static.thepioneerwoman.com/cooking/files/2011/06/pesto.jpg", "cookTime": "PT1H", "recipeYield": "8", "datePublished": "2011-06-06", "prepTime": "PT6M", "description": "I finally have basil in my garden. Basil I can use. This is a huge development.     I had no basil during the winter. None. G..."},
        {"name": "Herb Roasted Pork Tenderloin with Preserves", "ingredients": "2 whole Pork Tenderloins\n Salt And Pepper, to taste\n8 Tablespoons Herbs De Provence (more If Needed\n1 cup Preserves (fig, Peach, Plum)\n1 cup Water\n1 Tablespoon Vinegar", "url": "http://thepioneerwoman.com/cooking/2011/09/herb-roasted-pork-tenderloin-with-preserves/",
         "image": "http://static.thepioneerwoman.com/cooking/files/2011/09/porkloin.jpg", "cookTime": "PT15M", "recipeYield": "12", "datePublished": "2011-09-15", "prepTime": "PT5M", "description": "This was yummy. And easy. And pretty! And it took basically no time to make.     Before I share the recipe, I'll just say it:..."}
    ]

    setup_data = {
        "recipes": recipes,
        "recipes_jsonl": '{"name":"recipe1"}\n{"name":"recipe2"} \n{"name":"recipe3"}'
    }
    yield setup_data
    print("teardown")


class TestRecipe:
    def test_download_recipe_file(self, setup_data, mocker):
        mocker.patch(
            "hf_bi_python_exercise.Recipe.requests.get",
            return_value=Mock(
                status_code=200,
                text=setup_data['recipes_jsonl']
            )
        )

        recipe = Recipe()
        result = recipe.download_recipes_file('http://abc.com/file.json')

        assert result == [{"name": "recipe1"}, {
            "name": "recipe2"}, {"name": "recipe3"}]

    def test_is_ingredient_in_recipe(self):
        recipe = Recipe()
        found = recipe.is_ingredient_in_recipe(
            ["eggs", "egg"],
            "random text with eggs and 3 egg"
        )

        assert found == True

        found = recipe.is_ingredient_in_recipe(
            ["Chilies"],
            "1 whole Onion, Diced\n2 Tablespoons Butter\n1 can (15 Ounce) Green Enchilada Sauce\n2 cans (4 Ounce) Chopped Green Chilies\n12 whole Corn Tortillas\n2 cups Freshly Grated Cheddar (or Cheddar-jack) Cheese (or Any Cheese You'd Like)\n Sour Cream\n Salsa\n Pico De Gallo (optional)\n Guacamole (optional)\n Cilantro Leaves, Optional"
        )

        assert found == True

        found = recipe.is_ingredient_in_recipe(
            ["onion"],
            "random text with eggs and 3 egg"
        )

        assert found == False

        found = recipe.is_ingredient_in_recipe(
            ["Pepper"],
            "1 whole Onion, Diced\n2 Tablespoons Butter\n1 can (15 Ounce) Green Enchilada Sauce\n2 cans (4 Ounce) Chopped Green Chilies\n12 whole Corn Tortillas\n2 cups Freshly Grated Cheddar (or Cheddar-jack) Cheese (or Any Cheese You'd Like)\n Sour Cream\n Salsa\n Pico De Gallo (optional)\n Guacamole (optional)\n Cilantro Leaves, Optional"
        )

        assert found == False

    def test_get_difficulty(self):
        recipe = Recipe()
        assert recipe.get_difficulty("10M", "10M") == "Easy"
        assert recipe.get_difficulty("", "5M") == "Easy"
        assert recipe.get_difficulty("5M", "") == "Easy"

        assert recipe.get_difficulty("20M", "20M") == "Medium"
        assert recipe.get_difficulty("", "40M") == "Medium"
        assert recipe.get_difficulty("50M", "") == "Medium"

        assert recipe.get_difficulty("30M", "40M") == "Hard"
        assert recipe.get_difficulty("", "2H") == "Hard"
        assert recipe.get_difficulty("3H", "") == "Hard"
        assert recipe.get_difficulty("2H", "5M") == "Hard"

        assert recipe.get_difficulty("", "") == "Unknown"
        assert recipe.get_difficulty("random", "PT") == "Unknown"

    def test_filter_recipes(self, setup_data):
        recipe = Recipe()
        filtered_recipes = recipe.filter_recipes(
            setup_data['recipes'], ["Eggs", "Egg"])

        assert len(filtered_recipes) == 2

        assert 'difficulty' in filtered_recipes[0]
        assert 'difficulty' in filtered_recipes[1]

        assert filtered_recipes[0]['difficulty'] == 'Easy'
        assert filtered_recipes[1]['difficulty'] == 'Hard'

        filtered_recipes = recipe.filter_recipes(
            setup_data['recipes'], ["Eggs", "Egg", "Pepper"])

        assert len(filtered_recipes) == 3

        assert 'difficulty' in filtered_recipes[0]
        assert 'difficulty' in filtered_recipes[1]
        assert 'difficulty' in filtered_recipes[2]

        filtered_recipes = recipe.filter_recipes(
            setup_data['recipes'], ["Carrot", "Kathirika", "Inji"])

        assert len(filtered_recipes) == 0

    def test_get_average_time_for_difficulty(self, setup_data):
        recipe = Recipe()
        filtered_recipes = recipe.filter_recipes(
            setup_data['recipes'], ["Eggs", "Egg", "Pepper"])
        hard_average, medium_average, easy_average = recipe.get_average_time_for_difficulty(
            filtered_recipes)

        assert hard_average == 66
        assert medium_average == 0
        assert easy_average == 17

        filtered_recipes = recipe.filter_recipes(
            setup_data['recipes'], ["Carrot", "Kathirika", "Inji"])
        hard_average, medium_average, easy_average = recipe.get_average_time_for_difficulty(
            filtered_recipes)

        assert hard_average == 0
        assert medium_average == 0
        assert easy_average == 0
