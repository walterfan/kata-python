import unittest
import math
import os
import struct
from dataclasses import dataclass, field
from struct import pack, unpack, unpack_from
from typing import Any, List, Optional, Tuple, Union


RTP_HEADER_LENGTH = 12
RTCP_HEADER_LENGTH = 4

PACKETS_LOST_MIN = -(1 << 23)
PACKETS_LOST_MAX = (1 << 23) - 1

RTCP_SR = 200
RTCP_RR = 201
RTCP_SDES = 202
RTCP_BYE = 203
RTCP_RTPFB = 205
RTCP_PSFB = 206


def load(name: str) -> bytes:
    path = os.path.join(os.path.dirname(__file__), name)
    with open(path, "rb") as fp:
        return fp.read()

class RtcpReportBlock:
    """RTCP Report Block """

    def __init__(self):
        self.base_format = '>LLLLLL'
        self.ssrc = 0 # 32 bits
        self.packets_lost = 0 # 32 bits fraction_lost + cumulative_packets_lost
        self.ext_seqno = 0  # 32 bits
        self.jitter = 0 # 32 bits
        self.lsr = 0 # 32 bits
        self.dlsr = 0 # 32 bits

    def __repr__(self):
        return "ssrc={}, fraction_lost={}, cumulative_packets_lost={}, ext_seqno={}, jitter={}, lsr={}, dlsr={}"\
            .format(self.ssrc, self.get_fraction_lost(), self.get_cumulative_packets_lost(), 
                    self.ext_seqno, self.jitter, self.lsr, self.dlsr)

    def pack(self):
        return struct.pack(self.base_format, self.ssrc, self.packets_lost,
                           self.ext_seqno, self.jitter, self.lsr, self.dlsr)

    def get_fraction_lost(self):
        return self.packets_lost >> 24 >> 8

    def get_cumulative_packets_lost(self):
        return self.packets_lost & 0xfff


class RtcpReportBlocks:
    def __init__(self):
        self.count = 0
        self.blocks = []

    def unpack(self, rtcpPacket):
        self.count = rtcpPacket.vpc & 0x1F
        packet_len = rtcpPacket.len_bytes()
        for i in range(self.count):
            pos = i * 24
            block = RtcpReportBlock()
            block.ssrc, block.packets_lost, block.ext_seqno, block.jiter, block.lsr, block.dlsr \
                = struct.unpack('>LLLLLL', rtcpPacket.payload[pos:24])
            self.blocks.append(block)
    
    def __repr__(self):
        out = ""
        for block in self.blocks:
            out = out + repr(block) + "\n"
        return out

class RtcpRrPacket:
    """RTCP packet"""

    """
            0                   1                   2                   3
            0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
     header |V=2|P|    RC   |   PT=RR=201   |             length            |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |                     SSRC of packet sender                     |
            +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
     report |                 SSRC_1 (SSRC of first source)                 |
     block  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       1    | fraction lost |       cumulative number of packets lost       |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |           extended highest sequence number received           |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |                      interarrival jitter                      |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |                         last SR (LSR)                         |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
            |                   delay since last SR (DLSR)                  |
            +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
     report |                 SSRC_2 (SSRC of second source)                |
     block  +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
       2    :                               ...                             :
            +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
            |                  profile-specific extensions                  |
            +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

    """
    def __init__(self, sender_ssrc, num_blocks):
        self.base_format = '>BBHL{payload}s'
        self.vpc = 0x80
        self.type = 201
        self.len =  6 + (num_blocks * 6)
        self.ssrc = sender_ssrc
        self.payload = ''

    @staticmethod
    def parse(data):
        pos = 0
        packets = []

        while pos < len(data):
            if len(data) < pos + RTCP_HEADER_LENGTH:
                raise ValueError(
                    f"RTCP packet length is less than {RTCP_HEADER_LENGTH} bytes"
                )

            v_p_count, packet_type, length = unpack("!BBH", data[pos : pos + 4])
            version = v_p_count >> 6
            padding = (v_p_count >> 5) & 1
            count = v_p_count & 0x1F
            if version != 2:
                raise ValueError("RTCP packet has invalid version")
            pos += 4

            end = pos + length * 4
            if len(data) < end:
                raise ValueError("RTCP packet is truncated")
            payload = data[pos:end]
            pos = end

            if padding:
                if not payload or not payload[-1] or payload[-1] > len(payload):
                    raise ValueError("RTCP packet padding length is invalid")
                payload = payload[0 : -payload[-1]]

            rrPacket = RtcpRrPacket()
            rrPacket.vpc = v_p_count
            


            packets.append(RtcpRrPacket.parse(payload, count))


        return packets

class RtcpPacketTest(unittest.TestCase):

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()