#!/usr/bin/python

"""The geo_helper determines zip codes and plots points between two addresses.

Uses geopandas to assemble data and compare with shapely LineString objects.
"""

import matplotlib
matplotlib.use('Agg')

import geopandas as gp
import matplotlib.pyplot as plt

import shapely

ZIP_HEADER = 'ZCTA5CE10'
DPI = 200
GDF = None


def CreateGeoDataFrame():
  """Creates a GeoDataFrame from geopandas."""
  global GDF
  if not GDF:
    GDF = gp.GeoDataFrame.from_file('cb_2013_us_zcta510_500k.shp')


def ProcessRequest(departure, destination):
  """Handles incoming web requests.

  Args:
    departure: A tuple containing an x and y coordinate (x, y)
    destination: A tuple containing an x and y coordinate (x, y)

  Returns:
    A tuple containing the list of zip codes and the path to the
    image generated.
  """
  # Create a shapely line that we will query GeoPandas with.
  line = shapely.geometry.LineString([departure[::-1], destination[::-1]])
  line_gdf = gp.GeoDataFrame([{'geometry': line}])
  intersect_results = GDF['geometry'].intersects(line)
  # Polygon coords for google maps.
  polygon_coords = []
  # A dataframe with only the resulting multipolygon objects to plot
  gdf_results = []
  # list of all zip codes to cross through
  zips = []

  for index, result in enumerate(intersect_results):
    if result:
      zips.append(GDF[ZIP_HEADER][index])
      multi_polygon = GDF['geometry'][index]
      gdf_results.append({'geometry': multi_polygon})
      if isinstance(multi_polygon, shapely.geometry.polygon.Polygon):
        polygon_coords.append(multi_polygon.exterior)
      else:
        # iterate through the multi polygon to get exterior
        for polygon in multi_polygon:
          polygon_coords.append(polygon.exterior)
  results = gp.GeoDataFrame(gdf_results)
  results.plot()  # plot all the zip code polygons.
  line_gdf.plot()  # plot a dataframe with the line
  image_path = '%s.png' % hash(departure + destination)
  plt.savefig(image_path, bbox_inches='tight', dpi=DPI)
  plt.clf()
  return zips, image_path
