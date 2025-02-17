import numpy as np
from sklearn.cluster import DBSCAN
import random
import folium
from datetime import datetime

"""
def generate_data_around(center, num_points, variance):
    return [[center[0] + np.random.normal(0, variance), center[1] + np.random.normal(0, variance)] for _ in range(num_points)]

centers = [
    [47.0, 2.0],  # Zone résidentielle
    [47.005, 2.005],  # Zone commerciale
    [46.995, 1.995],  # Parc
    [47.002, 2.002],  # Quartier de vie nocturne
    [46.985, 1.990],  # Zone industrielle
]

num_points_per_zone = [100, 150, 50, 120, 10]

variance = 0.001

data = []
for center, num_points in zip(centers, num_points_per_zone):
    data.extend(generate_data_around(center, num_points, variance))

# print(len(data), data )

map = folium.Map(location=[47.0, 2.0], zoom_start=13)

for lat, lon in data:
    folium.CircleMarker(location=[lat, lon], radius=2, color='red').add_to(map)



new_data = []


def dbscan(data, eps, min_samples):
    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(data)
    labels = clustering.labels_
    unique_labels = set(labels)
    representative_point = []
    for label in unique_labels:
        if label != -1:
            indices = [i for i, l in enumerate(labels) if l == label]
            new_data.append(len(indices))
            cluster_mean = np.mean(data[indices], axis=0)
            representative_point.append(cluster_mean.tolist())
    return representative_point


for lat,lon in dbscan(np.array(data), 0.002, 3):
    folium.CircleMarker(location=[lat, lon], radius=2, color='blue').add_to(map)
"""

def cluster(markers_list, eps=0.002, min_samples=3):
    for marker in markers_list:
        marker['time'] = datetime.strptime(marker['time'], '%Y-%m-%d %H:%M:%S')

    grouped_markers = {}
    for marker in markers_list:
        incident_type = marker["incident_type"]
        if incident_type in grouped_markers:
            grouped_markers[incident_type].append(marker)
        else:
            grouped_markers[incident_type] = [marker]

    def cluster_by_incident_type(markers):
        coords = np.array([[marker["lat"], marker["long"]] for marker in markers])
        clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(coords)
        labels = clustering.labels_

        clusters = {}

        for label, marker in zip(labels, markers):
            if label != -1:
                if label in clusters:
                    clusters[label]['coords'].append([marker['lat'], marker['long']])

                    if marker['time'] > clusters[label]['time']:
                        clusters[label]['time'] = marker['time']
                else:
                    clusters[label] = {
                        'coords': [[marker['lat'], marker['long']]],
                        'incident_type': marker['incident_type'],
                        'time': marker['time'],
                        'count': 0
                    }

        for label in clusters:
            mean_lat, mean_long = np.mean(clusters[label]['coords'], axis=0)
            clusters[label]['lat'] = mean_lat
            clusters[label]['long'] = mean_long
            del clusters[label]['coords']
            clusters[label]['count'] = sum([1 for l in labels if l == label])
            clusters[label]['time'] = clusters[label]['time'].strftime('%Y-%m-%d %H:%M:%S')

        return list(clusters.values())

    clustered_markers = []
    for incident_type, markers in grouped_markers.items():
        clustered_markers.extend(cluster_by_incident_type(markers))

    return clustered_markers


"""
print(new_data)
map.save('map.html')
"""