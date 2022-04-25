from manim import *
import igraph

from intermediate.imobject import IMobject

class INode(IMobject):
    def __init__(self, mobject_handler, text="N", radius=0.6, color=RED, textcolor=RED):
        # Node members
        self.parent = None
        self.children = []

        # Manim mobjects
        self.label = Text(text, color=textcolor) 
        self.circle = Circle(radius=radius, color=color)
        self.mobject = VGroup(self.label, self.circle)
        self.line_to_parent = None 

        # Aux info for igraph layout and line connecting
        self.igraph_vertex_id = None
        self.mobject_handler = mobject_handler


    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def move_node(self, x, y):
        self.mobject.move_to(np.array([x, y, 0]))
        if self.parent is not None:
            # Move connecting line
            pn = self.parent.mobject
            cn = self.mobject

            if pn.get_x() <= cn.get_x():
                direction = RIGHT
            else:
                direction = LEFT

            self.line_to_parent = Line(pn.get_corner(DOWN + direction) + DOWN * 0,
                        cn.get_top() + UP * 0,
                        stroke_width=2,
                        color=GREY)

            self.line_to_parent.add_updater(lambda m: m.put_start_and_end_on(self.mobject_handler.getCopy(self.parent).get_corner(DOWN + direction) + DOWN * 0,
                        self.mobject_handler.getCopy(self).get_top() + UP * 0))

    """ Recursive functions """
    def scale_subtree(self, layout):
        self.move_node(*layout[self.igraph_vertex_id])
        for c in self.children:
            c.scale_subtree(layout)

    def update_colours(self):
        self.label.set_color(WHITE)
        self.circle.set_color(WHITE)
        if self.line_to_parent is not None:
            self.line_to_parent.set_color(GREY) 
        for c in self.children:
            c.update_colours()

    def build_tree_to_scene(self, state_handler):
        if self.mobject is not None:
            state_handler.add_object_to_curr(self)
        if self.line_to_parent is not None:
            state_handler.instant_add(self.line_to_parent)

        for c in self.children:
            c.build_tree_to_scene(state_handler)

    def build_igraph(self, g, parent_id=None):
        v = g.add_vertex()
        self.igraph_vertex_id = v.index
        if parent_id is not None:
            g.add_edge(parent_id, v.index)
        for c in self.children:
            c.build_igraph(g, v.index)

    
class IRoot(INode):
    def build(self, x_scale, y_scale):
        self.update_colours()
        self.layout(x_scale, y_scale)


    # Automatically layout tree using igraph
    def layout(self, x_scale, y_scale):
        g = igraph.Graph()
        self.build_igraph(g)

        layout = g.layout_reingold_tilford(root=[0])

        scaled_layout = [[x * x_scale, -y * y_scale +3] for x, y in layout]
        self.scale_subtree(scaled_layout) 