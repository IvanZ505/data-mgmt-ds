import csv
import math
from collections import Counter

# Q1 Pt.1
total_fire = 0
total_f40 = 0
with open("pokemonTrain.csv", "r") as file:
    reader = csv.DictReader(file)
    for line in reader:
        if line['type'] == "fire":
            total_fire+=1
            if float(line['level']) >= 40.0:
                total_f40+=1

    #print(total_fire, total_f40)


with open("pokemon1.txt", "w") as file:
    file.write(f'Percentage of fire type Pokemons at or above level 40 = {round((total_f40/total_fire)*100)}')

# Q1 Pt.2
pokemans = []
with open("pokemonTrain.csv", "r") as file:
    reader = csv.DictReader(file)
    for line in reader:
        pokemans.append(line)

# The type mapping is a mapping of keys as the weakness, the values as the one that the NaN types will map to.
pokeman_weakness_type = set([x['weakness'] for x in pokemans if x['type'] != "NaN"])
type_mapping = dict.fromkeys(pokeman_weakness_type)
#print(type_mapping)
for i in type_mapping.keys():
    weakness_count = Counter([x['type'] for x in pokemans if x['weakness'] == i and x['type'] != "NaN"])
    sorted_alphabetically = {key: weakness_count[key] for key in sorted(weakness_count.keys())}
    implied_type = max(sorted_alphabetically, key=sorted_alphabetically.get)
    type_mapping[i] = implied_type
    #print(i, weakness_count, implied_type)

#print(type_mapping)

#print([x for x in pokemans if x["name"] == "Magmar"])

# Q1 Pt.3
stats_g40_aggr = {'atk': [float(x['atk']) for x in pokemans if float(x['level']) > 40 and x['atk'] != "NaN"], 
             'def': [float(x['def']) for x in pokemans if float(x['level']) > 40 and x['def'] != "NaN"], 
             'hp': [float(x['hp']) for x in pokemans if float(x['level']) > 40 and x['hp'] != "NaN"]}
stats_le40_aggr = {'atk': [float(x['atk']) for x in pokemans if float(x['level']) <= 40 and x['atk'] != "NaN"], 
             'def': [float(x['def']) for x in pokemans if float(x['level']) <= 40 and x['def'] != "NaN"], 
             'hp': [float(x['hp']) for x in pokemans if float(x['level']) <= 40 and x['hp'] != "NaN"]}

stats_g40 = {x: round(sum(y)/len(y),1) for x,y in stats_g40_aggr.items()}
stats_le40 = {x: round(sum(y)/len(y),1) for x,y in stats_le40_aggr.items()}
#print(stats_g40, stats_le40)
for poke in pokemans:
    if poke['type'] == "NaN":
        poke['type'] = type_mapping[poke['weakness']]
    if poke['atk'] == "NaN":
        poke['atk'] = stats_g40['atk'] if float(poke['level']) > 40 else stats_le40['atk']
    if poke['def'] == "NaN":
        poke['def'] = stats_g40['def'] if float(poke['level']) > 40 else stats_le40['def']
    if poke['hp'] == "NaN":
        poke['hp'] = stats_g40['hp'] if float(poke['level']) > 40 else stats_le40['hp']

with open("pokemonResult.csv", "w", newline="") as file:
    writer = csv.writer(file)
    heading = [k for k in pokemans[0].keys()]
    writer.writerow(heading)
    for line in pokemans:
        a = [v for _,v in line.items()]
        #print(a)
        writer.writerow(a)

# Q1 Pt.4 and 5
hp_aggr, cnt = 0, 0
personality_dict = {}
with open("pokemonResult.csv", "r") as file:
    reader = csv.DictReader(file)
    for line in reader:
        # Pt.5
        if float(line['stage']) == 3.0:
            hp_aggr += float(line['hp'])
            cnt += 1

        # Pt.4
        personality_dict.setdefault(line['type'], [])
        personality_dict[line['type']].append(line['personality'])

personality_dict = {k: sorted(v) for k,v in sorted(personality_dict.items(), key=lambda x:x[0])}

with open("pokemon4.txt", "w") as file:
    for k,v in personality_dict.items():
        file.write(f'{k}: {', '.join(v)}\n')


#print("\nPersonality:", personality_dict)

with open("pokemon5.txt", "w") as file:
    file.write(f'Average hit point for Pokemons of stage 3.0 = {round(hp_aggr/cnt)}')

