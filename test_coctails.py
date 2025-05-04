import unittest, csv,os
from coctails import (Ingredients, Alcohol, Syrups, Juice, Garnish, Component,
IngredientFactory, AlcoholFactory, SyrupsFactory, JuiceFactory, GarnishFactory, ComponentFactory,
Inventory, Coctail, CoctailDecorator, DiscountedCoctail)
from io import StringIO
from coctails import create_ingredient_from_csv, create_cocktail_from_csv,read_cocktails_from_csv,write_cocktail_to_csv


class TestAlcohol(unittest.TestCase):

    def setUp(self):
        self.ingredient = Alcohol("Vodka", 40, 2.5, strength=40, substitutes=["Tequila", "Rum"] ,amount_needed=1)  

    def test_get_name(self):
        self.assertEqual(self.ingredient.get_name(), "Vodka")

    def test_get_amount(self):
        self.assertEqual(self.ingredient.get_amount(), 40)

    def test_get_price_per_unit(self):
        self.assertEqual(self.ingredient.get_price_per_unit(), 2.5)

    def test_get_substitutes(self):
        self.assertEqual(self.ingredient.get_substitutes(), ["Tequila", "Rum"])

    def test_get_substitute_found(self):
        inventory = ["Tequila", "Vodka"]
        self.assertEqual(self.ingredient.get_substitute(inventory), "Tequila")

    def test_get_substitute_not_found(self):
        inventory = ["Gin", "Vodka"]
        self.assertIsNone(self.ingredient.get_substitute(inventory))

    def test_show_info(self):
        self.assertEqual(self.ingredient.show_info(), "Vodka (Alcohol, 40% , 40ml, 2.50Eur)")  

    def test_get_amount_needed(self):
        self.assertEqual(self.ingredient.get_amount_needed(), 1)



class TestSyrups(unittest.TestCase):   
        
    def setUp(self):
        self.syrup = Syrups("Strawberry Syrup", 50, 3.5, ["Fruit"], amount_needed=1)

    def test_get_name(self):
        self.assertEqual(self.syrup.get_name(), "Strawberry Syrup")
    
    def test_get_amount(self):
        self.assertEqual(self.syrup.get_amount(), 50)
    
    def test_get_price_per_unit(self):
        self.assertEqual(self.syrup.get_price_per_unit(), 3.5)
    
    def test_get_substitutes(self):
        self.assertEqual(self.syrup.get_substitutes(), ["Fruit"])


    def test_get_substitute_found(self):
        inventory = ["Honey", "Fruit"]
        self.assertEqual(self.syrup.get_substitute(inventory), "Fruit")

    def test_get_substitute_not_found(self):
        inventory = ["Honey"]
        self.assertIsNone(self.syrup.get_substitute(inventory))
    
    def test_show_info(self):
        expected_info = "Strawberry Syrup (Syrup 50ml, 3.50Eur)"
        self.assertEqual(self.syrup.show_info(), expected_info)

    def test_get_amount_needed(self):
        self.assertEqual(self.syrup.get_amount_needed(), 1)



class TestJuice(unittest.TestCase):

    def setUp(self):
        self.juice = Juice("Apple Juice", 250, 1.8, organic=True, type="Apple", substitutes=["Pear Juice"], amount_needed=1)

    def test_get_name(self):
        self.assertEqual(self.juice.get_name(), "Apple Juice")

    def test_get_amount(self):
        self.assertEqual(self.juice.get_amount(), 250)

    def test_get_price_per_unit(self):
        self.assertEqual(self.juice.get_price_per_unit(), 1.8)

    def test_get_substitutes(self):
        self.assertEqual(self.juice.get_substitutes(), ["Pear Juice"])

    def test_get_substitute_found(self):
        inventory = ["Pear Juice", "Orange Juice"]
        self.assertEqual(self.juice.get_substitute(inventory), "Pear Juice")

    def test_get_substitute_not_found(self):
        inventory = ["Orange Juice"]
        self.assertIsNone(self.juice.get_substitute(inventory))

    def test_show_info(self):
        expected = "Apple Juice (Juice organic , 250ml, 1.80Eur,Apple)"
        self.assertEqual(self.juice.show_info(), expected)

    def test_get_amount_needed(self):
        self.assertEqual(self.juice.get_amount_needed(), 1)




