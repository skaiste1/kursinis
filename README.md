Introduction:
"Cocktail recipe and ingredient management system" mano programa veikia taip:
1. Ji nuskaito kokteilių sąrašą iš failo. Kiekvienas kokteilis turi savo pavadinimą ir ingredientus.
2. Galima matyti, kokių ingredientų reikia kiekvienam kokteiliui ir kiek jie kainuoja.
3. Programa gali patikrinti, ar yra visi reikiami ingredientus, kad galima būtų pagaminti kokteilį. Jei ko nors trūksta, ji gali pasiūlyti, kuo tą ingredientą galima pakeisti.
4. Taip pat galima įrašyti naujus kokteilių receptus į failą.
5. Programa apskiačiuoja bendra sukurto kokteilio kaina, galima pritaikyti ir nuolaidas.

Kaip paleisti programą?
1. Išsisaugoti kodą kaip Python .py failą (coctails.py)
2. Tame pačiame aplankale turi būti csv failas (coctails.csv), jame turėtų būti kokteilių receptai, tokiu formatu. ![CSV failo fragmentas su duomenimis](csv_fragmentas1.jpg) 
3. Įsitikinti, kad turite įdiegtą Python.
4. Atidaryti terminalą ir paleisti programą.


Kaip naudotis programa?
1. Programa nuskaitys CSV faile esančius kokteilius.(CSV faile jų galima pridėt, redaguot ir pan.)
2. Ji patikrins, ar galima pagaminti konkretų kokteilį iš turimų ingredientų.
3. Jei trūksta ingredientų, programa parodys ko trūksta arba pasiūlys pakaitalus.
4. Programa gali paskaičiuoti kiekvieno kokteilio kainą.(Gali turėti ir nuolaidas)


