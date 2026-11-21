---
title: Geodata: GeoPandas and Folium
summary: GeoDataFrames, geometries, buffers, projections and interactive maps.
order: 12
duration: 55 min
difficulty: advanced
tags: geopandas, folium, maps
---

Geodata adds location: points, polygons, CRS and maps.

## GeoDataFrame

```python
import geopandas as gpd
from shapely.geometry import Point

df = gpd.GeoDataFrame(
    {"city": ["Moscow", "SPb"]},
    geometry=[Point(37.6, 55.7), Point(30.3, 59.9)],
    crs="EPSG:4326",
)
```

## Operations

```python
df.geometry.buffer(0.5)
df.geometry.distance(other)
df.to_crs("EPSG:3857")
```

## Folium map

```python
import folium
m = folium.Map(location=[55.75, 37.61], zoom_start=8)
folium.Marker([55.75, 37.61], popup="Moscow").add_to(m)
m.save("map.html")
```

## Lesson summary

GeoPandas for geometry analysis; Folium for interactive maps.

<!--TASK-->
### Task 1 — Points
Create a GeoDataFrame of 3 cities with Point geometry.

### Task 2 — Read file
Read a GeoJSON if available; else create one.

### Task 3 — Buffer
Build buffers around points; print geom_type.

### Task 4 — Distance
Compute distance between two points.

### Task 5 — Projection
Convert to EPSG:3857 and re-check distance.

### Task 6 — Map
Create a Folium map with markers.

### Task 7 — Auto map
Use df.explore() or loop markers from a GeoDataFrame.
<!--/TASK-->

<!--HINT-->
### Hint 1
Point(lon, lat); crs="EPSG:4326".

### Hint 2
gpd.read_file("cities.geojson").

### Hint 3
df.geometry.buffer(0.5).

### Hint 4
df.geometry.iloc[0].distance(df.geometry.iloc[1]).

### Hint 5
df.to_crs("EPSG:3857").

### Hint 6
folium.Map + Marker.

### Hint 7
for row in df.itertuples(): add marker.
<!--/HINT-->

<!--SOLUTION-->
### Solution 1
```python
import geopandas as gpd
from shapely.geometry import Point

df = gpd.GeoDataFrame(
    {"city": ["Moscow", "SPb", "Kazan"]},
    geometry=[Point(37.6, 55.7), Point(30.3, 59.9), Point(49.1, 55.8)],
    crs="EPSG:4326",
)
```

### Solution 2
```python
df = gpd.read_file("cities.geojson")
```

### Solution 3
```python
buffers = df.geometry.buffer(0.5)
print(buffers.geom_type)
```

### Solution 4
```python
d = df.geometry.iloc[0].distance(df.geometry.iloc[1])
print(d)
```

### Solution 5
```python
metric = df.to_crs("EPSG:3857")
print(metric.geometry.iloc[0].distance(metric.geometry.iloc[1]))
```

### Solution 6
```python
import folium
m = folium.Map(location=[55.75, 37.61], zoom_start=6)
folium.Marker([55.75, 37.61], popup="Moscow").add_to(m)
m.save("map.html")
```

### Solution 7
```python
m = folium.Map(location=[55.75, 37.61], zoom_start=6)
for row in df.itertuples():
    folium.Marker([row.geometry.y, row.geometry.x], popup=row.city).add_to(m)
m.save("cities.html")
```
<!--/SOLUTION-->

<!--QUIZ-->
What is a GeoDataFrame?
- DataFrame with geometry
- Normal DataFrame
- Series
- Map
* Correct answer: DataFrame with geometry
Plus crs.

What is Point?
- A geometry
- A city
- A float
- A map
* Correct answer: A geometry
Coordinates.

What is crs?
- Coordinate reference system
- City
- Color
- Size
* Correct answer: Coordinate reference system
Projection.

What does buffer do?
- Creates a zone around geometry
- Deletes
- Moves
- Sorts
* Correct answer: Creates a zone around geometry
Polygon.

What does distance do?
- Distance between geometries
- Area
- Length
- Buffer
* Correct answer: Distance between geometries
In CRS units.

What does to_crs do?
- Reprojects
- Sorts
- Copies
- Crops
* Correct answer: Reprojects
Changes CRS.

What is EPSG:4326?
- Lat/lon degrees
- Meters
- Pixels
- None
* Correct answer: Lat/lon degrees
Geographic.

What is EPSG:3857?
- Web Mercator meters
- Degrees
- Kelvin
- Feet
* Correct answer: Web Mercator meters
Projected.

What does Folium create?
- Interactive HTML maps
- Images
- GeoJSON
- Tables
* Correct answer: Interactive HTML maps
Browser maps.

How to add a marker?
- folium.Marker([lat, lon], popup="...").add_to(m)
- map.add
- marker.add
- plot
* Correct answer: folium.Marker([lat, lon], popup="...").add_to(m)
API.

What is popup?
- Tooltip content
- Location
- Color
- Icon
* Correct answer: Tooltip content
Info on click.

How to save a map?
- m.save("map.html")
- m.write
- m.export
- m.png
* Correct answer: m.save("map.html")
HTML output.
<!--/QUIZ-->
