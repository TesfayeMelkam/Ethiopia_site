# (title, date, description, region slug or None, kind)
FESTIVALS = [
("Enkutatash (New Year)","Sept 11 (Meskerem 1)","Ethiopian New Year, with yellow daisies (adey abeba), songs and family feasts.",None,"national"),
("Meskel","Sept 27","Finding of the True Cross, with the Demera bonfire; inscribed by UNESCO in 2013.",None,"religious"),
("Genna","Jan 7","Ethiopian Christmas, marked by church services, white clothes and the genna stick game.",None,"religious"),
("Timkat","Jan 19","Epiphany, with the Tabot processions and the blessing of water; UNESCO inscribed in 2019.",None,"religious"),
("Adwa Victory Day","March 2","Commemorates Ethiopia's victory over Italy at Adwa in 1896.",None,"national"),
("Eid al-Fitr / Eid al-Adha","Varies","Major Muslim holidays celebrated all across Ethiopia.",None,"religious"),
("Irreecha","Early October","Oromo thanksgiving festival held at lakes and rivers after the rainy season.","oromia","cultural"),
("Fiche-Chambalaalla","Varies","Sidama New Year (UNESCO), with food, songs and family gatherings.","sidama","cultural"),
("Fasika (Easter)","Varies (Apr-May)","Ethiopian Orthodox Easter after the 55-day fast, with the great feast of doro wat.",None,"religious"),
("Siklet (Good Friday)","Varies","Solemn day of prayer and fasting before Fasika.",None,"religious"),
("Hosanna (Palm Sunday)","Varies","Palm Sunday, with palm leaves and church processions.",None,"religious"),
("Mawlid (Nebiy Mewlid)","Varies (Islamic calendar)","Birthday of the Prophet, celebrated with prayers and gatherings, especially in Harar and Wollo.",None,"religious"),
("Ethiopian Patriots' Victory Day","May 5 (Miazia 27)","Marks the liberation from Italian occupation in 1941.",None,"national"),
("Downfall of the Derg","May 28 (Ginbot 20)","National holiday marking the end of the Derg regime in 1991.",None,"national"),
("Nations, Nationalities and Peoples' Day","Dec 8","Celebrates Ethiopia's diversity and the 1995 constitution.",None,"national"),
("Buhe","Aug 19 (Nehase 13)","Boys light torches and sing, celebrated across Tigray and Amhara.",None,"cultural"),
("Ashenda","Aug 22-ish (Nehase 16)","Girls dress in beads and sing for days, famous in Tigray and Amhara (Shadey).","tigray","cultural"),
("Tsion Mariam (Aksum)","Nov 30 (Hidar 21)","Pilgrimage to St. Mary of Zion in Aksum.","tigray","religious"),
("Lalibela Genna","Jan 7","Thousands gather at the rock-hewn churches for Ethiopian Christmas.","amhara","religious"),
("Gondar Timkat","Jan 19","Fasilides' Bath is filled and blessed, and crowds joyfully splash in the water.","amhara","religious"),
("Kulubi Gabriel","Dec 28 (and July 26)","Huge pilgrimage to the Kulubi St. Gabriel church near Dire Dawa.","oromia","religious"),
("Great Ethiopian Run","November","Annual 10 km road race in Addis Ababa, one of Africa's largest.","addis-ababa","cultural"),
("Meskel Demera at Meskel Square","Sept 26 evening","The giant Demera bonfire is lit at Meskel Square in Addis Ababa.","addis-ababa","religious"),
("Meskel Gurage","Sept 27","Gurage people celebrate Meskel with kitfo and family gatherings.","central-ethiopia","cultural"),
("Yeshoora (Hadiya New Year)","Varies (around Sept)","New year celebration of the Hadiya people.","central-ethiopia","cultural"),
("Gifata (Wolayta New Year)","Varies (around Sept-Oct)","New year celebration of the Wolayta people in South Ethiopia.","south-ethiopia","cultural"),
("Ashura in Harar","Muharram 10 (varies)","Ashura is observed in Harar with prayers and community meals.","harari","religious"),
("Sheikh Hussein Pilgrimage","Varies (Bale)","Pilgrims visit the Sheikh Hussein shrine in Bale, Oromia, twice a year.","oromia","religious"),
]

