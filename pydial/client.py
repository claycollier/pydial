"""
Module that implements a basic DIAL protocol client.
Usage:
     import pydial
     servers = pydial.discover()
     client = pydial.DialClient(servers[0])
     device = client.get_device_description()
     client.launch_app('YouTube')

Based on code from PyChromecast - https://github.com/balloob/pychromecast
"""

import select
import socket
import requests
from urlparse import urlparse
import datetime as dt
from contextlib import closing
import xml.etree.ElementTree as ET
from collections import namedtuple

from .common import (SSDP_ADDR, SSDP_PORT, SSDP_MX, SSDP_ST)

# Wait at least one second past the SSDP_MX to give servers a chance to respond
DISCOVER_TIMEOUT = SSDP_MX + 1

SSDP_REQUEST = 'M-SEARCH * HTTP/1.1\r\n' + \
                  'HOST: {}:{:d}\r\n'.format(SSDP_ADDR, SSDP_PORT) + \
                  'MAN: "ssdp:discover"\r\n' + \
                  'MX: {:d}\r\n'.format(SSDP_MX) + \
                  'ST: {}\r\n'.format(SSDP_ST) + \
                  '\r\n'


_BASE_URL = "http://{}:{}{}"
DeviceStatus = namedtuple("DeviceStatus",
                          ["friendly_name", "model_name",
                           "manufacturer", "api_version"])

AppStatus = namedtuple("AppStatus", ["app_id", "description", "state",
                                     "options", "service_url",
                                     "service_protocols"])

# Device status XML constants
XML_NS_UPNP_DEVICE = "{urn:schemas-upnp-org:device-1-0}"
XML_NS_DIAL = "{urn:dial-multiscreen-org:schemas:dial}"
XML_NS_CAST = "{urn:chrome.google.com:cast}"

