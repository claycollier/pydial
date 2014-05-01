NOTE: PyDial is currently pre-alpha, and in the middle of being ported from Python 2.7 to Python 3.x. The 2.x client branch basically works; the 2.x server can answer UPnP discovery requests, but doesn't implement the rest of DIAL. The 3.x client/server kit is mid-port and may not be working at any given moment. As of 4/19/14, server discovery was working but other client funcionts hadn't been tested and the server could respond to UPnP discovery requests.

pydial
======

Simple Python client and server for the DIAL protocol.

The DIAL (DIscovery And Launch) protocol enables devices to request display devices on the same LAN/WLAN segment (like smart TVs, Chromecast, and other multimedia devices) to play back media on their behalf. It is used by Google's Chromecast device to stream YouTube, Netflix, Hulu, and other services, allowing you to control playback from a smartphone, tablet, or other computer while displaying content on a large screen.

DIAL is built on top of parts of the UPnP and HTTP protocols. UPnP is used for discovering DIAL-enabled devices on your network segment; HTTP is used for requesting and controlling playback. App developers can build their own protocols for controlling authentication, playback, etc. on top of the DIAL protocol.

PyDial aims at being a simple implementation of the DIAL protocol, suitable for prototyping DIAL-enabled functions on first screen (display device) or second screen (control/client device) devices that understand Python. You can also use it to develop desktop apps that can interact with DIAL devices.

DIAL was developed by Netflix and Google; complete details are available here: http://www.dial-multiscreen.org/

Wikipedia description of the DIAL protocol: http://en.wikipedia.org/wiki/DIscovery_And_Launch

Resources
---------

* The DIAL protocol specification: http://www.dial-multiscreen.org/dial-protocol-specification
* The UPnP device architecture specification: http://www.upnp.org/specs/arch/UPnP-arch-DeviceArchitecture-v1.0-20080424.pdf

Acknowledgements
----------------

Code for the PyDial client code was derived from the PyChromecast project: https://github.com/balloob/pychromecast

Licensing and Legal
-------------------

See the LICENSE file for complete licensing information.

PyDial is distributed under the MIT license.

The following applies to the DIAL protocol:
Copyright © 2012 Netflix, Inc. All rights reserved.

Redistribution and use of the DIAL DIscovery And Launch protocol specification
(the “DIAL Specification”), with or without modification, are permitted 
provided that the following conditions are met:

● Redistributions of the DIAL Specification must retain the above copyright 
notice, this list of conditions and the following disclaimer.

● Redistributions of implementations of the DIAL Specification in source code 
form must retain the above copyright notice, this list of conditions and the 
following disclaimer.

● Redistributions of implementations of the DIAL Specification in binary form 
must include the above copyright notice.  

● The DIAL mark, the NETFLIX mark and the names of contributors to the DIAL 
Specification may not be used to endorse or promote specifications, software, 
products, or any other materials derived from the DIAL Specification without 
specific prior written permission. The DIAL mark is owned by Netflix and 
information on licensing the DIAL mark is available at 
www.dial-multiscreen.org.

THE DIAL SPECIFICATION IS PROVIDED BY NETFLIX, INC. "AS IS" AND ANY EXPRESS OR 
IMPLIED WARRANTIES, INCLUDING, BUT NOT 

LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
PURPOSE AND NONINFRINGEMENT 

ARE DISCLAIMED. IN NO EVENT SHALL NETFLIX OR CONTRIBUTORS TO THE DIAL 
SPECIFICATION BE LIABLE FOR ANY DIRECT, 

INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
OR OTHERWISE) 

ARISING IN ANY WAY OUT OF THE USE OF THE DIAL SPECIFICATION, EVEN IF ADVISED OF
THE POSSIBILITY OF SUCH DAMAGES.