class TestGarnish(unittest.TestCase):

    def setUp(self):
        self.garnish = Garnish("Mint", 5, 0.5, "Leaves", substitutes=["Basil"], amount_needed=1)

    def test_get_name(self):
        self.assertEqual(self.garnish.get_name(), "Mint")

    def test_get_amount(self):
        self.assertEqual(self.garnish.get_amount(), 5)

    def test_get_price_per_unit(self):
        self.assertEqual(self.garnish.get_price_per_unit(), 0.5)

    def test_get_substitutes(self):
        self.assertEqual(self.garnish.get_substitutes(), ["Basil"])

    def test_get_substitute_found(self):
        inventory = ["Parsley", "Basil"]
        self.assertEqual(self.garnish.get_substitute(inventory), "Basil")

    def test_get_substitute_not_found(self):
        inventory = ["Parsley"]
        self.assertIsNone(self.garnish.get_substitute(inventory))

    def test_show_info(self):
        expected = "Mint (Garnish Leaves , 5g, 0.50Eur)"
        self.assertEqual(self.garnish.show_info(), expected)

    def test_get_amount_needed(self):
        self.assertEqual(self.garnish.get_amount_needed(), 1)



class TestComponent(unittest.TestCase):

    def setUp(self):
        self.component = Component("Sugar", 10, 0.2, substitutes=["Honey"], amount_needed=1)

    def test_get_name(self):
        self.assertEqual(self.component.get_name(), "Sugar")

    def test_get_amount(self):
        self.assertEqual(self.component.get_amount(), 10)

    def test_get_price_per_unit(self):
        self.assertEqual(self.component.get_price_per_unit(), 0.2)

    def test_get_substitutes(self):
        self.assertEqual(self.component.get_substitutes(), ["Honey"])

    def test_get_substitute_found(self):
        inventory = ["Honey", "Maple Syrup"]
        self.assertEqual(self.component.get_substitute(inventory), "Honey")

    def test_get_substitute_not_found(self):
        inventory = ["Salt"]
        self.assertIsNone(self.component.get_substitute(inventory))

    def test_show_info(self):
        expected = "Sugar (Component 10g, 0.20Eur)"
        self.assertEqual(self.component.show_info(), expected)

    def test_get_amount_needed(self):
        self.assertEqual(self.component.get_amount_needed(), 1)



class TestFactories(unittest.TestCase):

    def test_alcohol_factory(self):
        factory = AlcoholFactory()
        alcohol = factory.create(name="Rum", amount=50, price_per_unit=2.0, substitutes=["Vodka"], strength=40)
        self.assertIsInstance(alcohol, Alcohol)
        self.assertEqual(alcohol.get_name(), "Rum")
        self.assertEqual(alcohol.get_amount(), 50)
        self.assertEqual(alcohol.get_price_per_unit(), 2.0)
        self.assertEqual(alcohol.get_substitutes(), ["Vodka"])
        self.assertEqual(alcohol.show_info(), "Rum (Alcohol, 40% , 50ml, 2.00Eur)")

    def test_syrups_factory(self):
        factory = SyrupsFactory()
        syrup = factory.create(name="Vanilla Syrup", amount=30, price_per_unit=1.2, substitutes=["Caramel Syrup"])
        self.assertIsInstance(syrup, Syrups)
        self.assertEqual(syrup.get_name(), "Vanilla Syrup")

    def test_juice_factory(self):
        factory = JuiceFactory()
        juice = factory.create(name="Orange Juice", amount=200, price_per_unit=1.5, type="Citrus", organic=False, substitutes=["Lemon Juice"])
        self.assertIsInstance(juice, Juice)
        self.assertEqual(juice._type, "Citrus")
        self.assertFalse(juice._organic)

    def test_garnish_factory(self):
        factory = GarnishFactory()
        garnish = factory.create(name="Lime Slice", amount=5, price_per_unit=0.4, type="Citrus", substitutes=["Lemon Slice"])
        self.assertIsInstance(garnish, Garnish)
        self.assertEqual(garnish._type, "Citrus")

    def test_component_factory(self):
        factory = ComponentFactory()
        component = factory.create(name="Salt", amount=2, price_per_unit=0.1, substitutes=["Sugar"])
        self.assertIsInstance(component, Component)
        self.assertEqual(component.get_name(), "Salt")

    def test_is_subclass_of_ingredient_factory(self):
        self.assertTrue(issubclass(AlcoholFactory, IngredientFactory))
        self.assertTrue(issubclass(SyrupsFactory, IngredientFactory))
        self.assertTrue(issubclass(JuiceFactory, IngredientFactory))
        self.assertTrue(issubclass(GarnishFactory, IngredientFactory))
        self.assertTrue(issubclass(ComponentFactory, IngredientFactory))



