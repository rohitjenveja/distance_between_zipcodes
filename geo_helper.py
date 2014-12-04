#!/usr/bin/python

# Needs to be put at the top, unless X display is specified.
import matplotlib
matplotlib.use('Agg')

import geopandas as gp
import matplotlib.pyplot as plt

ZIP_HEADER = 'ZCTA5CE10'
DPI = 200
GDF = None


def CreateGeoDataFrame():
  """Creates a GeoDataFrame from geopandas."""
  global GDF
  if not GDF:
    GDF = gp.GeoDataFrame.from_file('cb_2013_us_zcta510_500k.shp')
  # GDF.to_crs(GDF.crs, inplace=True)  
  # plt.xticks(rotation=90)

def PlotPoints(zip_code):
  series = GDF[GDF[ZIP_HEADER] == zip_code]
  series.plot()



if __name__ == '__main__':
  # Usually, this file is imported as a module. However,
  # it can be run from command line  interface as well.
  CreateGeoDataFrame()
  
  # PlotPoints('94114')
  # PlotPoints('08540')

  # plt.savefig('nyc.png', dpi=DPI, bbox_inches='tight')