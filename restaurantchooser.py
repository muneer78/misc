import random

low = ["Strip's Chicken",  "Panera",  "Chipotle",  "McDonald's",  "Sonic",  "Burger King",  "Wendy's",  "Taco Bell",  "DQ",  "Pizza Street",  "Wing Street",  "Little Caesar's",  "Pancho's"]
mid = ["ABC Cafe",  "Hong Kong Star",  "Q39",  "Bo Ling's",  "Cheddar's",  "Kulture Kurry",  "Fasika",  "El Salvadoreno",  "Nick & Jake's",  "Hu Hot",  "Mi Ranchito",  "Salty Iguana",  "Applebee's",  "Elsa's",  "Thai House",  "Mai Thai",  "India Palace",  "Macaroni Grill",  "Old Chicago",  "Red Lobster",  "Sushi Mido",  "Lucky Wok",  "Thai Place",  "KC Grill & Kabob",  "Zoe's Kitchen",  "Joe's Kansas City",  "Houlihan's",  "Red Door Grill",  "Pizza Hut",  "Minsky's",  "Buffalo Wild Wings",  "Domino's",  "Ni Hao Fresh",  "Em Chamas",  "Joy Wok"]
high = ["J. Gilbert's",  "Eddie V's",  "McCormick & Schmick's",  "Paisano's",  "Seafood Island",  "Argosy Buffet",  "Bristol",  "Cupini's",  "Garozzo's",  "Fogo de Chao",  "Sushi Train",  "Lulu's Noodle Shop",  "Burger Stand",  "Artego Pizza",  "Jade Garden",  "Buca di Beppo",  "Peachtree Buffet",  "Jazz"]

output_low = random.sample(low, k=3)
output_mid = random.sample(mid, k=3)
output_high = random.sample(high, k=3)

message_low = 'Your low priced choices are: '
message_mid = 'Your mid priced choices are: '
message_high = 'Your high priced or far away choices are: '

print(message_low + ', '.join(output_low))
print(message_mid + ', '.join(output_mid))
print(message_high + ', '.join(output_high))