class TestInventory(unittest.TestCase):

    def setUp(self):
        inv = Inventory()
        inv._Inventory__items.clear()

    def test_singleton_instance(self):
        inv1 = Inventory()
        inv2 = Inventory()
        self.assertIs(inv1, inv2)

    def test_add_ingredient(self):
        inv = Inventory()
        ingredient = Alcohol("Vodka", 50, 2.5, substitutes=["Rum"], strength=40)
        inv.add(ingredient)
        items = inv.get_inventory_items()
        self.assertIn(ingredient, items)
        self.assertEqual(len(items), 1)

    def test_inventory_persists_across_instances(self):
        inv1 = Inventory()
        ingredient1 = Alcohol("Gin", 30, 2.0, substitutes=["Vodka"], strength=38)
        inv1.add(ingredient1)

        inv2 = Inventory()
        ingredient2 = Alcohol("Tequila", 40, 3.0, substitutes=["Mezcal"], strength=45)
        inv2.add(ingredient2)

        items = inv1.get_inventory_items()
        self.assertIn(ingredient1, items)
        self.assertIn(ingredient2, items)
        self.assertEqual(len(items), 2)

    def test_get_inventory_items_returns_list(self):
        inv = Inventory()
        self.assertIsInstance(inv.get_inventory_items(), list)

    def test_clear_inventory_between_tests(self):
        inv = Inventory()
        self.assertEqual(len(inv.get_inventory_items()), 0)