BOOKS = [
("Ethiopia at a Glance","Ethiopia Portal Editors","Guide",None,"A short introduction to the land, calendar and languages of Ethiopia.","""# Land and People

Ethiopia lies in the Horn of Africa and covers about 1.1 million square kilometres. Its landscape ranges from the Danakil Depression, one of the lowest and hottest places on Earth, to the Simien Mountains, where Ras Dashen rises to about 4,550 metres.

More than 80 languages are spoken here. Amharic is the federal working language, and Afaan Oromo, Tigrinya, Somali and Afar are widely spoken. Most people are farmers, and the highlands are among the most densely settled parts of Africa.

# A Different Calendar

Ethiopia keeps its own calendar with twelve months of thirty days and a thirteenth month, Pagume, of five or six days. The new year, Enkutatash, falls on 11 September in most years. The calendar runs about seven to eight years behind the Gregorian one.

Time is counted differently too: the day starts at sunrise, so 7 a.m. is called one o'clock in the morning.

# Script and Language

Amharic and Tigrinya are written in the Ge'ez script (fidel), in which each character stands for a consonant and a vowel together. Ge'ez is still the liturgical language of the Ethiopian Orthodox Tewahedo Church."""),
("A Short History of Ethiopia","Ethiopia Portal Editors","History",None,"From early human ancestors to the modern federal republic.","""# Origins

Fossils found in the Afar region, including the 3.2-million-year-old skeleton nicknamed Lucy, found in 1974, show that the land was home to early human ancestors.

By the first centuries CE, the Kingdom of Aksum in the northern highlands traded with Rome, Arabia and India and minted its own coins. In the 4th century King Ezana adopted Christianity.

# Lalibela and the Solomonic Line

In the 12th and 13th centuries the Zagwe dynasty ruled from Lasta, and the rock-hewn churches of Lalibela were carved. In 1270 Yekuno Amlak restored the Solomonic line, which traces its descent, by tradition, from Menelik I, son of King Solomon and the Queen of Sheba.

# Empire and Independence

Gondar became the capital in the 1630s. In 1886 Menelik II founded Addis Ababa, and in 1896 his armies defeated an Italian invasion at Adwa, which kept Ethiopia independent. Italy occupied the country from 1936 to 1941 before it was liberated. After the monarchy ended in 1974, Ethiopia became a federal republic in 1995."""),
("The Ethiopian Coffee Ceremony","Ethiopia Portal Editors","Culture","south-west-ethiopia","How coffee began in Kaffa and how the traditional ceremony is performed.","""# The Origin

Coffea arabica grew wild in the forests of Kaffa in south-western Ethiopia. A popular legend tells of a goatherd named Kaldi who noticed his goats dancing after eating red berries.

# The Ceremony

The ceremony begins with fresh grass spread on the floor. Green beans are washed and roasted on a pan, and the host carries the fragrant smoke around so guests can enjoy it. The beans are ground by hand, brewed in a clay pot called a jebena and served in small cups.

# Three Rounds

Three rounds are served: abol, tona and baraka. Leaving before the third round is considered impolite. Popcorn or bread (dabo) is often offered with the coffee."""),
("Festivals of Ethiopia","Ethiopia Portal Editors","Culture",None,"The great holidays of the Ethiopian year.","""# Enkutatash and Meskel

Enkutatash, the New Year, falls on 11 September, when the rains end and fields turn yellow with daisies. Two weeks later, on 27 September, Meskel remembers the finding of the True Cross. Great bonfires called Demera are lit, and UNESCO inscribed Meskel in 2013.

# Genna and Timkat

Genna, the Ethiopian Christmas, is on 7 January. Timkat follows on 19 January and celebrates Epiphany, when the Tabot is carried in colourful processions and water is blessed. UNESCO inscribed Timkat in 2019.

# Regional Celebrations

Besides national holidays, many peoples have their own festivals, such as Irreecha of the Oromo, Fiche-Chambalaalla of the Sidama and Ashenda in Tigray."""),
("Rock-Hewn Churches of Lalibela","Ethiopia Portal Editors","Heritage","amhara","The eleven monolithic churches of Lalibela, a UNESCO World Heritage Site.","""# The Eleven Churches

The churches of Lalibela were carved downward from solid volcanic rock in the 12th and 13th centuries. They are connected by trenches and tunnels and form two main groups, with Bete Giyorgis standing apart in the shape of a cross. UNESCO listed the site in 1978.

# Pilgrimage

Lalibela is a living place of worship. Thousands of pilgrims come for Genna and Timkat, dressed in white shawls, and priests still chant in Ge'ez."""),
]

