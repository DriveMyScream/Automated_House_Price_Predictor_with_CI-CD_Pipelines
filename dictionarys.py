Hospital = {"PD Hinduja Hospital": [19.0332, 72.8391], "Lilavati Hospital": [19.0509, 72.8289], "Breach Candy Hospital": [18.9725, 72.8046],
              "Wockhardt Hospital": [18.9759, 72.8244], "KEM Hospital": [19.0013, 72.8406], "JJ Hospital": [18.9631, 72.8336],
              "Nair Hospital": [18.9727, 72.8212], "SevenHills Hospital": [19.1175, 72.8795], "Nanavati Super Speciality Hospital": [19.0957, 72.8402],
              "Kokilaben Dhirubhai Ambani Hospital": [19.1312, 72.8248]}

Schools = {"St Xavier": [19.1359, 72.9289], "Bombay Scottish": [19.0337, 72.8388], "Don Bosco": [19.0259, 72.8584],
           "Hansraj Morarji Public School": [19.11654, 72.82825], "St Anne":[19.19405, 72.8379]}

Collages = {"KJ.Somaiya College": [19.0723, 72.9002], "Mithibai College": [19.1034, 72.8369], "Ruia College": [19.0237, 72.8502],
            "Jai Hind College": [18.9346, 72.8252], "Narsee Monjee College": [19.10390, 72.8370]}

Street = {"Fashion Street": [19.076, 72.8777], "Bandra Linking Road": [19.0615, 72.8359], "Bandra Hill Road": [19.0555, 72.8322],
         "Colaba Causeway": [18.9218, 72.8347], "Crawford Market": [18.9463, 72.8352], "Malad West": [19.1827, 72.8401],
         "Natraj Market": [19.1152, 72.853], "Hindmata": [19.0062, 72.8405], "Grant Road": [18.9629, 72.81757],
         "Infiniti Mall": [19.1846, 72.8344], "RCity Mall": [19.0996, 72.9162], "Phoenix Marketcity": [19.0865, 72.8888], "Growel Mall": [19.2032, 72.8599] }

Areas = {"South Mumbai": [19.0197, 72.8515], "Bandra": [19.0548, 72.8407], "Juhu": [19.0884, 72.8265], "Powai": [19.1176, 72.906],
         "BKC": [19.0688, 72.8703], "Worli": [18.9986, 72.8174], "Lower Parel": [18.9982, 72.8270], "Andheri West": [19.1364, 72.8296],
         "Goregaon East": [19.1663, 72.8526], "Thane": [19.2183, 72.9781]}

import math
# It will return the distance in km
def haversine_distance(lat1, lon1, lat2, lon2):
  # Convert degree into radian
  lat1_rad = math.radians(lat1)
  lon1_rad = math.radians(lon1)
  lat2_rad = math.radians(lat2)
  lon2_rad = math.radians(lon2)

  dlat = lat2_rad - lat1_rad
  dlon = lon2_rad - lon1_rad
  a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  R = 6371 # Radius of earth in km
  distance = R * c
  return distance


def preprocess(row):
  area,	latitude, longitude, bedrooms, bathrooms, balcony, neworold, parking, furnished_status, lift, type_of_building = row
  Total_Rooms = bedrooms + bathrooms
  Approx_Avg_Area_Per_Room = area / Total_Rooms
  Balcony_Ratio = balcony / bedrooms
  Bathroom_Ratio = bathrooms / bedrooms
  distances = calculates_distance(latitude, longitude)
  features = row + [Total_Rooms, Approx_Avg_Area_Per_Room, Balcony_Ratio, Bathroom_Ratio] + distances
  return features


def process(row):
   if row == 'One':
      return 1.0
   elif row == 'Two':
      return 2.0
   elif row == 'Three':
      return 3.0
   elif row == 'Four':
      return 4.0
   elif row == 'Five':
      return 5.0
   elif row == 'Six':
      return 6.0


def calculates_distance(latitude1, longitude1):
    
    hospital_distance = []
    Schools_distance = []
    Collages_distance = []
    Street_distance = []
    Areas_distance = []
    for key, value in Hospital.items():
        latitude2, longitude2 = value
        distance = haversine_distance(latitude1, longitude1, latitude2, longitude2)
        hospital_distance.append(distance)

    for key, value in Schools.items():
        latitude2, longitude2 = value
        distance = haversine_distance(latitude1, longitude1, latitude2, longitude2)
        Schools_distance.append(distance)

    for key, value in Collages.items():
        latitude2, longitude2 = value
        distance = haversine_distance(latitude1, longitude1, latitude2, longitude2)
        Collages_distance.append(distance)
    
    for key, value in Street.items():
        latitude2, longitude2 = value
        distance = haversine_distance(latitude1, longitude1, latitude2, longitude2)
        Street_distance.append(distance)

    for key, value in Areas.items():
        latitude2, longitude2 = value
        distance = haversine_distance(latitude1, longitude1, latitude2, longitude2)
        Areas_distance.append(distance)
    
    
    distances = hospital_distance + Schools_distance + Collages_distance + Street_distance + Areas_distance

    return distances

def number_to_words(number):
    terms = ["", "thousand", "lakh", "crore"]
    groups = []
    while number:
        number, group = divmod(number, 100)
        groups.append(group)

    words = []
    for i, group in enumerate(groups):
        if group:
            words.append(f"{group} {terms[i]}")

    words.reverse()
    return " ".join(words)