class TestCoctail(unittest.TestCase):

    def setUp(self):
      
        self.rum = Alcohol("Rum", 40, 5, substitutes=["Vodka"], amount_needed=2)  # Rum, reikia 2
        self.sugar_syrup = Syrups("Sugar Syrup", 20, 1, substitutes=["Honey Syrup"], amount_needed=1)
        self.lime_juice = Juice("Lime Juice", 40, 1, True, "Citrus", substitutes=["Lemon Juice"], amount_needed=1)
        self.mineral_water = Component("Mineral Water", 100, 0.5, substitutes=["Tonic"], amount_needed=2)
        self.mint = Garnish("Mint", 5, 0.1, "leaves", amount_needed=1)

        self.aperol_liquer = Alcohol("Aperol Liquer", 40, 15, substitutes=["Campari Vermouth"], amount_needed=2)
        self.prosecco = Syrups("Prosecco", 30, 1, substitutes=["Champagne"], amount_needed=1)
        self.mineral_water = Component("Mineral Water", 100, 0.5, substitutes=["Tonic"], amount_needed=2)
        self.orange = Garnish("Orange", 0.5, 10, "slices", amount_needed=1) 
        self.campari_vermouth = Alcohol("Campari Vermouth", 40, 15, substitutes=["Aperol"], amount_needed=2) 

   
        self.mojito = Coctail("Mojito", [self.rum, self.sugar_syrup, self.lime_juice, self.mineral_water, self.mint])
        self.aperol_spritz=Coctail("Aperol Spritz", [self.aperol_liquer,self.prosecco,self.mineral_water,self.orange])
        self.campari_spritz=Coctail("Campari Spritz", [self.campari_vermouth,self.prosecco,self.mineral_water,self.orange])

    def test_get_total_price(self):
        inventory = ["Rum", "Sugar Syrup", "Lime Juice", "Mineral Water", "Mint"]
        self.assertEqual(self.mojito.get_total_price(inventory), 13.1)  

    def test_get_total_price_with_substitutes(self):
        inventory = ["Vodka", "Honey Syrup", "Lime Juice", "Tonic", "Mint"]
        self.assertEqual(self.mojito.get_total_price(inventory), 13.1)  

    def test_is_makeable_with_all_ingredients(self):
        inventory = ["Rum", "Sugar Syrup", "Lime Juice", "Mineral Water", "Mint"]
        self.assertEqual(self.mojito.is_makeable(inventory), "The Mojito can be made with the available ingredients")

    def test_is_makeable_with_missing_ingredient(self):
        inventory = ["Vodka", "Sugar Syrup", "Lime Juice", "Mineral Water", "Mint"]
        self.assertEqual(self.mojito.is_makeable(inventory), "The Mojito can be made with the available ingredients")


    def test_substitute_changes_name(self):
        inventory = ["Campari_Vermouth", "Prosecco", "Mineral_Water", "Orange", "Olive", "Tonic"]
        aperol_spritz = Coctail("Aperol Spritz", [self.aperol_liquer, self.prosecco, self.mineral_water, self.orange])
        self.assertEqual(aperol_spritz.is_makeable(inventory), "The Campari Spritz can be made with the available ingredients")

    def test_substitute_for_missing_ingredient(self):
        inventory = ["Aperol_Liquer", "Prosecco", "Tonic", "Orange", "Olive"]
        aperol_spritz = Coctail("Aperol Spritz", [self.aperol_liquer, self.prosecco, self.mineral_water, self.orange])
        self.assertEqual(aperol_spritz.is_makeable(inventory), "The Aperol Spritz can be made with the available ingredients")

    def test_invalid_substitute(self):
        inventory = ["Tequila", "Honey Syrup", "Lime Juice", "Tonic", "Mint"]
        mojito = Coctail("Mojito", [self.rum, self.sugar_syrup, self.lime_juice, self.mineral_water, self.mint])
        self.assertEqual(mojito.is_makeable(inventory), "cannot make Mojito, missing Rum")

    def test_get_substitute(self):
        inventory = ["Vodka", "Honey Syrup", "Lime Juice", "Mineral Water", "Tonic"]
        self.assertEqual(self.rum.get_substitute(inventory), "Vodka")  

    def test_get_price_per_unit(self):
        self.assertEqual(self.rum.get_price_per_unit(), 5)  

    def test_show_info(self):
        self.assertEqual(self.rum.show_info(), "Rum (Alcohol, 0% , 40ml, 5.00Eur)")  

    def test_missing_ingredients(self):
        inventory = ["Campari_Vermouth", "Prosecco", "Mineral_Water", "Orange", "Olive", "Tonic"]
        
        result = self.aperol_spritz.missing_ingredients(inventory)
        self.assertEqual(result, "Missing ingredients Aperol Liquer")

def test_show_recipe(self):
    inventory = ["Vodka", "Honey Syrup", "Lemon Juice", "Tonic", "Mint"]
    recipe = self.mojito.show_recipe()
    expected_recipe = "Mojito\nRum: 2 x 5.00 Eur\nSugar Syrup: 1 x 20.00 Eur\nLime Juice: 1 x 40.00 Eur\nMineral Water: 2 x 0.50 Eur\nMint: 1 x 5.00 Eur\n61.50 Eur"
    self.assertEqual(recipe, expected_recipe)

    def test_get_substitutes_for_missing(self):
        inventory = ["Vodka", "Honey Syrup", "Lemon Juice", "Tonic", "Mint"]
        substitutes = self.mojito.get_substitutes_for_missing(inventory)
        self.assertEqual(substitutes, {"Rum": "Vodka", "Sugar Syrup": "Honey Syrup", "Lime Juice": "Lemon Juice", "Mineral Water": "Tonic"})


    def test_get_name(self):
        result = self.aperol_spritz.get_name()
        self.assertEqual(result, "Aperol Spritz")
    
    def test_get_ingredients(self):
        result = self.aperol_spritz.get_ingredients()
        self.assertEqual(result, [self.aperol_liquer, self.prosecco, self.mineral_water, self.orange])



