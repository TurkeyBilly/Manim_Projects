
from manim import *


'''
python -m manim render manimlib\Projects\Implicit_graph.manimCE.py -s -pqh
C:\TDDownload\manim_master_2021.9.5\manin_master_9.5\media\images\Implicit_graph.manimCE\ImplicitFunctionExample_ManimCE_v0.11.0.png
'''


class ImplicitFunctionExample(MovingCameraScene):
    def construct(self):
        self.camera.frame.scale(1.5)
        x, y = RIGHT, UP
        '''
        Length = 21 (14*1.5);
        Height = 12 (8*1.5);
        EDGE TO THE CENTER{
            LEFT: 7; RIGHR: 14;
            UP: 4; DOWN: 8;
        }
        '''
        self.camera.frame.move_to(3.5*RIGHT+2*DOWN)
        func_tex = MathTex(
            r'x^{2}+y^{2}-cx^{2}y^{2}=1',
            substrings_to_isolate=['x', 'y', 'c']
        )
        title_1 = Tex("b) Algebratic Proof").move_to(9.2*RIGHT+3.63*UP)
        bound_title = Underline(title_1, buff=0.08)
        self.add(bound_title, title_1)
        formulas_in_mathtex = [
            (r'x^{2}+y^{2}-x^{2}y^{2}', '=', '1'),
            (r'for\ x', '=', r'\pm1\  \implies\  x^{2}=1'),
            (r'1+y^{2}-1\cdot y^{2}','=','1'),
            (r'\quad y^{2}-y^{2}', '=', '1-1'),
            (r'\quad 0', '=', '0'),
            (r'\therefore \forall_y ', r'\in', r'\mathbb{R} \ \Longleftarrow  \ x=\pm1'),
            (r'\because',r'\,x^{2}+y^{2}-x^{2}y^{2}'),
            (r'is\ ',r'a\ symmetric\ polynomial'),
            (r'\therefore \forall_x ', r'\in', r'\mathbb{R} \ \Longleftarrow \ y=\pm1')
            #(r'\therefore\ ', r'for\ y', '=', r'\pm1\ ', r'\implies\ ', r' x ', r'\in', r'\mathbb{R}'),
            
        ]
        for index, obj in enumerate(formulas_in_mathtex):
            formulas_in_mathtex[index] = MathTex(
                *formulas_in_mathtex[index],
                substrings_to_isolate=['x', 'y']
            ).set_color_by_tex('x', RED).set_color_by_tex('y', YELLOW)\
                if index != 7 else MathTex(
                *formulas_in_mathtex[index]
            )
            if index == 0:
                formulas_in_mathtex[index].move_to(10.5*RIGHT+2.7*UP)
            else:
                formulas_in_mathtex[index].next_to(
                    formulas_in_mathtex[index-1],
                    DOWN
                )
        
        formulas_in_mathtex[5].shift(0.7*LEFT).add_background_rectangle(color=BLUE)
        formulas_in_mathtex[8].shift(0.7*LEFT).add_background_rectangle(color=BLUE)
        f1s = SurroundingRectangle(formulas_in_mathtex[5])
        f2s = SurroundingRectangle(formulas_in_mathtex[8], color=RED)
        center1 = f1s.get_corner(UP+LEFT)
        center2 = f2s.get_corner(UP+LEFT)
        self.add(*formulas_in_mathtex, f1s, f2s)
        func_tex.set_color("#76DDC0").set_color_by_tex('x', RED).set_color_by_tex('y', YELLOW).set_color_by_tex('c', GREEN)
        plane = NumberPlane()
        plane.add_coordinates()
        graph = ImplicitFunction(
            lambda x, y: (x**2) + (y**2) - (x**2) * (y**2) - 1,
            x_range=[-config.frame_width / 2, config.frame_width / 2],
            min_depth=1,
            max_quads=2000,
            color=ORANGE,
            stroke_width=1.5*DEFAULT_STROKE_WIDTH
        )
        
        Other_c_val = [0, 1, -2, -1/2]
        other_color = ["#FF0000", "#DC75CD", "#FFFF00", "#00FF00"]
        other_graphs = VGroup(
            *[ImplicitFunction(
            lambda x, y: (x**2) + (y**2) + c*(x**2) * (y**2) - 1,
            x_range=[-config.frame_width / 2, config.frame_width / 2],
            min_depth=1,
            max_quads=2000,
            color=_color,
            fill_opacity = 0,
            stroke_width=0.5*DEFAULT_STROKE_WIDTH) for c, _color in\
                zip(Other_c_val, other_color)
                ]   
        )
        
        
        self.add(other_graphs)
        self.add(plane, graph, func_tex.move_to(3.5*UP+4.5*LEFT))
        
        c_is_neg_1 = Tex('(c=-1)', substrings_to_isolate=['c']).set_color(ORANGE).\
                set_color_by_tex('c', GREEN)
        c_val_indication = VGroup(
            *[Tex(f'(c={num})', substrings_to_isolate=['c']).set_color(_color).\
                set_color_by_tex('c', GREEN)\
            for num, _color in zip(Other_c_val, other_color)]
        )
        c_is_neg_1.next_to(func_tex, DOWN)
        c_val_indication[0].next_to(c_is_neg_1, RIGHT)
        c_val_indication[1].move_to(-6*x+2*y)
        c_val_indication[2].next_to(c_val_indication[1], RIGHT)
        c_val_indication[3].next_to(c_is_neg_1, LEFT)
        self.add(c_is_neg_1, c_val_indication)
        

        dots_kwargs = dict(
            color=BLUE_D, 
            fill_opacity=0.8, 
            radius=0.5*DEFAULT_DOT_RADIUS
        )
        dots_kwargs2 = dict(
            color=BLUE, 
            fill_opacity=.0 ,
            radius=0.5*DEFAULT_DOT_RADIUS, 
            stroke_width=0.5*DEFAULT_STROKE_WIDTH
        )
        dots = VGroup(
            Dot(point=LEFT+UP, **dots_kwargs), Circle(**dots_kwargs2).move_to(LEFT+UP),
            Dot(point=LEFT+DOWN, **dots_kwargs), Circle(**dots_kwargs2).move_to(LEFT+DOWN),
            Dot(point=RIGHT+UP, **dots_kwargs), Circle(**dots_kwargs2).move_to(RIGHT+UP),
            Dot(point=RIGHT+DOWN, **dots_kwargs), Circle(**dots_kwargs2).move_to(RIGHT+DOWN)
        )
        self.add(dots)
            
        connections = VGroup(
            d1:=Dot(2.5*RIGHT+UP, color=RED),
            d2:=Dot(1.5*RIGHT+DOWN, color=RED),
            d3:=Dot(3.5*UP+RIGHT, color=YELLOW),
            d4:=Dot(3*UP+LEFT, color=YELLOW),
            DashedLine(d1, center2, color=RED),
            DashedLine(d2, center2, color=RED),
            DashedLine(d3, center1, color=YELLOW),
            DashedLine(d4, center1, color=YELLOW)
        )
        self.add(connections)
        
        # TODO Part C 
        # Proving by implicit differenciation
        
        # Give Myself a little break by adding the logal
        banner = ManimBanner().move_to(13*RIGHT-4.35*UP).scale(1/4)
        self.add(banner)
        
        title_2 = Tex("C) Implicit Differenciation").move_to(-4.3*UP-4*RIGHT)
        bound_title2 = Underline(title_2).next_to(title_2, DOWN)
        # NOTE !!! DON't Use * with tuple, don't use frac with splits
        formulas_set2 = [
            func_tex.copy().next_to(bound_title2, DOWN).shift(0.9*LEFT+0.2*DOWN), #0
            r"\Longrightarrow", #1
            r'{d\over dx}x^{2}+{d\over dx}y^{2}+{d\over dx}cx^{2}y^{2}={d\over dx}\left(1\right)', #2
            r"\Longrightarrow", #3
            r"2x+2yy'+2cxy^{2}+2cx^{2}yy'=0", #4
            r"y'\left(2y+2cx^{2}y\right)=-2cxy^{2}-2x, ",#5
            r"\ \ y' = {-2cxy^{2}-2x\over \left(2y+2cx^{2}y\right)}", #6
            r"=-{cxy^{2}+x\over y\left(1+cx^{2}\right)}=", #7
            r"{x-xy^{2}\over y\left(1-x^{2}\right)}", #8
            r"(when\ c=-1)", #9
        ]
        MathTex().break_up_tex_strings
        for i in range(1, 10):
            formulas_set2[i] = MathTex(
                formulas_set2[i],
                substrings_to_isolate=['x', 'y', 'c', 'd']
            ).set_color_by_tex('x', RED).set_color_by_tex('y', YELLOW).\
                set_color_by_tex('d', GREY).set_color_by_tex('c', GREEN)
        
        for i in range(1, 5):
            formulas_set2[i].next_to(formulas_set2[i-1], RIGHT)
        formulas_set2[5].move_to(-3.6*x-6.75*y)
        for i in range(6, 10):
            formulas_set2[i].next_to(formulas_set2[i-1])

        formulas_set2 = VGroup(*formulas_set2)
        self.add(SurroundingRectangle(formulas_set2[8], color=BLUE))
        self.add(title_2, bound_title2, formulas_set2)
        
        
        
