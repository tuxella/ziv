#! /usr/bin/python

import drawSVG
import sys
import math

COMPONENTS = "components"
NODES = "nodes"
LINKS = "links"
NODE = "node"
COMPONENT = "component"
GRAPH = "graph"
LINK = "link"
TYPE = "type"
WIDTH = "width"
HEIGHT = "height"
GRID = "grid"
LAYOUT = "layout"
LOGIC = "logic"
ROWS = "rows"
COLUMNS = "columns"
ID = "id"
INNER_MARGIN = "inner_margin"
FILLCOLOR = "fill"
STROKE_WIDTH = "stroke-width"
STROKE = "stroke"
RX = "rx"
X = "x"
Y = "y"
RECTANGLE = "rect"
SHAPE = "shape"

inherited_properties = ["node",
                        "component",
                        "layout"]


def inherit_properties(parent, child):
    if (parent is None) or (child is None):
        return

    for p in parent.keys():
        if p not in child:
            child[p] = parent[p]

    if NODE == child[TYPE]:
        for p in parent[NODE]:
            if p not in child:
                child[p] = parent[p]


def layout_component(c):
    if NODES not in c:
        return c

    if LAYOUT not in c:
        c[LAYOUT] = {LOGIC:GRID}

    l = c[LAYOUT]
    if GRID == l[LOGIC]:
        print "Layouting : GRID"
        if (ROWS not in l) and (COLUMNS not in l):
            print "Both rows and columns are computed"
            rows = int(math.floor(math.sqrt(len(c[NODES]))))
            columns = int(math.ceil(float(len(c[NODES])) / rows))
            l[ROWS] = rows
            l[COLUMNS] = columns
        if ROWS not in l:
            print "Rows computed from columns count"
            rows = int(math.floor(math.sqrt(len(c[NODES]))))
            rows = int(math.ceil(float(len(c[NODES])) / l[COLUMNS]))
            l[ROWS] = rows
        if COLUMNS not in l:
            print "Columns computed from rows count"
            columns = int(math.ceil(float(len(c[NODES])) / l[ROWS]))
            l[COLUMNS] = columns
        print "Layout of component %s : [%d x %d]" % (c[ID], l[ROWS], l[COLUMNS])

        x_offset = c[INNER_MARGIN]
        y_offset = c[INNER_MARGIN]
        row = 0
        col = 0

        rows_nodes = [[] for i in range(0, l[ROWS])]
        columns_nodes = [[] for i in range(0, l[COLUMNS])]

        i = 0
        for n in c[NODES]:
            row = i / l[COLUMNS]
            col = i % l[COLUMNS]
            rows_nodes[row].append(n)
            columns_nodes[col].append(n)
            i = i + 1

        x_offset = c[INNER_MARGIN]
        y_offset = c[INNER_MARGIN]

        for row in rows_nodes:
            max_height = 0
            for n in row:
                if n[HEIGHT] > max_height:
                    max_height = n[HEIGHT]
                n[Y] = y_offset
            y_offset = y_offset + max_height + c[INNER_MARGIN]

        for column in columns_nodes:
            max_width = 0
            for n in column:
                if n[WIDTH] > max_width:
                    max_width = n[WIDTH]
                n[X] = x_offset
            x_offset = x_offset + max_width + c[INNER_MARGIN]


        c[WIDTH] = x_offset + c[INNER_MARGIN]
        c[HEIGHT] = y_offset + c[INNER_MARGIN]

def item_size(i, parent):
    inherit_properties(parent, i)
    if NODE == i[TYPE]:
        return {'width':i[WIDTH],
                'height':i[HEIGHT]}

    if COMPONENT == i[TYPE]:
        layout_component(i)
        return {'width':i[WIDTH],
                'height':i[HEIGHT]}


def set_default_component(c):
    default_properties = {
        TYPE: COMPONENT,
        INNER_MARGIN: 3,
        X: 0,
        Y: 0,
        WIDTH: 50,
        HEIGHT: 50,
        STROKE: "#8fc8ff",
        STROKE_WIDTH:3,
        RX:10,
        SHAPE:RECTANGLE,
        FILLCOLOR: "#DDDDDD"}

    for p, v in default_properties.items():
        if p not in c:
            c[p] = v

def set_default_node(n, n_id):
    default_properties = {
        TYPE: NODE,
        INNER_MARGIN: 3,
        X: 0,
        Y: 0,
        WIDTH: 50,
        HEIGHT: 50,
        SHAPE: RECTANGLE,
        FILLCOLOR: "#EEEEEE",
        STROKE_WIDTH:3,
        STROKE: "#ff8fe6"}
    n[ID] = n_id
    for p, v in default_properties.items():
        if p not in n:
            n[p] = v


def augment_items(components, nodes, links):
    for c in components:
        set_default_component(c)
        nodes_list = []
        for n in c[NODES]:
            nodes_list.append(nodes[n])
        c[NODES] = nodes_list
    for n_id, n in nodes.items():
        set_default_node(n, n_id)
    for l in links:
        l[TYPE] = LINK

def trace_node(n, svg):
    svg.addChildElement(n[SHAPE], n)

def trace_component(c, svg, parent):
    layout_component(c)

    svg.addChildElement(c[SHAPE], c)
    for n in c[NODES]:
        trace_node(n, svg)

def render(g):
    components = g[COMPONENTS] if COMPONENTS in g else []
    nodes = g[NODES] if NODES in g else []
    links = g[LINKS] if LINKS in g else []

    augment_items(components, nodes, links)
    graph = {TYPE:GRAPH}

    my_svg = drawSVG.SVG()

    print "len : %s" % len(components)

    if 0 < len(components):
        for c in components:
            trace_component(c, my_svg, None)

    return my_svg

def main():
    if 3 > len(sys.argv):
        print "Need the name of the file to parse and the output file"
        return 1

    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    graph = eval('%s' % open(input_file_name).read())
    print "graph : ", graph["components"]
    svg = render(graph)
    svg.outputToFile(output_file_name)


if "__main__" == __name__:
    sys.exit(main())
