import re
import csv
from collections import Counter

# Q2 Pt.1
data = []
with open("covidTrain.csv", "r") as file:
    reader = csv.DictReader(file)
    for line in reader:
        data.append(line)

# Q2 Pt.2
prov_aggr = {}
for pt in data:
    if re.search("-", pt['age']):
        tmp = re.split("-", pt['age'])
        pt['age'] = round((float(tmp[0]) + float(tmp[1]))/2)

    onset_tmp = re.split(r"\.", pt['date_onset_symptoms'])
    #print(onset_tmp)
    admission_tmp = re.split(r"\.", pt['date_admission_hospital'])
    conf_tmp = re.split(r"\.", pt['date_confirmation'])

    pt['date_onset_symptoms'] = f'{onset_tmp[1]}.{onset_tmp[0]}.{onset_tmp[2]}'
    pt['date_admission_hospital'] = f'{admission_tmp[1]}.{admission_tmp[0]}.{admission_tmp[2]}'
    pt['date_confirmation'] = f'{conf_tmp[1]}.{conf_tmp[0]}.{conf_tmp[2]}'

    # Used for pt.3
    prov_aggr.setdefault(pt['province'], {'lat':[], 'long':[]})
    if pt['latitude'] != "NaN":
        prov_aggr[pt['province']]['lat'].append(float(pt['latitude']))
    if pt['longitude'] != "NaN":
        prov_aggr[pt['province']]['long'].append(float(pt['longitude']))

# Q2 Pt.3
prov_avgs = {k: {'lat': round(sum(v['lat'])/len(v['lat']), 2), 
                 'long': round(sum(v['long'])/len(v['long']), 2)} for k, v in prov_aggr.items()}

#print(prov_avgs)

for pt in data:
    if pt['latitude'] == "NaN":
        pt['latitude'] = prov_avgs[pt['province']]['lat']
    if pt['longitude'] == "NaN":
        pt['longitude'] = prov_avgs[pt['province']]['long']

    #print(pt['latitude'], pt['longitude'])

# Q2 Pt.4
provinces_uniq = set([x['province'] for x in data])
prov_city_dict = dict.fromkeys(provinces_uniq)

for i in prov_city_dict.keys():
    city_count = Counter([x['city'] for x in data if x['province'] == i and x['city'] != "NaN"])
    sorted_alphabetically = {key: city_count[key] for key in sorted(city_count.keys())}
    implied_city = max(sorted_alphabetically, key=sorted_alphabetically.get)
    prov_city_dict[i] = implied_city
    #print(i, city_count, implied_city)

for pt in data:
    if pt['city'] == "NaN":
        pt['city'] = prov_city_dict[pt['province']]

# Q2 Pt.5
prov_symptom_dict = dict.fromkeys(provinces_uniq)

# Create dict for top symptoms
for i in prov_symptom_dict.keys():
    symptom_count = Counter([y for x in data if x['province'] == i and x['symptoms'] != "NaN" for y in re.split(r'[\s]*;[\s]*', x['symptoms'])])
    sorted_alphabetically = {key: symptom_count[key] for key in sorted(symptom_count.keys())}
    implied_symptoms = max(sorted_alphabetically, key=sorted_alphabetically.get)
    prov_symptom_dict[i] = implied_symptoms
    #print(i, symptom_count, implied_symptoms)

for pt in data:
    if pt['symptoms'] == "NaN":
        pt['symptoms'] = prov_symptom_dict[pt['province']]

with open("covidResult.csv", "w", newline='') as file:
    header = [k for k,_ in data[0].items()]
    writer = csv.writer(file)
    writer.writerow(header)
    for line in data:
        a = [v for _,v in line.items()]
        #print(a)
        writer.writerow(a)

        