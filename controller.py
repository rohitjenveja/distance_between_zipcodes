#!/usr/bin/python

"""The controller that renders HTML templates."""

__author__ = ("Rohit Jenveja - rjenveja@gmail.com")

from flask import Flask
from flask import make_response
from flask import render_template
from flask import request, url_for

import geo_helper

import logging

from pygeocoder import Geocoder
import shapely
from third_party.pygmaps import pygmaps as gmap


application = Flask(__name__)


class Error(Exception):
  """Base error class from which all other exceptions inherit from."""

class InvalidAddress(Error):
  """Raised if a user enters an invalid address."""


@application.route('/')
def index():
  """Main handler that prompts user for departure and destination.

  Valid GET arguments:
    departure: The full address from which to depart.
    destination: The desired destination.

  Processes user request if all necessary information is available.
  If an invalid address is passed, HandleException is called and may
  raise an exception or ask the user to try again.
  """
  departure, destination = (
      request.args.get('departure'), request.args.get('destination'))
  geo_data = {}
  # Use pygeocoder to validate and get precise longitude and latitude.
  if departure and destination:
    departure = Geocoder.geocode(request.args.get('departure'))
    destination = Geocoder.geocode(request.args.get('destination'))
    logging.info("Depature: %s", departure)
    logging.info("Destination: %s", destination)

    if departure.valid_address and destination.valid_address:
      # Process the request and return a dict to populate in to the template.
      geo_data = {
                  'departure': departure.formatted_address,
                  'destination': destination.formatted_address,
                  'departure_coordinates': departure.coordinates,
                  'destination_coordinates': destination.coordinates,
                 }
      zips, image_path = geo_helper.ProcessRequest(
          departure.coordinates,
          destination.coordinates)
      geo_data["zip_codes"] = zips
      geo_data["image_path"] = image_path
    else:
      # If in dev mode, raise the exception. Otherwise, show form.html.
      HandleException(InvalidAddress, "User has entered an invalid address.",
                      'form.html')
  # Prompt user with form
  return render_template('form.html', geo_data=geo_data)


@application.route("/images/<path:path>")
def images(path):
  """Loads images from local file system."""
  fullpath = "./" + path
  resp = make_response(open(fullpath).read())
  resp.content_type = "image/png"
  return resp


def HandleException(exception_to_raise, error_reason, template):
  """Logic to determine how to display the exception to end-user.

  Args:
    exception_to_raise: The exception class that will be raised.
    error_reason: The text to pass in to the exception class or template.
    template: The HTML text to display, if not in debug mode.

  Returns:
    A rendered template if we are not in debug mode.

  Raises:
    An exception that occurred earlier in the stack, if in debug mode.
  """

  if application.debug:
    raise exception_to_raise(error_reason)
  else:
    render_template(template, error_happened=error_reason)


if __name__ == '__main__':
  # Load the GeoDataFrame in to memory prior to starting server.
  geo_helper.CreateGeoDataFrame()
  application.debug = True
  application.run(port=5000,host='0.0.0.0')