class DialClient(requests.Session):
     """Client for easily sending DIAL requests to a server."""
     def __init__(self, device_url):
          requests.Session.__init__(self)
          url = urlparse(device_url)
          self.dev_host = url.hostname
          self.dev_port = url.port
          self.dev_descrip_path = url.path
          self.app_path = None
          self.app_host = None
          self.app_port = None

     def _craft_app_url(self, app_id=None):
          """ Helper method to create a ChromeCast url given
          a host and an optional app_id. """
          url = _BASE_URL.format(self.app_host, self.app_port, self.app_path)
          if app_id is not None:
               return url + app_id
          else:
               return url
     def get_app_status(self, appid=None):
          """Returns the status of the requested app as a named tuple."""
          if not self.app_path:
               raise AttributeError('Uninitialized application URL.')

          url = _BASE_URL.format(self.app_host, self.app_port, self.app_path) \
                    + appid
          req = requests.Request('GET', url).prepare()
          response = self.send(req)

          # FIXME: Raise an exception here?
          # TODO: Look for 404 in case app is not present
          if response.status_code == 204:
               return None

          status_el = ET.fromstring(response.text.encode("UTF-8"))
          options = status_el.find(XML_NS_DIAL + "options").attrib

          app_id = _read_xml_element(status_el, XML_NS_DIAL,
                                   "name", "Unknown application")

          state = _read_xml_element(status_el, XML_NS_DIAL,
                                  "state", "unknown")

          service_el = status_el.find(XML_NS_CAST + "servicedata")

          if service_el is not None:
               service_url = _read_xml_element(service_el, XML_NS_CAST,
                                            "connectionSvcURL", None)

               protocols_el = service_el.find(XML_NS_CAST + "protocols")

               if protocols_el is not None:
                    protocols = [el.text for el in protocols_el]
               else:
                    protocols = []

          else:
               service_url = None
               protocols = []

          activity_el = status_el.find(XML_NS_CAST + "activity-status")
          if activity_el is not None:
               description = _read_xml_element(activity_el, XML_NS_CAST,
                                            "description", app_id)
          else:
               description = app_id

          return AppStatus(app_id, description, state, options, service_url, protocols)


     def launch_app(self, appid, args=None):
          if not self.app_path:
               raise AttributeError('Uninitialized application URL.')

          url = _BASE_URL.format(self.app_host, self.app_port, self.app_path) \
                    + appid
          header = ''
          if not args:
               header = 'Content-Length: 0'
          req = requests.Request('POST', url, data=args, headers=header)
          prepped = req.prepare()
          response = self.send(prepped)
          print response

     def quit_app(self, app_id=None):
          """ Quits specified application if it is running.
          If no app_id specified will quit current running app. """

          if not app_id:
               status = self.get_app_status(app_id)

          if status:
               app_id = status.app_id

          if app_id:
               self.delete(self._craft_app_url(app_id))

     def get_device_description(self):
          """ Returns the device status as a named tuple. Initializes the
          app path if not initialized."""
          # FIXME: Error handling? Probably should throw errors up.
          try:
               req = self.get(_BASE_URL.format(self.dev_host, self.dev_port, \
                    self.dev_descrip_path))

               # TODO: Make sure this is case insensitive
               if not self.app_path:
                    app_url = urlparse(req.headers['application-url'])
                    self.app_host = app_url.hostname
                    self.app_port = app_url.port
                    self.app_path = app_url.path

               status_el = ET.fromstring(req.text.encode("UTF-8"))

               device_info_el = status_el.find(XML_NS_UPNP_DEVICE + "device")
               api_version_el = status_el.find(XML_NS_UPNP_DEVICE + "specVersion")

               friendly_name = _read_xml_element(device_info_el, XML_NS_UPNP_DEVICE,
                                          "friendlyName", "Unknown device")
               model_name = _read_xml_element(device_info_el, XML_NS_UPNP_DEVICE,
                                       "modelName", "Unknown model name")
               manufacturer = _read_xml_element(device_info_el, XML_NS_UPNP_DEVICE,
                                         "manufacturer",
                                         "Unknown manufacturer")

               api_version = (int(_read_xml_element(api_version_el,
                                             XML_NS_UPNP_DEVICE, "major", -1)),
                       int(_read_xml_element(api_version_el,
                                             XML_NS_UPNP_DEVICE, "minor", -1)))

               return DeviceStatus(friendly_name, model_name, manufacturer,
                            api_version)

          except (requests.exceptions.RequestException, ET.ParseError):
               return None 


def discover(max_devices=None, timeout=DISCOVER_TIMEOUT, verbose=False):
     """
     Sends a message over the network to discover DIAL servers and returns
     a list of found IP addresses.

     Inspired by Crimsdings
     https://github.com/crimsdings/ChromeCast/blob/master/cc_discovery.py
     """
     devices = []

     start = dt.datetime.now()

     with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
          sock.sendto(SSDP_REQUEST, (SSDP_ADDR, SSDP_PORT))
          sock.setblocking(0)

          while True:
               time_diff = dt.datetime.now() - start
               seconds_left = timeout - time_diff.seconds

               if seconds_left <= 0:
                    return devices

               ready = select.select([sock], [], [], seconds_left)[0]

               if ready:
                    response = sock.recv(1024)
                    if verbose:
                         print response
                    found_url = found_st = None
                    headers = response.split("\r\n\r\n", 1)[0]

                    for header in headers.split("\r\n"):
                         try:
                              key, value = header.split(": ", 1)
                         except ValueError:
                              # Skip since not key-value pair
                              continue

                         if key == "LOCATION":
                              found_url = value

                         elif key == "ST":
                              found_st = value

                    if found_st == SSDP_ST and found_url:
                         devices.append(found_url)

                         if max_devices and len(devices) == max_devices:
                              return devices

     return devices


def _read_xml_element(element, xml_ns, tag_name, default=""):
     """ Helper method to read text from an element. """
     try:
          return element.find(xml_ns + tag_name).text

     except AttributeError:
          return default
