#!/usr/bin/python
from flask import Flask

from flask import render_template
from flask import request, url_for
from third_party.pygmaps import pygmaps as gmap

import geo_helper

application = Flask(__name__)

@application.route('/')
def index():
  """Main handler that prompts user for departure and destination.

  Valid GET arguments: departure and destination. Processes user 
  request if all necessary information is available. 
  """
  departure = request.args.get('departure')
  destination = request.args.get('destination')

  if departure and destination:
    # User has filled out the form.
    # Note: this data still needs to be validated/sanitized.
    geo_helper.process_request(departure, destination)
  else:
    # Prompt user with form
    return render_template('form.html')


if __name__ == '__main__':
  geo_helper.CreateGeoDataFrame()
  application.debug = True
  application.run(port=5000,host='0.0.0.0')