KNOW = {
"facts":[("Official name","Federal Democratic Republic of Ethiopia"),("Capital","Addis Ababa"),("Area","about 1.1 million km²"),("Population","about 120 million (estimate)"),("Languages","80+; Amharic is the federal working language"),("Currency","Ethiopian Birr (ETB)"),("Calendar","13 months, about 7-8 years behind the Gregorian calendar"),("Highest point","Ras Dashen, about 4,550 m"),("Lowest point","Danakil Depression, about 125 m below sea level"),("Largest lake","Lake Tana, source of the Blue Nile"),("Flag colours","Green, yellow and red"),("Time","Eastern Africa Time (UTC+3)")],
"timeline":[("3.2 million years ago","Lucy (Dinkinesh) lives in the Afar area; fossils were found in 1974."),("1st-7th century","The Kingdom of Aksum trades across the Red Sea and Indian Ocean."),("4th century","King Ezana adopts Christianity in Aksum."),("12th-13th century","The Zagwe dynasty carves the Lalibela churches."),("1270","Yekuno Amlak restores the Solomonic dynasty."),("1529-1543","War between Ethiopia and the Adal Sultanate."),("1636","Fasilides founds Gondar as a capital."),("1886","Menelik II founds Addis Ababa."),("1896","Ethiopia defeats Italy at the Battle of Adwa."),("1930","Haile Selassie is crowned emperor."),("1936-1941","Italian occupation, ending with liberation."),("1974","The monarchy ends and the Derg takes power."),("1991","The Derg regime falls."),("1995","The federal constitution is adopted."),("2019","Prime Minister Abiy Ahmed wins the Nobel Peace Prize.")],
"unesco":[("Rock-Hewn Churches, Lalibela","1978"),("Simien National Park","1978"),("Fasil Ghebbi, Gondar","1979"),("Aksum","1980"),("Lower Valley of the Awash","1980"),("Lower Valley of the Omo","1980"),("Tiya","1980"),("Harar Jugol","2006"),("Konso Cultural Landscape","2011"),("Gedeo Cultural Landscape","2023"),("Melka Kunture and Balchit","2023"),("Intangible: Meskel, Gadaa, Fiche-Chambalaalla, Timkat","various years")],
"people":[("Abebe Bikila","Won the Olympic marathon barefoot in Rome in 1960 and again in Tokyo in 1964."),("Haile Gebrselassie","Long-distance running legend and Olympic champion."),("Derartu Tulu","First Black African woman to win Olympic gold, in the 10,000 m in 1992."),("Tirunesh Dibaba","Olympic and world champion distance runner."),("Menelik II","Emperor who founded Addis Ababa and won at Adwa."),("Empress Taytu","Co-founder of Addis Ababa and key figure at Adwa."),("Haile Selassie","Emperor from 1930 to 1974."),("Mulatu Astatke","Father of Ethio-jazz."),("Sahle-Work Zewde","First woman president of Ethiopia (2018).")],
"food":[("Injera","Sour flatbread made from teff, the base of most meals."),("Doro wat","Spicy chicken stew with boiled eggs."),("Kitfo","Minced beef seasoned with mitmita and niter kibbeh."),("Tibs","Sauteed meat with onions and peppers."),("Shiro","Chickpea stew, a staple on fasting days."),("Berbere","Spice blend of chilli, garlic, ginger and herbs."),("Tej","Honey wine."),("Buna","Coffee, served in the traditional ceremony."),("Fasting food","Orthodox Christians eat vegan food on Wednesdays, Fridays and during Lent.")],
"culture":[("Krar","Five- or six-string lyre."),("Masenqo","One-string bowed fiddle played by azmari singers."),("Washint","Traditional bamboo flute."),("Begena","Large ten-string lyre used for prayer."),("Kebero","Drum used in church and festivals."),("Eskista","Shoulder dance, especially famous in Amhara."),("Habesha kemis","White cotton dress with woven tilet embroidery."),("Netela and gabi","White cotton shawls worn by men and women."),("Ethio-jazz","Genre combining jazz with Ethiopian scales.")],
"nature":[("Ethiopian wolf","One of the rarest canids, found in highland areas like Bale."),("Gelada","Grass-eating monkey of the Simien Mountains."),("Walia ibex","Endemic wild goat of the Simien Mountains."),("Mountain nyala","Large antelope found in the Bale Mountains."),("Blue Nile (Abay)","Starts at Lake Tana and feeds the Nile."),("Great Rift Valley","Chain of lakes including Ziway, Langano and Hawassa."),("Erta Ale","Volcano with a long-lasting lava lake."),("Awash River","Main river of the east, ending in the Afar desert."),("Birds","Ethiopia has hundreds of species and dozens of endemic birds.")],
"phrases":[("ሰላም","Selam","Hello"),("ጤና ይስጥልኝ","Tena yistilign","Greetings (formal)"),("እንዴት ነህ / ነሽ?","Endet neh / nesh?","How are you? (m/f)"),("አመሰግናለሁ","Amesegnalehu","Thank you"),("እሺ","Eshi","OK"),("ቡና","Buna","Coffee"),("ውሃ","Wuha","Water"),("አዎ / አይደለም","Awo / Aydelem","Yes / No"),("ደህና ሁን","Dehna hun","Goodbye")],
}

