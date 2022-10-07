#!/usr/bin/env python3
"""
draw flow chart as a simple string

apt install graphviz
pip install graphviz

refer to 
 - https://graphviz.readthedocs.io/en/stable/manual.html
 - https://graphviz.org/doc/info/lang.html
 - https://graphviz.org/doc/info/shapes.html
"""
from IPython.display import display, Image

from graphviz import Digraph
from graphviz import Source

g_node_id = 0
g_node_map = {}

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def get_node_id(node_name):
    global g_node_map
    global g_node_id
    
    node_id = g_node_map.get(node_name)
    if not node_id:
        g_node_id += 1
        node_id = g_node_id
        g_node_map[node_name]= node_id
    return "node_{}".format(node_id)


def draw_flow_chart(flow_content):
    flow = Digraph('video-flow', comment='WebRTC Video Flow', node_attr={'shape': 'box'})  

    start_node = flow.node("start", label="start", shape='ellipse')
    end_node = flow.node("end", label="end",  shape='ellipse')

    call_nodes = flow_content.split("\n")
    previous_node_id = None
    for call_node in call_nodes:
        if not previous_node_id:
            previous_node_id = "start"
        
        node_text = call_node.strip()
        if not node_text:
            continue
            
        node_name = remove_prefix(node_text, "->").strip()
        node_id = get_node_id(node_name)
        
        node_shape = "box"
        if node_name.startswith("if") or node_name.endswith("?"):
            node_shape = "diamond"
            
        flow.node(node_id, label=node_name, shape=node_shape)
        
        if node_text.startswith("->") or previous_node_id == "start":
            flow.edge(previous_node_id, node_id)
        
        previous_node_id = node_id

    flow.edge(previous_node_id, "end")
    
    return flow


rtp_receive_flow = """
->call::DeliverPacket(...)
->Call::DeliverRtp(...)
->Call::IdentifyReceivedPacket(...)
->video_receiver_controller_.OnRtpPacket(parsed_packet))
->demuxer_.OnRtpPacket(packet)
->RtpDemuxer::ResolveSink(packet)
"""

flow = draw_flow_chart(rtp_receive_flow)

print(flow.source)

flow.render(directory='.', view=True,  format='png')

