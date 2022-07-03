import math
import os
import struct
from dataclasses import dataclass, field
from struct import pack, unpack, unpack_from
from typing import Any, List, Optional, Tuple, Union


"""
example from https://github.com/aiortc/aiortc/blob/main/src/aiortc/rtp.py
"""

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


def pack_rtcp_packet(packet_type: int, count: int, payload: bytes) -> bytes:
    assert len(payload) % 4 == 0
    return pack("!BBH", (2 << 6) | count, packet_type, len(payload) // 4) + payload


def pack_packets_lost(count: int) -> bytes:
    return pack("!l", count)[1:]


def unpack_packets_lost(d: bytes) -> int:
    if d[0] & 0x80:
        d = b"\xff" + d
    else:
        d = b"\x00" + d
    return unpack("!l", d)[0]




@dataclass
class RtcpReceiverInfo:
    ssrc: int
    fraction_lost: int
    packets_lost: int
    highest_sequence: int
    jitter: int
    lsr: int
    dlsr: int

    def __bytes__(self) -> bytes:
        data = pack("!LB", self.ssrc, self.fraction_lost)
        data += pack_packets_lost(self.packets_lost)
        data += pack("!LLLL", self.highest_sequence, self.jitter, self.lsr, self.dlsr)
        return data

    @classmethod
    def parse(cls, data: bytes):
        ssrc, fraction_lost = unpack("!LB", data[0:5])
        packets_lost = unpack_packets_lost(data[5:8])
        highest_sequence, jitter, lsr, dlsr = unpack("!LLLL", data[8:])
        return cls(
            ssrc=ssrc,
            fraction_lost=fraction_lost,
            packets_lost=packets_lost,
            highest_sequence=highest_sequence,
            jitter=jitter,
            lsr=lsr,
            dlsr=dlsr,
        )


@dataclass
class RtcpRrPacket:
    ssrc: int
    reports: List[RtcpReceiverInfo] = field(default_factory=list)

    def __bytes__(self) -> bytes:
        payload = pack("!L", self.ssrc)
        for report in self.reports:
            payload += bytes(report)
        return pack_rtcp_packet(RTCP_RR, len(self.reports), payload)

    @classmethod
    def parse(cls, data: bytes, count: int):
        if len(data) != 4 + 24 * count:
            raise ValueError("RTCP receiver report length is invalid")

        ssrc = unpack("!L", data[0:4])[0]
        pos = 4
        reports = []
        for r in range(count):
            reports.append(RtcpReceiverInfo.parse(data[pos : pos + 24]))
            pos += 24
        return cls(ssrc=ssrc, reports=reports)
    

@dataclass
class RtcpByePacket:
    pass

@dataclass
class RtcpPsfbPacket:
    pass

@dataclass
class RtcpRtpfbPacket:
    pass

@dataclass
class RtcpSdesPacket:
    pass

@dataclass
class RtcpSrPacket:
    pass

AnyRtcpPacket = Union[
    RtcpByePacket,
    RtcpPsfbPacket,
    RtcpRrPacket,
    RtcpRtpfbPacket,
    RtcpSdesPacket,
    RtcpSrPacket,
]


class RtcpPacket:
    @classmethod
    def parse(cls, data: bytes) -> List[AnyRtcpPacket]:
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

            if packet_type == RTCP_RR:
                packets.append(RtcpRrPacket.parse(payload, count))


        return packets