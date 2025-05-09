from abc import ABC, abstractmethod
import csv

class Ingredients(ABC):
    def __init__(self, name, amount, price_per_unit, substitutes=None,amount_needed=1):
        self._name=name
        self._amount=amount
        self._price_per_unit=price_per_unit
        self._amount_needed=amount_needed
        self._substitutes = substitutes or []

    def get_substitute(self, inventory=None):
        if inventory is None:
            inventory=[]
        inventory_lower = [item.lower() for item in inventory]
        for sub in self._substitutes:
            if sub.lower() in inventory_lower:
                return sub
        return None
    
    def get_price(self):
        return self._price_per_unit * self._amount_needed 
    
    @abstractmethod
    def show_info(self):
        pass

    def get_name(self):
        return self._name

    def get_amount(self):
        return self._amount

    def get_price_per_unit(self):
        return self._price_per_unit
    
    def get_substitutes(self):
        return self._substitutes
    
    def get_amount_needed(self):
        return self._amount_needed

class Alcohol(Ingredients):
    def __init__(self, name, amount, price_per_unit,strength=0, substitutes=None, amount_needed=1):
        super().__init__(name, amount, price_per_unit, substitutes, amount_needed)
        self._strength = strength

    def show_info (self):
        return f"{self._name} (Alcohol, {self._strength}% , {self._amount}ml, {self._price_per_unit:.2f}Eur)"
    

class Syrups(Ingredients):
    def __init__(self, name, amount,price_per_unit, substitutes=None,amount_needed=1):
        super().__init__(name, amount, price_per_unit, substitutes,amount_needed)

    def show_info(self):
        return f"{self._name} (Syrup {self._amount}ml, {self._price_per_unit:.2f}Eur)"
    
    
class Juice(Ingredients):
    def __init__ (self, name,amount,price_per_unit, organic = True, type=None, substitutes=None, amount_needed=1):
        super().__init__(name, amount, price_per_unit, substitutes, amount_needed)
        self._organic = organic
        self._type= type

    def show_info(self):
        organic_text = "organic" if self._organic else "not organic"
        return f"{self._name} (Juice {organic_text} , {self._amount}ml, {self._price_per_unit:.2f}Eur,{self._type})"
    

class Garnish(Ingredients):
    def __init__(self, name,amount,price_per_unit, type, substitutes=None, amount_needed=1):
        super().__init__(name, amount, price_per_unit, substitutes, amount_needed)
        self._type = type

    def show_info(self):
        return f"{self._name} (Garnish {self._type} , {self._amount}g, {self._price_per_unit:.2f}Eur)"
    

class Component(Ingredients):
    def __init__(self, name, amount,price_per_unit, substitutes=None, amount_needed=1):
        super().__init__(name, amount, price_per_unit, substitutes, amount_needed)
        
    def show_info(self):
        return f"{self._name} (Component {self._amount}g, {self._price_per_unit:.2f}Eur)"
    
class IngredientFactory(ABC):
    @abstractmethod
    def create (self, **kwargs):
        pass
    
class AlcoholFactory(IngredientFactory):
    def create(self,**kwargs):
        return Alcohol(**kwargs)
    
class SyrupsFactory(IngredientFactory):
    def create(self,**kwargs):
        return Syrups(**kwargs)
    
class JuiceFactory(IngredientFactory):
    def create(self,**kwargs):
        return Juice(**kwargs)
    
class GarnishFactory(IngredientFactory):
    def create(self,**kwargs):
        return Garnish(**kwargs)
    
class ComponentFactory(IngredientFactory):
    def create(self,**kwargs):
        return Component(**kwargs)

    
class Inventory:
    _instance=None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Inventory, cls).__new__(cls)
            cls._instance.__items = []
        return cls._instance

    def add(self, ingredient):
        self.__items.append(ingredient)

    def get_inventory_items(self):
        return self.__items

