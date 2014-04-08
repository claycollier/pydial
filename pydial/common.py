# This multicast IP and port are specified by the DIAL standard
SSDP_ADDR = "239.255.255.250"
SSDP_PORT = 1900

# This is used during SSDP discovery- servers will wait up to this
# many seconds before replying to prevent flooding
SSDP_MX = 3

# The DIAL search target specified by the protocol
SSDP_ST = "urn:dial-multiscreen-org:service:dial:1"
