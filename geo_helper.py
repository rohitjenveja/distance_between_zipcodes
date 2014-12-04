#!/usr/bin/python


import geopandas as gp

ZIP_HEADER = 'ZCTA5CE10'


def OpenFromGeoDataFrame():
  gf = gp.GeoDataFrame.from_file('cb_2013_us_zcta510_500k.shp')
  home = gf[gf[ZIP_HEADER] =='08540']
  home_two = gf[gf[ZIP_HEADER] =='94114']
  interesction = home.intersection(home_two)


if __name__ == '__main__':
  OpenFromGeoDataFrame()
