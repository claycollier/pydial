import socketserver
import socket
import struct
import time
import platform
import random
import uuid

from .common import (SSDP_PORT, SSDP_ADDR, SSDP_ST)

UPNP_SEARCH = 'M-SEARCH * HTTP/1.1'
# If we get a M-SEARCH with no or invalid MX value, wait up
# to this many seconds before responding to prevent flooding
CACHE_DEFAULT = 1800
DELAY_DEFAULT = 10
PRODUCT = 'PyDial Server'
VERSION = '0.01'

SSDP_REPLY = 'HTTP/1.1 200 OK\r\n' + \
               'LOCATION: {}\r\n' + \
               'CACHE-CONTROL: max-age={}\r\n' + \
               'EXT:\r\n' + \
               'BOOTID.UPNP.ORG: 1\r\n' + \
               'SERVER: {}/{} UPnP/1.1 {}/{}\r\n' + \
               'ST: {}\r\n'.format(SSDP_ST) + \
               'DATE: {}\r\n' + \
               'USN: {}\r\n' + '\r\n'


class SSDPHandler(socketserver.BaseRequestHandler):
     """
     RequestHandler object to deal with DIAL UPnP search requests.

     Note that per the SSD protocol, the server will sleep for up
     to the number of seconds specified in the MX value of the 
     search request- this may cause the system to not respond if
     you are not using the multi-thread or forking mixin.
     """
     def __init__(self, request, client_address, server):
          socketserver.BaseRequestHandler.__init__(self, request, 
                         client_address, server)
          self.max_delay = DELAY_DEFAULT

     def handle(self):
          """
          Reads data from the socket, checks for the correct
          search parameters and UPnP search target, and replies
          with the application URL that the server advertises.
          """
          data = str(self.request[0], 'utf-8')
          data = data.strip().split('\r\n')
          if data[0] != UPNP_SEARCH:
               return
          else:
               dial_search = False
               for line in data[1:]:
                    field, val = line.split(':', 1)
                    if field.strip() == 'ST' and val.strip() == SSDP_ST:
                         dial_search = True
                    elif field.strip() == 'MX':
                         try:
                              self.max_delay = int(val.strip())
                         except ValueError:
                              # Use default
                              pass
               if dial_search:
                    self._send_reply()

     def _send_reply(self):
          """Sends reply to SSDP search messages."""
          time.sleep(random.randint(0, self.max_delay))
          _socket = self.request[1]
          timestamp = time.strftime("%A, %d %B %Y %H:%M:%S GMT", 
                    time.gmtime())
          reply_data = SSDP_REPLY.format(self.server.device_url,
                    self.server.cache_expire, self.server.os_id,
                    self.server.os_version, self.server.product_id,
                    self.server.product_version, timestamp, "uuid:"+str(self.server.uuid))

          sent = 0
          while sent < len(reply_data):
               sent += _socket.sendto(bytes(reply_data, 'utf-8'), self.client_address)

class SSDPServer(socketserver.UDPServer):
     """
     Inherits from SocketServer.UDPServer to implement the SSDP
     portions of the DIAL protocol- listening for search requests
     on port 1900 for messages to the DIAL multicast group and 
     replying with information on the URL used to request app
     actions from the server.

     Parameters:
          -device_url: Absolute URL of the device being advertised.
          -host: host/IP address to listen on

     The following attributes are set by default, but should be
     changed if you want to use this class as the basis for a 
     more complete server:
     product_id - Name of the server/product. Defaults to PyDial Server.
     product_version - Product version. Defaults to whatever version
          number PyDial was given during the last release.
     os_id - Operating system name. Default: platform.system()
     os_version - Operating system version. Default: platform.release().
     cache_expire - Time (in seconds) before a reply/advertisement expires.
          Defaults to 1800.
     uuid - UUID. By default created from the NIC via uuid.uuid1()
     """
     def __init__(self, device_url, host=''):
          socketserver.UDPServer.__init__(self, (host, SSDP_PORT), 
                    SSDPHandler, False)
          self.allow_reuse_address = True
          self.server_bind()
          mreq = struct.pack("=4sl", socket.inet_aton(SSDP_ADDR),
                                       socket.INADDR_ANY)
          self.socket.setsockopt(socket.IPPROTO_IP, 
                    socket.IP_ADD_MEMBERSHIP, mreq)
          self.device_url = device_url
          self.product_id = PRODUCT
          self.product_version = VERSION
          self.os_id = platform.system()
          self.os_version = platform.release()
          self.cache_expire = CACHE_DEFAULT
          self.uuid = uuid.uuid1()

     def start(self):
          self.serve_forever()

class DialServer(object):
     def __init__(self):
          pass

     def add_app(self, app_id, app_path):
          pass