class TestCoctailDecorator(unittest.TestCase):

    def setUp(self):
        self.rum = Alcohol("Rum", 40, 5, substitutes=["Vodka"], amount_needed=2)
        self.sugar_syrup = Syrups("Sugar Syrup", 20, 1, substitutes=["Honey Syrup"], amount_needed=1)
        self.lime_juice = Juice("Lime Juice", 40, 1, True, "Citrus", substitutes=["Lemon Juice"], amount_needed=1)
        self.mineral_water = Component("Mineral Water", 100, 0.5, substitutes=["Tonic"], amount_needed=2)
        self.mint = Garnish("Mint", 5, 0.1, "leaves", amount_needed=1)
        
        self.mojito = Coctail("Mojito", [self.rum, self.sugar_syrup, self.lime_juice, self.mineral_water, self.mint])

    def test_show_recipe_decorator(self):
        decorated_mojito = CoctailDecorator(self.mojito)
        
        expected_recipe = "Mojito\nRum: 2 x 5.00 Eur\nSugar Syrup: 1 x 1.00 Eur\nLime Juice: 1 x 1.00 Eur\nMineral Water: 2 x 0.50 Eur\nMint: 1 x 0.10 Eur\n13.10 Eur"
        self.assertEqual(decorated_mojito.show_recipe(), expected_recipe)

    def test_total_price_decorator(self):
        decorated_mojito = CoctailDecorator(self.mojito)
        self.assertEqual(decorated_mojito.get_total_price(), self.mojito.get_total_price())



class TestDiscountedCoctail(unittest.TestCase):
    
    def setUp(self):
        self.rum = Alcohol("Rum", 40, 5, substitutes=["Vodka"], amount_needed=2)
        self.sugar_syrup = Syrups("Sugar Syrup", 1, 20, substitutes=["Honey Syrup"], amount_needed=1)
        self.lime_juice = Juice("Lime Juice", 1, 40, True, "Citrus", substitutes=["Lemon Juice"], amount_needed=1)
        self.mineral_water = Component("Mineral Water", 0.5, 100, substitutes=["Tonic"], amount_needed=2)
        self.mint = Garnish("Mint", 0.1, 5, "leaves", amount_needed=1)
        
        self.mojito = Coctail("Mojito", [self.rum, self.sugar_syrup, self.lime_juice, self.mineral_water, self.mint])

    def test_get_total_price_with_discount(self):
        discounted_mojito = DiscountedCoctail(self.mojito, 0.2)
        expected_price = self.mojito.get_total_price() * (1 - 0.2)
        self.assertAlmostEqual(discounted_mojito.get_total_price(), expected_price, places=2)

    def test_show_info_with_discount(self):
        discounted_mojito = DiscountedCoctail(self.mojito, 0.2)
        
        expected_recipe = self.mojito.show_recipe()  
        self.assertEqual(discounted_mojito.show_info(), expected_recipe)

class TestCreateIngredientFromCSV(unittest.TestCase):

    def setUp(self):
        self.csv_data = """Mojito,Alcohol,Rum,40,5,40%,"Vodka",1
Mojito,Syrups,Sugar Syrup,20,1,,"Honey Syrup",1
Mojito,Juice,Lime Juice,40,1,True,"Lemon Juice",1
Mojito,Component,Mineral Water,100,0.5,,"Tonic, Sprite",1
Mojito,Garnish,Mint,1,0.1,leaves,,1
"""
        self.csv_file = StringIO(self.csv_data)
        self.csv_reader = csv.reader(self.csv_file)

    def test_create_ingredient_from_csv(self):
        for row in self.csv_reader:
            ingredient = create_ingredient_from_csv(row)
        
            ingredient_type = row[1].strip()

            if ingredient_type == "Alcohol":
                self.assertIsInstance(ingredient, Alcohol)
                self.assertEqual(ingredient._name, "Rum")
                self.assertEqual(ingredient._amount, 40)
                self.assertEqual(ingredient._price_per_unit, 5)
                self.assertEqual(ingredient._strength, 40)
                self.assertEqual(ingredient._substitutes, ['Vodka']) 
                self.assertEqual(ingredient._amount_needed,1)

            elif ingredient_type == "Syrups":
                self.assertIsInstance(ingredient, Syrups)
                self.assertEqual(ingredient._name, "Sugar Syrup")
                self.assertEqual(ingredient._amount, 20)
                self.assertEqual(ingredient._price_per_unit, 1)
                self.assertEqual(ingredient._substitutes, ["Honey Syrup"])
                self.assertEqual(ingredient._amount_needed,1)

            elif ingredient_type == "Juice":
                self.assertIsInstance(ingredient, Juice)
                self.assertEqual(ingredient._name, "Lime Juice")
                self.assertEqual(ingredient._amount, 40)
                self.assertEqual(ingredient._price_per_unit, 1)
                self.assertTrue(ingredient._organic)
                self.assertEqual(ingredient._substitutes, ['Lemon Juice'])
                self.assertEqual(ingredient._amount_needed,1)

            elif ingredient_type == "Component":
                self.assertIsInstance(ingredient, Component)
                self.assertEqual(ingredient._name, "Mineral Water")
                self.assertEqual(ingredient._amount, 100)
                self.assertEqual(ingredient._price_per_unit, 0.5)
                self.assertEqual(ingredient._substitutes, ['Tonic', 'Sprite'])
                self.assertEqual(ingredient._amount_needed,1)

            elif ingredient_type == "Garnish":
                self.assertIsInstance(ingredient, Garnish)
                self.assertEqual(ingredient._name, "Mint")
                self.assertEqual(ingredient._amount, 1)
                self.assertEqual(ingredient._price_per_unit, 0.1)
                self.assertEqual(ingredient._substitutes, [])
                self.assertEqual(ingredient._amount_needed,1)