class Coctail:
    def __init__(self, name, ingredients):
        self._name=name
        self._ingredients=ingredients

    def get_total_price(self, inventory=None):
        total_price = sum(ingredient.get_price() for ingredient in self._ingredients)
        return round(total_price, 2)
            
    
    def is_makeable(self, inventory):
        new_ingredients=[]
        missing_ingredients =[]
        inventory_dict = {item._name.lower().replace("_", " "): item for item in inventory}

        for ingredient in self._ingredients:
            ing_name = ingredient.get_name().lower().replace("_", " ")
            
            if ing_name not in inventory_dict:
                substitute = ingredient.get_substitute(inventory_dict)

                if substitute:
                    print(f"Changing {ingredient.get_name()} to {substitute}")
                    new_substitute = type(ingredient)(substitute, ingredient.get_amount(), ingredient.get_price_per_unit(), substitutes =[],amount_needed=ingredient.get_amount_needed())
                    new_ingredients.append(new_substitute)

                    old_word = ingredient.get_name().split()[0].lower()
                    new_word = substitute.split()[0].lower()
                    if old_word in self._name.lower():
                        self._name = self._name.lower().replace(old_word, new_word).title()
                    
                else: 
                    missing_ingredients.append(ingredient.get_name())
            else:
                new_ingredients.append(ingredient)

        if missing_ingredients:
            return f"cannot make {self._name}, missing {', '.join(missing_ingredients)}"
                
        self._ingredients=new_ingredients
        return (f"The {self._name} can be made with the available ingredients")
    
    def missing_ingredients(self, inventory):
        missing = [ingredient.get_name() for ingredient in self._ingredients if ingredient.get_name() not in inventory 
                   and not ingredient.get_substitute(inventory) ]
        if missing:
            return (f"Missing ingredients {''.join(missing)}")
        return ("All the ingredients are available")
        
    def get_substitutes_for_missing(self, inventory):
        substitutes = {}
        for ingredient in self._ingredients:
            if ingredient.get_name() not in inventory:
                substitute = ingredient.get_substitute(inventory)
                if substitute:
                    substitutes[ingredient.get_name()] = substitute
        return substitutes
    
    def show_recipe(self):
        recipe = f"{self._name}\n"
        total_price = 0
        for ingredient in self._ingredients:
            ingredient_info = ingredient.get_name()
            amount_needed = ingredient.get_amount_needed()
            price = ingredient.get_price_per_unit()
            total_price += price * amount_needed
            recipe += f"{ingredient_info}: {amount_needed} x {price:.2f} Eur\n"
    
        recipe += f"{total_price:.2f} Eur"
        return recipe
    
    def get_name(self):
        return self._name

    def get_ingredients(self):
        return self._ingredients


class CoctailDecorator(Coctail):
    def __init__(self, coctail):
        super().__init__(coctail.get_name(), coctail.get_ingredients())
        self._coctail=coctail
    
    def show_recipe(self):
        return self._coctail.show_recipe()
    
    def get_total_price(self):
        return self._coctail.get_total_price()
    

class DiscountedCoctail(CoctailDecorator):
    def __init__(self, coctail, discount):
        super().__init__(coctail)
        self.__discount=discount

    def get_total_price(self):
        price=self._coctail.get_total_price()
        return price*(1-self.__discount)
    
    def show_info(self):
        return self._coctail.show_recipe()

