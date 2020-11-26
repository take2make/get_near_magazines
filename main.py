import numpy as np
import pandas as pd

data_magazines = pd.read_csv(r'place_zone_coordinates.csv')
data_users = pd.read_csv(r'user_coordinates.csv')
coordinate_magazines = data_magazines[['Latitude', 'Longitude']]

#define radius of delivery area
radius = 1 # 10 km
delivery_radius = list(np.ones(coordinate_magazines.shape[0])*radius)
coordinate_magazines.insert(2, "Delivery", delivery_radius, True)
coordinate_users = data_users[['Latitude', 'Longitude']]

def calculate_distance(lat1, lon1, lat2, lon2, R = 6371):
    lat_1, lon_1, lat_2, lon_2 = np.radians([lat1, lon1, lat2, lon2])
    A = np.power(np.sin((lat_2-lat_1)/2),2)+np.cos(lat_2)*np.cos(lat_1)*np.power(np.sin((lon_2-lon_1)/2),2)
    return 2*R*np.arcsin(np.sqrt(A))

def save_csv(filename):
    with open(filename, 'w') as file:
        file.write("user_id, num_of_available_places, magazines_id\n")
        for user in available_places.keys():
            file.write(f"{user}, {len(available_places[user])}, {available_places[user]}\n")

users = coordinate_users.values
users_num = np.arange(users.shape[0]).reshape(-1,1)
users = np.concatenate((users, users_num), axis=1)

magazines = coordinate_magazines.values
magazines_num = np.arange(magazines.shape[0]).reshape(-1,1)
magazines = np.concatenate((magazines, magazines_num), axis=1)

available_places = {}

for user_lat, user_lon, user in users:
    available_places[user] = []
    distances = np.zeros(magazines.shape[0])
    for mag_lat, mag_lon, r, mag in magazines:
        distances[int(mag)] = calculate_distance(user_lat, user_lon, mag_lat, mag_lon)
        if distances[int(mag)] < r:
            available_places[user].append(int(mag))
    if available_places[user] == []:
        available_places[user] = np.argsort(distances)[0:1]

save_csv("available.csv")