QUIZ = [
{"q":"What is the capital of Ethiopia?","a":["Addis Ababa","Gondar","Hawassa","Mekelle"],"c":0},
{"q":"How many months are in the Ethiopian calendar?","a":["12","13","10","14"],"c":1},
{"q":"Which battle in 1896 kept Ethiopia independent?","a":["Maychew","Magdala","Adwa","Metema"],"c":2},
{"q":"Where is the town of the 11 rock-hewn churches?","a":["Lalibela","Aksum","Harar","Jimma"],"c":0},
{"q":"Where did wild Arabica coffee originate?","a":["Bale","Kaffa","Afar","Tigray"],"c":1},
{"q":"Who won the 1960 Olympic marathon barefoot?","a":["Haile Gebrselassie","Kenenisa Bekele","Abebe Bikila","Derartu Tulu"],"c":2},
{"q":"What is Ethiopia's highest peak?","a":["Ras Dashen","Mount Entoto","Mount Damota","Mount Batu"],"c":0},
{"q":"Which script is used to write Amharic?","a":["Latin","Arabic","Ge'ez (Fidel)","Cyrillic"],"c":2},
{"q":"Which festival features the Demera bonfire?","a":["Timkat","Meskel","Genna","Irreecha"],"c":1},
{"q":"Where is the walled city Harar Jugol?","a":["Harari Region","Somali Region","Afar Region","Tigray"],"c":0},
]