2. Body/Analysis:
    2.1 4 OOOP pillars
            Polymorphism:
            Tai gebėjimas objektiniame programavime vienam veiksmui (metodo iškvietimui) elgtis skirtingai priklausomai nuo objekto tipo, su kuriuo tas veiksmas yra atliekamas.Jis pasireiškia per method overriding arba method overloading. Method Overriding, kai subklasė turi metodą tokiu pačiu pavadinimu ir argumentų sąrašu kaip ir jos superklasė, bet metodo implementacija yra kitokia. Method Overloading, reiškia, kad vienoje klasėje gali būti keli metodai tuo pačiu pavadinimu, bet su skirtingu argumentų skaičiumi arba tipais.

            (a) Mano kode buvo naudojamas method overriding su show_info() metodu, kur Ingredients klasė ir jos paveldėtojai (Alcohol, Syrups, Juice, Component, Garnish), turėjo tą patį abstraktų metodą paveldėtą iš Ingredients. Kiekviena klasė pateikia informaciją apie save unikaliu formatu, atsižvelgdama į savo specifinius atributus (pvz., alkoholis rodo stiprumą, sultys – ar yra ekologiškos). ![polymorphism_ex1](polymorphysm1.png)

            (b) IngredientFactory klasė ir jos paveldėtojai (AlcoholFactory, SyrupsFactory, JuiceFactory, GarnishFactory, ComponentFactory), kur yra abstraktus metodas create() iš IngredientFactory. Paveldinčios klasės implementuoja šį metodą, kad sukurtų būtent tos rūšies ingrediento objektą. Tai leidžia lanksčiai kurti įvairių tipų ingredientus naudojant bendrą sąsają. ![polymorphysm_ex2](polymorphysm2.png)

            (c) CoctailDecorator klasė ir jos paveldėtojas (DiscountedCoctail) su metodu get_total_price(). CoctailDecorator yra bazinė dekoratoriaus klasė, kuri paveldi iš Coctail ir perima jo metodus. DiscountedCoctail yra konkretus dekoratorius, kuris perrašo get_total_price() metodą, pridėdamas nuolaidos logiką. ![polymorphysm_ex3](polymophysm3.png)


            Abstraction:
            Būdas pateikti svarbią informaciją ir paslėpti sudėtingus veikimo mechanizmus.

            (a) Demonstruojama naudojant abstrakčias bazines klases (ABC) ir abstrakčius metodus (@abstractmethod). Ingredients klasė yra abstrakti bazinė klasė su abstrakčiu metodu show_info(). Tada iš jos paveldinčios klasės gali įgyvendinti savo specifinį ingredientų informacijos rodymo būdą. ![abstraction1](abstraction1.png)
            
            (b) IngredientFactory yra dar viena abstrakti bazinė klasė, kuri leidžia kurti skirtingų tipų ingredientus.![abstraction2](abstraction2.png)


            Inheritance:
            Paveldinčioji klasė perima kitos tėvinės klasės savybes ir metodus.

            (a) Klasės (Alcohol, Syrups, Juice, Component, Garnish) paveldi iš klasės Ingredients bendrus atributus ir metodus ir gali juos išplėsti arba pakeisti, kad atstovautų konkrečius ingredientų tipus su jų unikaliomis savybėmis (pvz., stiprumas alkoholiui, ekologiškos sultys). ![inheritance1](inheritance1.png)

            (b) Kode taip pat paveldėjimas matomas su paveldinčiom klasėm iš IngredientFactory ir CoctailDecorator paveldi iš Coctail.


            Encapsulation:
            Duomenys ir metodai, veikiantys su tais duomenimis, yra sujungiami į vieną vienetą. Dažnai apima duomenų slėpimą, apribojant tiesioginę prieigą ir leidžiant keisti duomenimis tik per klasės metodus.

            (a) Kode tam tikri kintamieji yra privatūs ir išorinis kodas negali tiesiogiai jų keisti tam yra get metodai. ![encapsulation1](encapsulation1.png)

    2.2 Design Patterns 
        Factory Method:
        Vietoj to, kad būtų tiesiogiai kuriami nauji objektai, jis kreipiasi į specialų objektą – factory. Šis factory yra atsakingas už reikiamo objekto tipo sukūrimą ir grąžinimą klientui. Man labiausiai tiko šis design pattern dėl to, nes galėjau kurti įvairius, bet susijusius objektų tipus. Savo kode turiu daug ingridientų klasių ir fabrikus joms kurti. ![factory](factory.png)


        Singleton:
        Leidžia sukurti tik vieną objektą visoje programoje. Mano kode Singleton šablonas buvo pritaikytas Inventory klasei. Tai užtikrino, kad visoje sistemoje būtų naudojamas tik vienas bendras inventoriaus objektas, kuris saugo visus turimus ingredientus. Tokiu būdu visi kokteiliai gali tikrinti ar jų ingredientai yra bendrame sąraše, o visi pakeitimai (pvz., naujų ingredientų pridėjimas) iš karto atsispindi visoje sistemoje. ![singleton](singleton.png)


        Decorator:
        Gali pridėti naujų savybių ar veiksmų objektui, nekeisdamas jo pradinio kodo. Mano kode naudotas Decorator šablonas, siekiant praplėsti Coctail objektų funkcionalumą. Sukurta CoctailDecorator klasė leidžia suteikti kokteiliui papildomomas savybes, nekeičiant pačio Coctail kodo. DiscountedCoctail pritaiko nuolaidą galutinei kainai. Šis šablonas leidžia išplėsti elgseną lanksčiai ir tvarkingai.![decorator](decorator.png)

    2.3 Composition/Aggregation
        Kompozicija – tai objektų ryšys, kai vienas objektas turi kitus objektus kaip savo dalis, ir be jų negalėtų veikti. Agregacija – tai irgi ryšys tarp objektų, bet silpnesnis. Vienas objektas turi kitą, bet priklausomybė nėra būtina. 

        Mano kode kompozicija matoma Coctail klasėjė, kur ji kompoziciškai naudoja Ingredient objektus. Jie būtini tam, kad kokteilis egzistuotų. Jei Coctail objektas sunaikinamas, tai ir susinaikins Ingredients esantys jame.![composition](composition.png)

        Klasė Inventory agreguoja Ingredient objektus, bet jie nėra būtini Inventory egzistavimui. ![aggregation](aggregation.png)

3. Results and summary:

    Results:
    1. Įgyvendinti visi 4 OOP principai bei trys dizaino šablonai (Factory, Singleton, Decorator), kompozicija/agregacija.
    2. Sėkmingai ištestuotos visos kodo eilutės.
    3. Sukurta pilnai veikianti kokteilių valdymo sistema, kuri leidžia patikrinti ingredientus, kainą ir galimus pakaitalus.

    Conclusion:
    Šio darbo metu buvo sukurta objektinio programavimo principais pagrįsta kokteilių valdymo sistema, kuri leidžia kurti, analizuoti ir vertinti kokteilių sudėtį.Pavyko sėkmingai pritaikyti svarbiausius OOP principus ir kelis dizaino šablonus, pagerinančius kodo lankstumą, išplėtimą ir organizaciją. Pavyko sėkmingai naudoti CSV failą kodo funkcionalumui, į jį rašyti, iš jo skaityti ir pan. 

    Future prospect:
    Galima būtų naudoti duomenų bazes vietoj CSV failo. Galėtų būti rekomendacijos sistema (siūlytų kokteilį pagal turima inventorių). Aiškesni receptai su detalesniais aprašymais kaip gaminti kokteilį.













