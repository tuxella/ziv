#! /usr/bin/python

import drawSVG
import sys
import math

COMPONENTS = "components"
CHILDREN = "children"
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
FLOAT = "float"
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
LAYOUTED = "layouted"
TRACED = "traced"
LABEL = "label"
TEXT_ANCHOR = "text-anchor"
MIDDLE = "middle"
TEXT_TOP_MARGIN = "text-top-margin"
REVERSE = "reverse"
DRIFT = "drift"

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
    if (CHILDREN not in c) or (0 == len(c[CHILDREN])):
        return c

    if c[LAYOUTED]:
        return c

    known_algorithms = [GRID, # Set the inner component on a grid, as square as possible by default
                        FLOAT, # Set the inner components on a grid, then match components containing the same inner components
                        REVERSE, # Sets the position of the component depending on the constrains of the inner components
                        DRIFT, # Used on a second pass to move prevent components from overlapping
                        ]


    if LAYOUT not in c:
        c[LAYOUT] = {LOGIC:GRID}

    l = c[LAYOUT]
    if GRID == l[LOGIC]:
        print "Layouting : GRID"
        if (ROWS not in l) and (COLUMNS not in l):
            print "Both rows and columns are computed"
            rows = int(math.floor(math.sqrt(len(c[CHILDREN]))))
            columns = int(math.ceil(float(len(c[CHILDREN])) / rows)) if rows else 1
            l[ROWS] = rows
            l[COLUMNS] = columns
        if ROWS not in l:
            print "Rows computed from columns count"
            rows = int(math.floor(math.sqrt(len(c[CHILDREN]))))
            rows = int(math.ceil(float(len(c[CHILDREN])) / l[COLUMNS])) if l[COLUMNS] else 1
            l[ROWS] = rows
        if COLUMNS not in l:
            print "Columns computed from rows count"
            columns = int(math.ceil(float(len(c[CHILDREN])) / l[ROWS])) if l[ROWS] else 1
            l[COLUMNS] = columns
        print "Layout of component %s : [%d x %d]" % (c[ID], l[ROWS], l[COLUMNS])


        rows_nodes = [[] for i in range(0, l[ROWS])]
        columns_nodes = [[] for i in range(0, l[COLUMNS])]

        i = 0
        for n in c[CHILDREN]:
            layout_component(n)
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
            for n in row:
                n[Y] = y_offset + max_height / 2 - n[HEIGHT] / 2
            y_offset = y_offset + max_height + c[INNER_MARGIN]


        for column in columns_nodes:
            max_width = 0
            for n in column:
                if n[WIDTH] > max_width:
                    max_width = n[WIDTH]
#                n[X] = x_offset
            for n in column:
                n[X] = x_offset + max_width / 2 - n[WIDTH] / 2
            x_offset = x_offset + max_width + c[INNER_MARGIN]


        c[WIDTH] = x_offset
        c[HEIGHT] = y_offset

        c[LAYOUTED] = True

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
        CHILDREN:[],
        LAYOUTED:False,
        TRACED:False,
        INNER_MARGIN: 5,
        X: 0,
        Y: 0,
        WIDTH: 50,
        HEIGHT: 50,
        STROKE: "#8fc8ff",
        STROKE_WIDTH:1.5,
        RX:10,
        SHAPE:RECTANGLE,
        FILLCOLOR: "#DDDDDD",
        TEXT_TOP_MARGIN:5}

    for p, v in default_properties.items():
        if p not in c:
            c[p] = v

def lookup_component(components, c_id):
    matching_components = filter(lambda c: c[ID] == c_id, components)
    c = matching_components[0] if len(matching_components) else None

    return c

def augment_items(components, links):
    for c in components:
        set_default_component(c)
        nodes_list = []
        for n in c[CHILDREN]:
            nodes_list.append(lookup_component(components, n))
        c[CHILDREN] = nodes_list
    for l in links:
        l[TYPE] = LINK

def center_x(item, reference):
    new_x = reference[X] + reference[WIDTH] / 2
    new_x = new_x - item[WIDTH] / 2

    return new_x

def center_y(item, reference):
    new_y = reference[Y] + reference[HEIGHT] / 2
    new_y = new_y - item[HEIGHT] / 2

    return new_y

def trace_component(c, svg, parent, depth = 0):
    if (TRACED in c) and c[TRACED]:
        return

    print "%sTracing : %s" % (" " * depth, c[ID])
    c[TRACED] = True
    layout_component(c)
    if parent is not None:
        c[X] = c[X] + parent[X] if X in parent else 0
        c[Y] = c[Y] + parent[Y] if Y in parent else 0

    c_item = svg.addChildElement(c[SHAPE], c)
    if LABEL in c:
        text_item = svg.addChildElement('text',
                                        {X: c[X] + c[WIDTH] / 2,
                                         Y: c[Y] + c[TEXT_TOP_MARGIN] / 2,
                                         TEXT_ANCHOR: MIDDLE},
                                        c[LABEL])

#        text_item[X] = center_x(text_item, c_item)
#        text_item[Y] = center_y(text_item, c_item)

        print "Type of : %s", str(type(text_item))

#        for k in text_item:
#            print "K : ", k

    for n in c[CHILDREN]:
        trace_component(n, svg, c, depth + 1)

def render(g):
    components = g[COMPONENTS] if COMPONENTS in g else []
    links = g[LINKS] if LINKS in g else []

    augment_items(components, links)

    my_svg = drawSVG.SVG()

    print "len : %s" % len(components)

    master_c = lookup_component(components, "root")

    set_default_component(master_c)

    trace_component(master_c, my_svg, None)
    return my_svg

def main():
    if 3 > len(sys.argv):
        print "Need the name of the file to parse and the output file"
        return 1

    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]
    graph = eval('%s' % open(input_file_name).read())
    svg = render(graph)
    svg.outputToFile(output_file_name)


if "__main__" == __name__:
    sys.exit(main())