def create_ingredient_from_csv(row):
    ingredient_type = row[1].strip()
    name = row[2].strip()
    amount = float(row[3])
    price_per_unit = float(row[4])
    extra_info = row[5].strip() if row[5].strip() else None
    substitutes = [s.strip() for s in row[6].split(',') if s.strip()]
    amount_needed=float(row[7]) if len(row) > 7 and row[7].replace('.', '', 1).isdigit() else 1

    kwargs = {
        'name': name,
        'amount': amount,
        'price_per_unit': price_per_unit,
        'substitutes': substitutes,
        'amount_needed': amount_needed,
    }

    if ingredient_type == 'Alcohol':
        kwargs['strength'] = float(extra_info.replace('%', ''))
        factory = AlcoholFactory()
    elif ingredient_type == 'Syrups':
        factory = SyrupsFactory()
    elif ingredient_type == 'Juice':
        kwargs['organic'] = extra_info.lower() == 'true'
        kwargs['type'] = extra_info if extra_info else None
        factory = JuiceFactory()
    elif ingredient_type == 'Garnish':
        kwargs['type'] = extra_info
        factory = GarnishFactory()
    elif ingredient_type == 'Component':
        factory = ComponentFactory()
    else:
        raise ValueError(f"Unknown ingredient type: {ingredient_type}")

    ingredient = factory.create(**kwargs)
    ingredient.substitutes = substitutes
    return ingredient


def create_cocktail_from_csv(rows):
    cocktail_name = rows[0][0].strip()
    ingredients = [create_ingredient_from_csv(row) for row in rows] 
    return Coctail(cocktail_name, ingredients) 

def read_cocktails_from_csv(filename="cocktails.csv"):
    cocktails = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  

            cocktail_name_idx = header.index("coctail_name")
            ingredient_type_idx = header.index("ingredient_type")
            ingredient_name_idx = header.index("ingredient_name")
            amount_idx = header.index("amount")
            price_per_unit_idx = header.index("price_per_unit")
            extra_info_idx = header.index("extra_info")
            substitutes_idx = header.index("substitutes")
            amount_needed_idx = header.index("amount_needed")

            cocktail_rows = []
            current_cocktail_name = None

            for row in reader:
                if not row: 
                    continue

                cocktail_name = row[cocktail_name_idx].strip()

            
                if current_cocktail_name != cocktail_name:
                    if cocktail_rows:  
                        cocktail = create_cocktail_from_csv(cocktail_rows)
                        cocktails[current_cocktail_name] = cocktail
                    cocktail_rows = [row]  
                    current_cocktail_name = cocktail_name
                else:
                    cocktail_rows.append(row)  

           
            if cocktail_rows:
                cocktail = create_cocktail_from_csv(cocktail_rows)
                cocktails[current_cocktail_name] = cocktail

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except csv.Error as e:
        print(f"Error reading CSV file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")

    return cocktails


def write_cocktail_to_csv(cocktail, filename="cocktails.csv"):
    try:
        with open(filename, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow([
                    "coctail_name", "ingredient_type", "ingredient_name", "amount",
                    "price_per_unit", "extra_info", "substitutes"
                ])

            for ingredient in cocktail.get_ingredients():
                ingredient_type = ""
                extra_info = ""
                if isinstance(ingredient, Alcohol):
                    ingredient_type = "Alcohol"
                    extra_info = f"{ingredient._strength}%"
                elif isinstance(ingredient, Syrups):
                    ingredient_type = "Syrups"
                    extra_info = ingredient._type
                elif isinstance(ingredient, Juice):
                    ingredient_type = "Juice"
                    extra_info = "True" if ingredient._organic else "False" 
                elif isinstance(ingredient, Garnish):
                    ingredient_type = "Garnish"
                    extra_info = ingredient._type
                elif isinstance(ingredient, Component):
                    ingredient_type = "Component"
                    extra_info = ingredient._type

                substitutes_str = ",".join(ingredient.get_substitutes())

                writer.writerow([
                    cocktail.get_name(),
                    ingredient_type,
                    ingredient.get_name(),
                    ingredient.get_amount(),
                    ingredient.get_price_per_unit(),
                    extra_info,
                    substitutes_str
                ])
    except Exception as e:
        print(f"An error occurred while writing to CSV file: {e}")


import csv



def read_cocktails_from_csv(filename="cocktails.csv"):
 
    cocktails = {}
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)  
            
            cocktail_name_idx = header.index("cocktail_name")
            ingredient_type_idx = header.index("ingredient_type")
            ingredient_name_idx = header.index("ingredient_name")
            amount_idx = header.index("amount")
            price_per_unit_idx = header.index("price_per_unit")
            extra_info_idx = header.index("extra_info")
            substitutes_idx = header.index("substitutes")
            amount_needed_idx = header.index("amount_needed")
            
            cocktail_rows = []
            current_cocktail_name = None

            for row in reader:
                if not row:
                    continue

                cocktail_name = row[cocktail_name_idx].strip()

                if current_cocktail_name != cocktail_name:
                    if cocktail_rows:  
                        cocktail = create_cocktail_from_csv(cocktail_rows)
                        cocktails[current_cocktail_name] = cocktail
                    cocktail_rows = [row]  
                    current_cocktail_name = cocktail_name
                else:
                    cocktail_rows.append(row)  

            if cocktail_rows:
                cocktail = create_cocktail_from_csv(cocktail_rows)
                cocktails[current_cocktail_name] = cocktail

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    except csv.Error as e:
        print(f"Error reading CSV file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")

    return cocktails