AM = {"addis-ababa":"አዲስ አበባ","tigray":"ትግራይ","afar":"አፋር","amhara":"አማራ","benishangul-gumuz":"ቤኒሻንጉል ጉሙዝ","dire-dawa":"ድሬዳዋ","gambela":"ጋምቤላ","harari":"ሐረሪ","oromia":"ኦሮሚያ","sidama":"ሲዳማ","somali":"ሶማሌ","south-ethiopia":"ደቡብ ኢትዮጵያ","central-ethiopia":"ማዕከላዊ ኢትዮጵያ","south-west-ethiopia":"ደቡብ ምዕራብ ኢትዮጵያ"}
KNOW["religion"]=[("Ethiopian Orthodox Tewahedo Church","One of the world's oldest Christian churches, using Ge'ez in worship, with a rich tradition of fasting, icons and manuscripts."),("Islam","Arrived in the 7th century; Harar and parts of Wollo, Arsi, Bale and the Somali and Afar regions are major centres. The Al Negashi mosque in Tigray is among Africa's earliest."),("Protestant churches","Growing since the 20th century, especially in the south and west."),("Catholic Church","A smaller community with schools and clinics."),("Waaqeffannaa","Traditional Oromo faith centred on Waaqa; Irreecha is closely linked to it."),("Beta Israel","Ethiopian Jewish community, historically in the Gondar and Simien areas; most emigrated to Israel in the 1980s-90s.")]
KNOW["languages"]=[("Amharic","Federal working language, written in the Ge'ez script."),("Afaan Oromo","Widely spoken Cushitic language, written in Latin script (Qubee)."),("Tigrinya","Semitic language of Tigray, written in Ge'ez script."),("Somali","Cushitic language of the Somali Region."),("Afar","Cushitic language of the Afar Region."),("Sidaamu Afoo","Language of the Sidama people."),("Wolaytta","Omotic language of Wolayta."),("Gurage languages","Group of Semitic languages of Central Ethiopia."),("Ge'ez","Ancient language still used in the Orthodox liturgy.")]
KNOW["facts"]+= [("Neighbours","Eritrea, Djibouti, Somalia, Kenya, South Sudan and Sudan"),("Main export","Coffee")]
QUIZ+=[
{"q":"Which is Ethiopia's largest lake?","a":["Lake Tana","Lake Hawassa","Lake Ziway","Lake Langano"],"c":0},
{"q":"In which region is the Danakil Depression?","a":["Oromia","Afar","Sidama","Gambela"],"c":1},
{"q":"What is injera made from?","a":["Wheat","Maize","Teff","Rice"],"c":2},
{"q":"Who founded Addis Ababa in 1886?","a":["Haile Selassie","Menelik II","Fasilides","Tewodros II"],"c":1},
{"q":"Which wild goat lives in the Simien Mountains?","a":["Ibex (Walia)","Markhor","Chamois","Tahr"],"c":0},
{"q":"How old is the fossil Lucy?","a":["320,000 years","3.2 million years","32 million years","32,000 years"],"c":1},
{"q":"Which people celebrate Irreecha?","a":["Oromo","Afar","Tigray","Gurage"],"c":0},
{"q":"What is Ethiopia's currency?","a":["Shilling","Birr","Dinar","Nakfa"],"c":1},
{"q":"What is the clay coffee pot called?","a":["Jebena","Mitad","Sini","Mesob"],"c":0},
{"q":"Which country does NOT border Ethiopia?","a":["Kenya","Sudan","Tanzania","Djibouti"],"c":2},
]
BOOKS+=[
("Languages and Peoples of Ethiopia","Ethiopia Portal Editors","Guide",None,"An overview of the main languages and peoples.","""# Many Languages

Ethiopia is home to more than 80 languages in four main families: Semitic (Amharic, Tigrinya, Gurage), Cushitic (Afaan Oromo, Somali, Afar), Omotic (Wolaytta) and Nilo-Saharan (Anuak, Nuer).

# Scripts

Amharic and Tigrinya use the Ge'ez script. Afaan Oromo and Somali are written with the Latin alphabet. Each language carries songs, proverbs and traditions that are part of the country's heritage."""),
("A Guide to Ethiopian Cuisine","Ethiopia Portal Editors","Culture",None,"Injera, stews, spices and the tradition of eating together.","""# The Meal

Most meals are served on injera, a spongy sour flatbread made from teff. Stews called wat, such as doro wat and misir wat, are placed on top, and people eat with their right hands from a shared plate.

# Gursha

To show friendship, a host feeds a guest a bite by hand; this is called gursha.

# Fasting Days

Orthodox Christians fast on Wednesdays, Fridays and during Lent, eating vegan dishes such as shiro, gomen and misir."""),
("Traditions of the Ethiopian Orthodox Church","Ethiopia Portal Editors","Heritage",None,"Fasting, festivals, church art and the Ge'ez tradition.","""# A Living Tradition

The Ethiopian Orthodox Tewahedo Church dates back to the 4th century. Services are chanted in Ge'ez, and the church keeps ancient manuscripts and a distinctive style of icon painting.

# The Tabot

Every church holds a replica of the Ark of the Covenant, called the Tabot. It is carried in procession during Timkat."""),
]
