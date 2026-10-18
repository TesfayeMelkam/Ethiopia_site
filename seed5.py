COORDS = {"addis-ababa":(9.03,38.74),"tigray":(13.49,39.47),"afar":(11.79,41.00),"amhara":(11.59,37.39),"benishangul-gumuz":(10.07,34.53),"dire-dawa":(9.60,41.86),"gambela":(8.25,34.59),"harari":(9.31,42.12),"oromia":(8.54,39.27),"sidama":(7.06,38.48),"somali":(9.35,42.80),"south-ethiopia":(6.03,37.55),"central-ethiopia":(7.55,37.85),"south-west-ethiopia":(7.27,36.25)}
# approximate coordinates (name, lat, lng, region, kind)
MAPPTS = [("Lalibela",12.03,39.04,"amhara","heritage"),("Gondar",12.60,37.47,"amhara","heritage"),("Aksum",14.12,38.72,"tigray","heritage"),("Yeha",14.29,39.43,"tigray","heritage"),("Harar Jugol",9.31,42.12,"harari","heritage"),("Konso (Karat)",5.25,37.48,"south-ethiopia","heritage"),("Tiya",8.43,38.61,"central-ethiopia","heritage"),("Debre Libanos",9.71,38.84,"oromia","heritage"),
("Dessie",11.13,39.63,"amhara","city"),("Debre Markos",10.33,37.72,"amhara","city"),("Debre Berhan",9.68,39.53,"amhara","city"),("Jimma",7.67,36.83,"oromia","city"),("Adama",8.54,39.27,"oromia","city"),("Bishoftu",8.75,38.98,"oromia","city"),("Hawassa",7.06,38.48,"sidama","city"),("Arba Minch",6.03,37.55,"south-ethiopia","city"),("Mekelle",13.49,39.47,"tigray","city"),("Bahir Dar",11.59,37.39,"amhara","city"),("Dire Dawa",9.60,41.86,"dire-dawa","city"),
("Blue Nile Falls",11.49,37.58,"amhara","nature"),("Simien Mountains (Debark)",13.15,38.00,"amhara","nature"),("Lake Tana",12.00,37.30,"amhara","nature"),("Erta Ale",13.60,40.67,"afar","nature"),("Dallol",14.24,40.30,"afar","nature"),("Bale Mountains",6.75,39.75,"oromia","nature"),("Lake Langano",7.60,38.75,"oromia","nature"),("Nechisar National Park",5.85,37.75,"south-ethiopia","nature"),("Awash National Park",9.00,40.00,"afar","nature")]
RECIPES = [
("Shiro Wat","about 40 min",4,["1 cup shiro powder (ground chickpea mix)","1 large onion, finely chopped","2 tbsp oil or niter kibbeh","2 cloves garlic, minced","1 tsp berbere (or to taste)","3 cups water","Salt"],[("Cook the chopped onion in a dry pot over medium heat, stirring.",5),("Add the oil, garlic and berbere and cook until fragrant.",3),("Add the water and bring to a gentle boil.",3),("Whisk in the shiro powder gradually to avoid lumps.",2),("Simmer on low, stirring often, until thick and smooth. Add salt.",20),("Serve hot with injera.",0)]),
("Misir Wat (Red Lentil Stew)","about 45 min",4,["1 cup red lentils, rinsed","2 onions, finely chopped","3 tbsp oil","3 cloves garlic","1 tsp grated ginger","2 tbsp berbere","1 tbsp tomato paste","3 cups water","Salt"],[("Cook the onions in a dry pot until soft.",8),("Add oil, garlic, ginger and berbere. Stir for a few minutes.",4),("Add tomato paste and lentils, then the water.",2),("Simmer until the lentils are tender and the stew is thick. Add salt.",25),("Serve with injera.",0)]),
("Doro Wat (Chicken Stew)","about 1 hr 30 min",6,["1 kg chicken pieces","4 large red onions, finely chopped","4 tbsp niter kibbeh (spiced butter)","3 tbsp berbere","3 cloves garlic and 1 tsp ginger","4 hard-boiled eggs","Juice of 1 lemon","2 cups water","Salt"],[("Cook the onions in a dry pot until soft and reduced.",20),("Add niter kibbeh, garlic, ginger and berbere. Cook gently.",10),("Add the chicken and water. Cover and simmer.",45),("Add the peeled boiled eggs and lemon juice. Add salt.",10),("Serve with injera.",0)]),
("Tibs (Sauteed Beef)","about 25 min",3,["500 g beef, cut in small cubes","1 onion, sliced","1 green pepper, sliced","2 tbsp niter kibbeh or oil","2 cloves garlic","Rosemary or berbere (optional)","Salt"],[("Heat the niter kibbeh in a pan until hot.",2),("Add the beef and brown it well.",8),("Add the onion, garlic and pepper.",6),("Season and cook until the meat is done.",5),("Serve with injera or bread.",0)]),
]
PEOPLE = [
("Ezana","Rulers","4th century","King of Aksum who adopted Christianity and made it the state religion."),
("Lalibela","Rulers","c. 1181-1221","Zagwe king traditionally credited with the rock-hewn churches of Lalibela."),
("Zara Yaqob","Rulers","1399-1468","Emperor who strengthened the church and founded Debre Berhan."),
("Tewodros II","Rulers","1818-1868","Emperor who began the reunification of Ethiopia."),
("Menelik II","Rulers","1844-1913","Founded Addis Ababa and led Ethiopia to victory at Adwa."),
("Empress Taytu","Rulers","c. 1851-1918","Wife of Menelik II, co-founder of Addis Ababa and key figure at Adwa."),
("Haile Selassie","Rulers","1892-1975","Emperor of Ethiopia from 1930 to 1974."),
("Abebe Bikila","Athletes","1932-1973","Won Olympic marathon gold in 1960 (barefoot) and 1964."),
("Haile Gebrselassie","Athletes","b. 1973","Distance running legend and two-time Olympic 10,000 m champion."),
("Derartu Tulu","Athletes","b. 1972","First Black African woman Olympic champion (1992, 10,000 m)."),
("Kenenisa Bekele","Athletes","b. 1982","Olympic and world distance champion."),
("Tirunesh Dibaba","Athletes","b. 1985","Olympic and world champion distance runner."),
("Mulatu Astatke","Artists","b. 1943","Ethiopian musician known as the father of Ethio-jazz."),
("Aster Aweke","Artists","b. 1959","Celebrated Ethiopian singer."),
("Haddis Alemayehu","Writers","1910-2003","Author of the novel Fikir Eskemekabir."),
("Maaza Mengiste","Writers","b. 1974","Ethiopian-American novelist."),
("Sahle-Work Zewde","Leaders","b. 1950","First woman president of Ethiopia (from 2018)."),
("Abiy Ahmed","Leaders","b. 1976","Prime Minister of Ethiopia; Nobel Peace Prize 2019."),
]
DYNASTIES = [("Kingdom of Aksum","c. 1st-10th century","Trading empire in the northern highlands."),("Zagwe dynasty","c. 10th century-1270","Rulers from Lasta who built Lalibela's churches."),("Solomonic dynasty","1270-1974","Dynasty tracing its line to Solomon and the Queen of Sheba."),("Era of the Princes","1769-1855","Period of regional princes before reunification."),("Derg regime","1974-1991","Military government after the monarchy ended."),("Federal republic","1995-present","Federal constitution with regional states.")]
DIRECTORY = [
("addis-ababa","transport","Bole International Airport","Ethiopia's main international airport, hub of Ethiopian Airlines.","Bole, Addis Ababa"),
("addis-ababa","transport","Ethiopian Airlines","National airline with hub in Addis Ababa and many domestic routes.","Addis Ababa"),
("addis-ababa","transport","Addis Ababa-Djibouti Railway","Standard-gauge railway linking the Addis Ababa area with Djibouti.","Addis Ababa to Djibouti"),
("addis-ababa","hospital","Tikur Anbessa (Black Lion) Hospital","Large teaching hospital in Addis Ababa.","Addis Ababa"),
("addis-ababa","hotel","Taitu Hotel","Historic hotel founded by Empress Taytu, near Piassa.","Piassa, Addis Ababa"),
("addis-ababa","cafe","Tomoca Coffee","Well-known Addis Ababa coffee roaster and cafe.","Piassa, Addis Ababa"),
]
FIDEL = [("h","ሀ ሁ ሂ ሃ ሄ ህ ሆ"),("l","ለ ሉ ሊ ላ ሌ ል ሎ"),("m","መ ሙ ሚ ማ ሜ ም ሞ"),("r","ረ ሩ ሪ ራ ሬ ር ሮ"),("s","ሰ ሱ ሲ ሳ ሴ ስ ሶ"),("sh","ሸ ሹ ሺ ሻ ሼ ሽ ሾ"),("q","ቀ ቁ ቂ ቃ ቄ ቅ ቆ"),("b","በ ቡ ቢ ባ ቤ ብ ቦ"),("t","ተ ቱ ቲ ታ ቴ ት ቶ"),("n","ነ ኑ ኒ ና ኔ ን ኖ"),("ʼ","አ ኡ ኢ ኣ ኤ እ ኦ"),("k","ከ ኩ ኪ ካ ኬ ክ ኮ"),("w","ወ ዉ ዊ ዋ ዌ ው ዎ"),("z","ዘ ዙ ዚ ዛ ዜ ዝ ዞ"),("y","የ ዩ ዪ ያ ዬ ይ ዮ"),("d","ደ ዱ ዲ ዳ ዴ ድ ዶ"),("g","ገ ጉ ጊ ጋ ጌ ግ ጎ"),("T","ጠ ጡ ጢ ጣ ጤ ጥ ጦ"),("f","ፈ ፉ ፊ ፋ ፌ ፍ ፎ"),("p","ፐ ፑ ፒ ፓ ፔ ፕ ፖ")]
VOWELS = ["ä","u","i","a","e","ə","o"]
NUMBERS = [("፩ / አንድ","and","1"),("፪ / ሁለት","hulet","2"),("፫ / ሦስት","sost","3"),("፬ / አራት","arat","4"),("፭ / አምስት","amist","5"),("፮ / ስድስት","sidist","6"),("፯ / ሰባት","sebat","7"),("፰ / ስምንት","simint","8"),("፱ / ዘጠኝ","zetegn","9"),("፲ / አስር","asir","10")]
DAYS = [("ሰኞ","Segno","Monday"),("ማክሰኞ","Maksegno","Tuesday"),("ረቡዕ","Rebu'e","Wednesday"),("ሐሙስ","Hamus","Thursday"),("ዓርብ","Arb","Friday"),("ቅዳሜ","Kidame","Saturday"),("እሁድ","Ehud","Sunday")]
KIDS = [("🌍","Ethiopia is in East Africa, in a region called the Horn of Africa."),("📅","Ethiopia has 13 months in a year!"),("☕","Coffee comes from Ethiopia."),("🏃","Ethiopian runners win many Olympic medals."),("🦁","Wild animals like the gelada monkey live in the Simien Mountains."),("⛪","Churches in Lalibela were carved from solid rock."),("🌈","The flag is green, yellow and red."),("🍞","People eat a spongy bread called injera.")]
POLL = ("What is your favourite Ethiopian festival?",["Timkat","Meskel","Enkutatash","Genna","Irreecha","Fasika"])
I18N = {
"en":{"home":"Home","addis":"Addis Ababa","regions":"Regions","library":"Library","know":"Know Ethiopia","festivals":"Festivals","more":"More","admin":"Admin"},
"am":{"home":"መነሻ","addis":"አዲስ አበባ","regions":"ክልሎች","library":"ቤተ መጻሕፍት","know":"ኢትዮጵያን ይወቁ","festivals":"በዓላት","more":"ተጨማሪ","admin":"አስተዳዳሪ"},
"om":{"home":"Fuula Duraa","addis":"Finfinnee","regions":"Naannolee","library":"Mana Kitaabaa","know":"Itoophiyaa Beeki","festivals":"Ayyaanota","more":"Dabalata","admin":"Bulchiinsa"},
}