def main():
    inventory = Inventory()
    cocktails = read_cocktails_from_csv()

    while True:
        print("\nCocktail Management system")
        print("1. Rodyti visus galimus kokteilius")
        print("2. Patikrinti, ar galima pagaminti kokteilį")
        print("3. Rodyti kokteilio receptą ir kainą")
        print("4. Pridėti ingredientą į inventorių")
        print("5. Peržiūrėti inventorių")
        print("6. Išeiti")

        choice = input("Pasirinkite veiksmą: ")

        if choice == "1":
            print("\nGalimi kokteiliai:")
            for name in sorted(cocktails.keys()):
                print(f"- {name}")

        elif choice == "2":
            cocktail_name = input("Įveskite kokteilio pavadinimą, kurį norite patikrinti: ").title()
            if cocktail_name in cocktails:
                result = cocktails[cocktail_name].is_makeable(inventory.get_inventory_items())
                print(result)
            else:
                print("Tokio kokteilio neradome.")

        elif choice == "3":
            cocktail_name = input("Įveskite kokteilio pavadinimą, kurio receptą norite pamatyti: ").title()
            if cocktail_name in cocktails:
                print(cocktails[cocktail_name].show_recipe())
                total_price = cocktails[cocktail_name].get_total_price()
                print(f"Bendra kaina: {total_price:.2f} Eur")
                has_discount = input("Ar turite nuolaidą? (taip/ne): ").lower()
                if has_discount == "taip":
                    try:
                        discount = float(input("Įveskite nuolaidos procentą (pvz., 10): ")) / 100
                        discounted_cocktail = DiscountedCoctail(cocktails[cocktail_name], discount)
                        discounted_price = discounted_cocktail.get_total_price()
                        print(f"Kaina su {discount * 100:.0f}% nuolaida: {discounted_price:.2f} Eur")
                    except ValueError:
                        print("Neteisingas nuolaidos formatas.")
            else:
                print("Tokio kokteilio neradome.")

        elif choice == "4":
            name = input("Įveskite ingrediento pavadinimą: ")
            try:
                amount = float(input("Įveskite kiekį (pvz., 100): "))
                price = float(input("Įveskite vieneto kainą: "))
                # Sukuriame bazinį Ingredient objektą, galite patobulinti pagal tipą
                ingredient = Component(name, amount, price)
                inventory.add(ingredient)
                print(f"Ingredientas '{name}' pridėtas į inventorių.")
            except ValueError:
                print("Neteisingas kiekio arba kainos formatas.")

        elif choice == "5":
            if inventory.get_inventory_items():
                print("\nDabartinis inventorius:")
                for item in inventory.get_inventory_items():
                    print(f"- {item.show_info()}")
            else:
                print("Inventorius tuščias.")

        elif choice == "6":
            print("Viso gero!")
            break

        else:
            print("Netinkamas pasirinkimas. Bandykite dar kartą.")

if __name__ == "__main__":
    main()