class TestCreateCocktailFromCSV(unittest.TestCase):
    def setUp(self):
        self.csv_data = """Mojito,Alcohol,Rum,40,5,40%,"Vodka",1
Mojito,Syrups,Sugar Syrup,20,1,,"Honey Syrup",1
Mojito,Juice,Lime Juice,40,1,True,"Lemon Juice",1
Mojito,Component,Mineral Water,100,0.5,,"Tonic, Sprite",1
Mojito,Garnish,Mint,5,0.1,leaves,,1
"""
        csv_file = StringIO(self.csv_data)
        self.rows = list(csv.reader(csv_file))

    def test_create_cocktail_from_csv(self):
        cocktail = create_cocktail_from_csv(self.rows)
        self.assertEqual(cocktail._name, "Mojito")
        self.assertEqual(len(cocktail._ingredients), 5)

        alcohol = cocktail._ingredients[0]
        self.assertEqual(alcohol._name, "Rum")
        self.assertEqual(alcohol._strength, 40)
        self.assertEqual(alcohol._substitutes, ["Vodka"])
        self.assertEqual(alcohol._amount_needed, 1)

        component = cocktail._ingredients[3]
        self.assertEqual(component._name, "Mineral Water")
        self.assertEqual(component._substitutes, ["Tonic", "Sprite"])


class TestReadRealCSVFile(unittest.TestCase):
    def test_read_actual_csv_file(self):
        filename = "coctails.csv"  


        self.assertTrue(os.path.exists(filename), f"Failas '{filename}' neegzistuoja.")

        cocktails = read_cocktails_from_csv(filename)


        self.assertTrue(len(cocktails) > 0, "Nė vienas kokteilis nebuvo nuskaitytas.")


        self.assertIn("Mojito", cocktails)


        mojito = cocktails["Mojito"]
        self.assertGreater(len(mojito._ingredients), 0)

        first_ingredient = mojito._ingredients[0]
        self.assertTrue(hasattr(first_ingredient, '_name'))
        self.assertTrue(hasattr(first_ingredient, '_amount'))

class TestWriteCocktailToCSV(unittest.TestCase):
    def setUp(self):
        self.test_filename = "test_cocktails.csv"
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

        self.alcohol = Alcohol("TestRum", 50, 10, 40,substitutes=["TestVodka"], amount_needed=1)
        self.cocktail = Coctail("TestCocktail", [self.alcohol])

    def test_write_cocktail_to_csv(self):
        write_cocktail_to_csv(self.cocktail, self.test_filename)

        self.assertTrue(os.path.exists(self.test_filename))

        with open(self.test_filename, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

            self.assertEqual(rows[0], [
                "coctail_name", "ingredient_type", "ingredient_name", "amount",
                "price_per_unit", "extra_info", "substitutes"
            ])

            self.assertEqual(rows[1], [
                "TestCocktail", "Alcohol", "TestRum", "50", "10", "40%", "TestVodka"
            ])

    def tearDown(self):
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

if __name__ == "__main__":
    unittest.main()