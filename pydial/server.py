import SocketServer
import socket
import struct

from .common import (SSDP_PORT, SSDP_ADDR)

ANY = '0.0.0.0'

class SSDPHandler(SocketServer.BaseRequestHandler):
          def handle(self):
               data = self.request[0].strip()
               socket = self.request[1]
               print "{} wrote:".format(self.client_address[0])
               print data

class SSDPServer(SocketServer.UDPServer):
     def __init__(self, host='localhost', port=SSDP_PORT):
          SocketServer.UDPServer.__init__(self, (host, port), SSDPHandler, False)
          self.allow_reuse_address(True)
          self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
          # FIXME: 4sl or 4sI?
          mreq = struct.pack("4sl", socket.inet_aton(SSDP_ADDR),
                                       socket.INADDR_ANY)
          self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

     def start(self):
          self.serve_forever()

class DialServer(object):
     pass

     def __init__(self):
          pass

     def add_app(self, app_id, app_path):
          pass

