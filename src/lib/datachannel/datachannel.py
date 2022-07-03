#!/usr/bin/env python3
"""
    Datachannel Client for WebRTC client testing
    
    protocol: SCTP over DTLS
"""

class DatachannelClient:

    def __init__(self, configuration):
        pass


    """ --- methods --- """
    def connect(self):
        pass

    def _negotiate_dtls(self):
        pass

    def close(self):
        pass
    
    def send(self, message):
        pass

    """ --- events --- """
    def on_open(self):
        pass
    
    def on_message(self):
        pass
    
    def on_error(self):
        pass

    def on_close(self):
        pass