from typing import Callable
from manimlib import *


__manimlib_version__ = "1.5.0*" # With modificationss
__python_version__ = "3.9.0"
__start_date__ = "2022.1.24"

commend_line = r'''
manimgl C:\Users\jiant\anaconda3\envs\manim\projects\GL\chain_rule_new.py
-o: save and open
-n10: start from scene 10
-n3,6: start from scene 3 and ends at scene 6
-l (480p15)
-m (720p30)
--hd (1080p30)
--uhd (4k)
'''
class FirstScene(Scene):
    def debugTeX(self, texm: Mobject, scale_factor: int = 0.6, text_color: str = PURPLE) -> None:
        # https://github.com/manim-kindergarten/manim_sandbox/blob/master/utils/functions/debugTeX.py
        for i, j in enumerate(texm):
            tex_id = Text(str(i), font="Consolas").scale(scale_factor).set_color(text_color)
            tex_id.move_to(j)
            self.add(tex_id)

    def remove_all_except(self, values: list[Mobject], *exceptions: list[Mobject]):
        if not values:
            values = self.mobjects
        print(values)
        self.remove(*filter(
            lambda m: isinstance(m, Mobject) and m not in exceptions,
            values
        ))
        return self

    def str_list_to_tex_list(self, f: list[str], **kwargs) -> VGroup:
        return  VGroup(
            *[Tex(s, **self.tex_kwargs, **kwargs)
            for s in f]
        )

    @staticmethod
    def cross_center(horizontal: Mobject, vertical: Mobject) -> np.array:
            return [vertical.get_center()[0], horizontal.get_center()[1], 0]

    def setup(self):
        self.isolate = ['f', 'g', 'x', '=', '(', ')', 'h', r"m_{1}", r"m_{2}", r"b_{1}", r"b_{2}", "+"]
        self.tex_to_color_map={
            'x': RED,
            'f': YELLOW,
            'g': BLUE,
            'h': GREEN,
            r"m_{1}": TEAL,
            r"m_{2}": TEAL
        }
        self.chainrule = Tex(
            r"{d\over dx} f(g(x)) = f'(g(x)) \cdot g(x)",
            isolate=self.isolate,
            tex_to_color_map=self.tex_to_color_map
        ).move_to(3.2*UP)

        self.tex_kwargs = dict(
            isolate=self.isolate,
            tex_to_color_map=self.tex_to_color_map
        )

        # self.add(self.chainrule)

    def construct(self):
        
        self.play(Write(self.chainrule, run_time=5)); self.wait(3)
        # self.debugTeX(self.chainrule)
        transed = self.chainrule[2:9].copy()
        no_transed = transed.copy()
        fg0 = Tex(
            'f( \ \ x \ )',
            isolate=[*self.isolate, "\\"], 
            tex_to_color_map=self.tex_to_color_map
        ).move_to(transed.get_center() + DOWN)

        fg1 = Tex('f(x)', 
            isolate=self.isolate, 
            tex_to_color_map=self.tex_to_color_map
        ).move_to(transed.get_center() + DOWN)

        self.play(Write(fg1, run_time=3.5))
        self.wait()

        no_transed.shift(2*DOWN)
        self.wait(3)

        arr = CurvedArrow(fg0.get_left(), transed.get_left() + 2*DOWN).set_color(BLUE)
        what_happened = Text('What Happened?', font_size=20).move_to(arr.get_center() + 1.7* LEFT)
        self.play(TransformMatchingTex(fg1, fg0, run_time=2.5),)
        self.play(
            TransformMatchingTex(fg0.copy(), __copied:=transed.copy().shift(2*DOWN)),
            *[ShowCreation(mob) for mob in [arr, what_happened]],
            transed.animate.shift(2*DOWN)
        )
        self.remove(__copied)
        self.wait(3)
        title = Text('Part 1')
        title2 = Text('Linear Combinations', font_size=20)
        gx = Tex('g(x)', **self.tex_kwargs).move_to(transed)
        formulas = [
            '=2x',
            '=3x'
        ]

        formulas = VGroup(
            *[Tex(s, **self.tex_kwargs)
            for s in formulas]
        )

        VGroup(title, title2).arrange(DOWN).move_to(3.2*UP + 4.3*RIGHT)
        self.play(
            Write(VGroup(title, title2)),
            self.chainrule.animate.shift(3*LEFT),
            *[FadeOut(mob)
                for mob in [what_happened, arr]
            ],
            LaggedStart(
                TransformMatchingTex(fg0, fg1),
                TransformMatchingTex(transed, gx),
                ShowCreation(formulas[0].next_to(fg1)),
                ShowCreation(formulas[1].next_to(gx))
            )
        )

        axis = Axes(
            x_range=[-1.0, 6.0, 1.0], y_range=[-1.0, 20.0, 1.0],
            height=FRAME_HEIGHT*1.3, width=FRAME_WIDTH*1.3
        ).scale(0.5).shift(1.5*RIGHT+.5*DOWN)
        
        labels = axis.add_coordinate_labels(
            #[*[x for x in range(-8, 9, 2)]],
            # [*[y for y in range(-6, 7, 2)]],
            font_size=12
        )

        x_min = -.5
        x_max = 2.5

        h_graph = axis.get_graph(lambda x: 6*x, x_range=[x_min, x_max, 0.1], color=GREEN)
        f_graph = axis.get_graph(lambda x: 2*x, x_range=[x_min, x_max, 0.1], color=YELLOW)
        g_graph = axis.get_graph(lambda x: 3*x, x_range=[x_min, x_max, 0.1], color=BLUE)
        self.play(
            LaggedStart(
                AnimationGroup(
                    *[
                        mob.animate.shift(4*LEFT)
                        for mob in [formulas[0], formulas[1], fg1, gx]
                    ]
                ),
                *[
                    ShowCreation(mob)
                    for mob in [axis, f_graph, g_graph]
                ],
                lag_ratio=0.2
            )
        )
        self.wait(3)
        fx = fg1
        hx = Tex('h(x)', **self.tex_kwargs).next_to(gx, DOWN)

        self.play(*[ApplyWave(mob, run_time=1.3, amplitude=0.28) 
            for mob in [fx,f_graph, formulas[0]]]
        )
        self.wait(1)
        self.play(*[ApplyWave(mob, run_time=1.3, amplitude=0.28) 
            for mob in [gx,g_graph, formulas[1]]]
        )

        gx_copy = gx.copy()
        gx_copy.shift(DOWN)
        fx_copy = fx.copy()
        fx_copy[0].next_to(fx_copy[1].next_to(gx_copy, LEFT, SMALL_BUFF/2), LEFT, SMALL_BUFF/1.5)
        fx_copy[3].next_to(gx_copy, RIGHT, SMALL_BUFF/3)
        formulas_copy = formulas.copy()
        formulas_copy[0][0].shift(2*DOWN)
        formulas_copy[0][1].shift(2*DOWN)
        star = Tex("\\cdot").next_to(formulas_copy[0][1], RIGHT, SMALL_BUFF)
        formulas_copy[1].remove(formulas_copy[1][0]).next_to(star, RIGHT, SMALL_BUFF)

        _a = [gx, *[fx[i] for i in [0, 1, 3]], 
            formulas[0][0], formulas[0][1], formulas[1][1], formulas[1][2]
        ]
        _b = [gx_copy, *[fx_copy[i] for i in [0, 1, 3]], 
            formulas_copy[0][0], formulas_copy[0][1], formulas_copy[1][0], formulas_copy[1][1]
        ]
        self.wait(3)

        self.play(
            *[ReplacementTransform(__a.copy(), __b)
            for __a, __b in zip(_a, _b)],
            ShowCreation(star)
        )
        self.play(ShowCreation(h_graph))
        self.wait(4)
        
        self.play(*[
            mob.animate.shift(DOWN)
            for mob in [*_a, *_b, *formulas, star, fx[2]]
        ])
        dx = self.chainrule[0:2]
        dx_copy = dx.copy().shift(2.6*RIGHT+DOWN)
        self.play(
            ReplacementTransform(dx.copy(), dx_copy)
        )


        self.play(
            LaggedStart(
                ReplacementTransform(
                    formulas[0][1].copy(), 
                    c:= formulas[0][1].copy().move_to(self.cross_center(fx, dx_copy)).set_color(TEAL)),
                ReplacementTransform(
                    formulas[1][1].copy(), 
                    d:= formulas[1][1].copy().move_to(self.cross_center(gx, dx_copy)).set_color(TEAL)),
                ReplacementTransform(
                    VGroup(formulas_copy[0][1], formulas_copy[1][1]).copy(), 
                    Tex("6").move_to(self.cross_center(formulas_copy[0][1], dx_copy)).set_color(TEAL)
                ),
                lag_ratio=0.5
            )
        )

        copies = []
        dis = 8.5
        copies.append(formulas[0][0].copy().shift(dis * RIGHT)) # First Equal Sign
        copies.append(formulas[1][0].copy().shift(dis * RIGHT)) # Second Equal Sign
        fx_copy2 = fx.copy().next_to(copies[0], LEFT)
        gx_copy2 = gx.copy().next_to(copies[1], LEFT)
        third_equal = formulas[1][0].copy().shift(dis * RIGHT + DOWN)
        fx_copy.remove(fx_copy[2]) # NOTE delete the extra x in fx!
        hx_copy2 = VGroup(fx_copy, gx_copy).copy().next_to(third_equal, LEFT)
        third_equal.next_to(hx_copy2, DOWN, buff=MED_LARGE_BUFF).shift(0.25*LEFT)

        _a = [fx, gx, formulas[0][0], formulas[1][0]]
        _b = [fx_copy2, gx_copy2, *copies]

        self.play(
            LaggedStart(
                *[
                    Transform(__a.copy(), __b)
                    for __a, __b in zip(_a, _b)
                ],
                lag_ratio=0.5
            )
        )

        new_formulas = [
            r"m_{1}x+b_{1}",
            r"m_{2}x+b_{2}",
            r"m_{1}(m_{2}x+b_{2})+b_{1}",
            r"m_{1}m_{2}x+m_{1}b_{2}+b_{1}"
        ]

        new_formulas = VGroup(
            *[Tex(s, **self.tex_kwargs)
            for s in new_formulas]
        )

        self.play(
            LaggedStart(
                Write(new_formulas[0].next_to(copies[0])),
                Write(new_formulas[1].next_to(copies[1])),
                lag_ratio=0.3,
                run_time=2.5
            )
        )
        
        m1_copy = new_formulas[0][0].copy().next_to(third_equal)
        brackets1 = hx_copy2[0][1].copy().next_to(m1_copy, buff=SMALL_BUFF/1.5)
        m2xb2 = new_formulas[1].copy().next_to(brackets1, buff=SMALL_BUFF/2)
        brackets2 = hx_copy2[0][2].copy().next_to(m2xb2, buff=SMALL_BUFF/3)
        plus_b1 = new_formulas[0][2:4].copy().next_to(brackets2, buff=SMALL_BUFF/2)
        # self.debugTeX(new_formulas[0])

        self.play(
            LaggedStart(
                ReplacementTransform(formulas_copy[0][0].copy(), third_equal),
                ReplacementTransform(VGroup(fx_copy, gx_copy).copy(), hx_copy2),
                ReplacementTransform(new_formulas[0][0].copy(), m1_copy),
                lag_ratio=0.3
            )
        )
        self.play(
            ReplacementTransform(hx_copy2[0][1].copy(), brackets1)
        )
        self.play(
            ReplacementTransform(new_formulas[1].copy(), m2xb2)
        )
        self.play(
            ReplacementTransform(hx_copy2[0][2].copy(), brackets2)
        )
        self.play(
            ReplacementTransform(new_formulas[0][2:4].copy(), plus_b1)
        )

        fourth_equal = third_equal.copy().next_to(third_equal, DOWN, MED_LARGE_BUFF)
        self.play(
            ReplacementTransform(third_equal.copy(), fourth_equal)
        )

        self.play(
            ReplacementTransform(m1_copy.copy(), _j1:=m1_copy.copy().next_to(fourth_equal))
        )

        self.play(
            ReplacementTransform(m2xb2[0:3].copy(), _j2:=m2xb2[0:3].copy().next_to(_j1, buff=SMALL_BUFF))
        )

        self.play(
            ReplacementTransform(m1_copy.copy(), _j4:=m1_copy.copy().next_to(_j2, buff=SMALL_BUFF)),
            ReplacementTransform(m2xb2[3:].copy(), _j5:=m2xb2[3:].copy().next_to(_j4, buff=SMALL_BUFF))
        )

        self.play(
            ReplacementTransform(plus_b1.copy(), plus_b1.copy().next_to(_j5, buff=SMALL_BUFF))
        )
        
        new_slope = VGroup(_j1, _j2[:1])
        self.play(
            LaggedStart(
                *[
                    ShowCreation(SurroundingRectangle(mob, color=GREEN_B))
                    for mob in (new_formulas[0][0], new_formulas[1][0], new_slope)
                ], lag_ratio=0.2
            )
        )
        self.wait(5)


# manimgl C:\Users\jiant\anaconda3\envs\manim\projects\GL\chain_rule_new.py SecondScene
class Abondened(FirstScene):
    def construct(self):
        plane = Axes(
            x_range=[-1.0, 6.0, 1.0], 
            y_range=[-1.0, 20.0, 1.0],
            height=FRAME_HEIGHT - 2,
            width=FRAME_WIDTH - 2,
            axis_config={
                "include_ticks" : False
            }
        )
        DecimalNumber._handle_scale_side_effects
        fx_graph = plane.get_graph(lambda x: x**2)
        self.add(plane, fx_graph)

        
class First2SecondTransition(FirstScene):
    # manimgl C:\Users\jiant\anaconda3\envs\manim\projects\GL\chain_rule_new.py First2SecondTransition
    def construct(self):
        derivative_sign = self.chainrule[0:2].scale(0.5)
        formulas = [
            r"f(x)+g(x)=(m_{1}+m_{2})x+(b_{1}+b_{2})",
            r"[f(x)+g(x)]=m_{1}+m_{2}", #
            r"[f(x)+g(x)]=f'(x)+g'(x)", #
            r"f(x)\cdot g(x)=(m_{1}x+b_{1})(m_{2}x+b_{2})",
            r"=m_{1}m_{2}x^{2}+(m_{1}b_{2}+m_{2}b_{1})x+b_{1}b_{2}",
            r"[f(x)\cdot g(x)]=2m_{1}m_{2}+m_{1}b_{2}+m_{2}b_{1}", #
            r"=m_{1}(m_{2}+b_{2})+m_{2}(m_{1}+b_{1})", #
            r"[f(x)\cdot g(x)]=f'(x)g(x)+g'(x)f(x)", #,
            r"y=", #8
            r"x" #9
        ]
        formulas = self.str_list_to_tex_list(formulas, font_size=24).arrange(DOWN).shift(3.5*LEFT)
        
        di = [2, 3, 6, 8]
        for i in di:
            i = i - 1
            cp = derivative_sign.copy().next_to(formulas[i], LEFT, buff=0.125)
            self.add(cp)
            formulas[i] = VGroup(cp, formulas[i])

        self.add(formulas)

        axis = Axes(
            x_range=[-1.0, 6.0, 1.0], y_range=[-1.0, 20.0, 1.0],
            height=FRAME_HEIGHT*1.3, width=FRAME_WIDTH*1.3
        ).scale(0.5).shift(2*RIGHT+.5*DOWN)
        self.add(axis)

        g = axis.get_graph(lambda x: x**2 + x*math.sin(3*x)/2, [-1, 5]).set_color(YELLOW)

        formulas[8].move_to(3*UP).scale(2)
        x_tracker = ValueTracker(1)
        slope = DecimalNumber(self.get_derivative(g, x_tracker.get_value())).add_updater(
            lambda mob: mob.set_value(self.get_derivative(g, x_tracker.get_value()))
        ).next_to(formulas[8]).scale(.5)
        formulas[9].next_to(slope).scale(2)

        y_intercept = DecimalNumber(self._get_secant_line_intercept(g, x_tracker.get_value()), include_sign=True).add_updater(
            lambda mob: mob.set_value(self._get_secant_line_intercept(g, x_tracker.get_value()))
        ).next_to(formulas[9]).scale(0.5)
        
        p = self.get_dot_from_func(axis, g, x_tracker.get_value()).set_color(BLUE)
        p.add_updater(lambda obj: obj.become(self.get_dot_from_func(axis, g, x_tracker.get_value())))
        tl_line = self.get_tangent_line(axis, g, x_tracker.get_value(), x_tolerance=0.5)
        tl_line.add_updater(lambda obj: obj.become(self.get_tangent_line(axis, g, x_tracker.get_value(), x_tolerance=0.5)))

        self.add(g, p, tl_line, slope, y_intercept)
        self.wait(1.5)
        self.play(x_tracker.animate.set_value(4), run_time=2)
        self.wait(1.5)
        self.play(x_tracker.animate.set_value(3), run_time=2)
        self.wait(1.5)
        self.play(x_tracker.animate.set_value(2), run_time=2)
    

        self.embed()

    def _round_decorator(func, *args, **kwargs):
        def wrap(*args, **kwargs):
            return round(func(*args, **kwargs), 3)
        return wrap

    @_round_decorator
    def get_slope(self, graph: ParametricCurve, x1, x2):
        func = graph.underlying_function
        return (func(x2) - func(x1)) / (x2-x1)

    @_round_decorator
    def get_derivative(self, graph: ParametricCurve, x_value, epsilon=1e-8) -> float:
        func = graph.underlying_function
        return (func(x_value + epsilon) - func(x_value)) / epsilon

    def get_secant_line(self, axis: Axes, graph: ParametricCurve, x1, x2, x_tolerance=1):
        func = graph.underlying_function
        slope = self.get_slope(graph, x1, x2)
        line = axis.get_graph(lambda x: slope*(x-x1) + func(x1), x_range=[x1-x_tolerance, x2+x_tolerance])
        return line

    def _get_secant_line_intercept(self, graph: ParametricCurve, x1):
        func = graph.underlying_function
        slope = self.get_derivative(graph, x1)
        return func(x1) - slope*x1
    
    def get_tangent_line(self, axis, graph, x1, epsilon=1e-8, x_tolerance=1):
        return self.get_secant_line(axis, graph, x1, x1 + epsilon, x_tolerance)


    def get_dot_from_func(self, axis: Axes, graph: ParametricCurve, x) -> Dot:
        return Dot(axis.c2p(x, graph.underlying_function(x)))


class DotOnPlane(Dot):
    _axis: Axes
    pos: np.ndarray
    CONFIG = {
        "stroke_width": 5
    }
    def __init__(self, x=0, y=0, axis=None, inner_color=None, outter_color=None,**kwargs):
        if axis is not None:
            self._axis = axis
        super().__init__(self._axis.c2p(x, y), **kwargs)

        if inner_color is not None:
            self.set_fill(inner_color)
        
        if outter_color is not None:
            self.set_stroke(outter_color, opacity=1)

    def __sub__(self, other: "DotOnPlane") -> np.ndarray:
        return self.get_center() - other.get_center()

    @property
    def pos(self) -> np.ndarray:
        return self.get_center()


class SecondScene(First2SecondTransition):
    def wait(self, duration=3, stop_condition=None, note=None, ignore_presenter_mode=False):
        return super().wait(duration, stop_condition, note, ignore_presenter_mode)

    def off(self, *mobjects: list[Mobject], opacity=.15, void=True, **kwargs):
        if void == True:
            self.play(
                *[m.animate.set_stroke(opacity=opacity) for m in mobjects],
                **kwargs
            )
        else:
            return AnimationGroup(*[m.animate.set_stroke(opacity=opacity) for m in mobjects])

    def on(self, *mobjects: list[Mobject], opacity=1, void=True, **kwargs):
        if void == True:
            self.play(
                *[m.animate.set_stroke(opacity=opacity) for m in mobjects],
                **kwargs
            )
        else:
            return AnimationGroup(*[m.animate.set_stroke(opacity=opacity) for m in mobjects])

    def on_off(self, on_mobjects: list[Mobject], off_mobjects: list[Mobject],
                on_opacity=1, off_opacity=.15, void=True, **kwargs):
        if not isinstance(on_mobjects, list):
            on_mobjects = [on_mobjects]
        if not isinstance(off_mobjects, list):
            off_mobjects = [off_mobjects]
        if void == True:
            self.play(
                *[m.animate.set_stroke(opacity=on_opacity) for m in on_mobjects],
                *[m.animate.set_stroke(opacity=off_opacity) for m in off_mobjects],
                **kwargs
            )
        else:
            return AnimationGroup(
                *[m.animate.set_stroke(opacity=on_opacity) for m in on_mobjects],
                *[m.animate.set_stroke(opacity=off_opacity) for m in off_mobjects],
            )

    # manimgl C:\Users\jiant\anaconda3\envs\manim\projects\GL\chain_rule_new.py SecondScene
    def construct(self, break_at_point: bool = False):
        def add_numbers(axis: NumberLine, x_values=None, excluding=None, font_size=24, **kwargs):
            numbers = VGroup()
            for x in x_values:
                if excluding is not None and x in excluding:
                    continue
                n = Tex(str(x))
                numbers.add(
                    n.next_to(
                        axis.number_to_point(x),
                        direction=axis.line_to_number_direction,
                        buff=axis.line_to_number_buff
                    )
                )
            return numbers
        frame: CameraFrame = self.camera.frame
        plane = NumberPlane(x_range=[-8, 12], y_range=[-3, 7], height=2*(FRAME_HEIGHT)-.2,
                width=2*FRAME_WIDTH)
        labels = plane.get_y_axis_label("y"), plane.get_x_axis_label("x", direction=UL)
        __axes = plane.get_axes()
        coordinate_labels = VGroup()
        for axis, values in zip(__axes, [range(-2, 8), range(-1, 5)]):
            axis: NumberLine
            labels = add_numbers(axis, values)
            coordinate_labels.add(labels)
        self.add(plane, *labels, coordinate_labels)

        title = Text('Part 2')
        title2 = Text('Inner is Linear', font_size=20)
        VGroup(title, title2).arrange(DOWN).move_to(3.2*UP + 5.3*RIGHT)
        self.add(title, title2)

        f = lambda x: x**2
        g = lambda x: x / 2  
        h = lambda x: f(g(x))
        f_graph = plane.get_graph(f).set_color(YELLOW)
        g_graph = plane.get_graph(g).set_color(BLUE)
        h_graph = plane.get_graph(h).set_color(GREEN)

        blackboard = Rectangle(3.4, 4.4).set_fill(BLACK, .5).set_stroke(WHITE).shift(1.4* UP + 5*LEFT)
        self.add(blackboard)

        blackboard_2 = Rectangle(3, 1).scale(1.3).shift(2*DOWN+5*RIGHT).scale(1.2).shift(.4*LEFT).\
            set_fill(BLACK, .5).set_stroke(WHITE)
        blackboard_3 = blackboard_2.copy()

        formulas = [
            r"f(x)=x^{2}",
            r"g(x)={1 \over 2} x",
            r"h(x)=f(g(x))",
            r"x", #3
            r"\xmapsto{g}",
            r"g(x)",
            r"\xmapsto{f}",
            r"h(x)",
            r"(x,\ g(x))", #8
            r"(g(x),\ g(x))",
            r"(g(x),\ h(x))",
            r"(x, \ h(x))"
        ]

        formulas = self.str_list_to_tex_list(formulas).arrange(DOWN).\
            next_to(blackboard.get_top(), DOWN)

        self.play(Write(formulas[0]))
        self.play(ShowCreation(f_graph))

        self.wait(2)

        self.play(Write(formulas[1])),
        self.play(
            ShowCreation(g_graph),
            self.off(f_graph, void=False)
        )

        self.wait(2)

        self.play(Write(formulas[2]))
        
        self.wait(3)

        self.play(ShowCreation(blackboard_2))
        self.wait(3)

        for i in range(3, 8):
            if i == 3:
                formulas[i].next_to(blackboard_2.get_left())
            else:
                formulas[i].next_to(formulas[i-1])
            if i == 4:
                formulas[i][0].set_color(BLUE)
            if i==6:
                formulas[i][0].set_color(YELLOW)
        self.play(
            LaggedStart(
                *[Write(formulas[i], run_time=1) for i in range(3,6)],
                lag_ratio=0.6
            )
        )

        symmetry_line = DashedLine(start=plane.c2p(-10, -10), end=plane.c2p(10, 10))
        c2p = plane.c2p

        # Anim 11 (-n10)
        DotOnPlane._axis = plane
        x_value_tracker = ValueTracker(3)
        x_val = x_value_tracker.get_value
        x0 = DotOnPlane(3, 0).set_color(RED).\
            add_updater(lambda m: m.become(
                DotOnPlane(x_val(), 0).set_color(RED)
            )
            )
        self.add(x0)

        # self.off(symmetry_line)
        gx0 = DotOnPlane(3, g(3)).set_fill(RED).set_stroke(BLUE, opacity=1).\
            add_updater(lambda m: m.become(
                DotOnPlane(x_val(), g(x_val())).set_fill(RED).set_stroke(BLUE, opacity=1)
            )
            )
        x_to_g = Line(x0, gx0).set_color(color=[RED, BLUE]).\
            add_updater(lambda x: x.put_start_and_end_on(x0.get_center(), gx0.get_center()))
        gx0_label = formulas[8].scale(.5).next_to(gx0).\
            add_updater(lambda x: x.next_to(gx0))

        self.play(ShowCreation(x_to_g), run_time=3)
        self.play(ReplacementTransform(x0.copy(), gx0), x0.animate.set_opacity(.35))
        self.play(Write(gx0_label))
        self.wait(4)
        
        self.play(Succession(*[Write(formulas[i], run_time=1) for i in range(6,8)]))
        self.wait(4)
        self.wait(2)
        gy0 = DotOnPlane(g(3), g(3)).set_fill(RED).set_stroke(WHITE, opacity=1).\
            add_updater(lambda x: x.become(
                DotOnPlane(g(x_val()), g(x_val())).set_fill(RED).set_stroke(WHITE, opacity=1))
            )
        gx_to_gy = Line(gx0, gy0).set_color(color=[BLUE, WHITE]).\
            add_updater(lambda x: x.put_start_and_end_on(gx0.get_center(), gy0.get_center()))
        gy0_label = formulas[9].scale(.5).next_to(gy0, UR+2*RIGHT, buff=0.15).\
            add_updater(lambda x: x.next_to(gy0, UR+2*RIGHT, buff=0.15))

        self.play(ShowCreation(gx_to_gy), self.on_off(symmetry_line, g_graph, void=False), run_time=3)
        self.play(ReplacementTransform(gx0.copy(), gy0), gx0.animate.set_opacity(.35))
        self.play(Write(gy0_label))
        self.wait(4)

        fx0 = DotOnPlane(g(3), f(g(3))).set_fill(RED).set_stroke(YELLOW, opacity=1).\
            add_updater(lambda x: x.become(
                DotOnPlane(g(x_val()), f(g(x_val()))).set_fill(RED).set_stroke(YELLOW, opacity=1))
            )
        gy_to_fx = Line(gy0, fx0).set_color(color=[WHITE, YELLOW]).\
            add_updater(lambda x: x.put_start_and_end_on(gy0.get_center(), fx0.get_center()))
        fx0_label = formulas[10].scale(.5).next_to(fx0, LEFT, buff=0.2).\
            add_updater(lambda x: x.next_to(fx0, LEFT, buff=0.2))

        self.play(ShowCreation(gy_to_fx), self.on_off([f_graph], [symmetry_line], void=False), run_time=3)
        self.play(ReplacementTransform(gy0.copy(), fx0), gy0.animate.set_opacity(.35))
        self.play(Write(fx0_label))
        self.wait(4)

        hx0 = DotOnPlane(3, f(g(3))).set_stroke(GREEN, opacity=1).\
            add_updater(lambda x: x.become(
                DotOnPlane(x_val(), f(g(x_val()))).set_stroke(GREEN, opacity=1))
            )
        fx_to_hx = Line(fx0, hx0).set_color(color=[YELLOW, GREEN]).\
            add_updater(lambda x: x.put_start_and_end_on(fx0.get_center(), hx0.get_center()))
        hx0_label = formulas[11].scale(.5).next_to(hx0, RIGHT, buff=0.2).\
            add_updater(lambda x: x.next_to(hx0, RIGHT, buff=0.2))

        self.play(ShowCreation(fx_to_hx), self.off(f_graph, void=False), run_time=3)
        self.play(ReplacementTransform(fx0.copy(), hx0), fx0.animate.set_opacity(.35))
        self.play(Write(hx0_label))
        self.wait(4)

        # Anim 27
        h_trace = VMobject().start_new_path(c2p(x_val(), f(g(x_val())))).set_stroke(GREEN, opacity=1).\
            add_updater(lambda mob, dt: mob.add_line_to(hx0.get_center()))
        
        self.add(h_trace)
        self.play(x_value_tracker.animate.set_value(4), run_time=4)

        h_trace.clear_updaters()
        self.play(FadeIn(h_graph))
        self.remove(h_trace)
        self.play(
            AnimationGroup(
                x_value_tracker.animate.set_value(2), run_time=8
            ),
            AnimationGroup(
                Uncreate(gy0_label),
                Uncreate(gx0_label),
                self.on(f_graph, void=False),
                Uncreate(g_graph),
                Uncreate(symmetry_line),
                Uncreate(formulas[3:8]),
                Uncreate(blackboard_2),
            )
        )
        self.wait(4)

        fx1 = DotOnPlane(1, 1, inner_color=RED, outter_color=YELLOW)
        fx2 = DotOnPlane(2, 4, inner_color=PURPLE_C, outter_color=YELLOW)
        fx1_label = Tex(r"f_{1}").next_to(fx1, DOWN).scale(0.5)
        fx2_label = Tex(r"f_{2}").next_to(fx2, DOWN).scale(0.5)
        hx1 = DotOnPlane(2, 1, inner_color=RED, outter_color=GREEN)
        hx2 = DotOnPlane(4, 4, inner_color=PURPLE, outter_color=GREEN)
        hx1_label = Tex(r"h_{1}").next_to(hx1, DOWN).scale(0.5)
        hx2_label = Tex(r"h_{2}").next_to(hx2, DOWN).scale(0.5)
        self.play(
            *[ShowCreation(mob)
            for mob in [fx1_label, hx1_label, fx1, hx1]]
        )
        self.wait(3)

        self.play(x_value_tracker.animate.set_value(4), run_time=8)
        self.play(
            *[ShowCreation(mob)
            for mob in [fx2_label, hx2_label, fx2, hx2]]
        )
        self.wait(3)

        self.play(*[
                Uncreate(mob)
                for mob in [
                    x_to_g, gx_to_gy, gy_to_fx, fx_to_hx, fx0_label, hx0_label,
                    x0, gx0, gy0, hx0
                ]
            ])
        self.wait(3)

        # 30
        tangent_1 = self.get_secant_line(plane, f_graph, 1, 2, 0.2)
        tangent_2 = self.get_secant_line(plane, h_graph, 2, 4, 0.2)

        self.play(
            ShowCreation(tangent_1),
            ShowCreation(tangent_2)
        )
        
        self.wait(2)
        self.play(self.off(h_graph, hx1, hx2, tangent_2, void=False))
        _h = h_graph.copy()
        _hx1 = hx1.copy()
        _hx2 = hx2.copy()
        _t2 = tangent_2.copy()
        self.play(
            ReplacementTransform(f_graph.copy(), _h, run_time=3),
            ReplacementTransform(fx1.copy(), _hx1, run_time=3),
            ReplacementTransform(fx2.copy(), _hx2, run_time=3),
            ReplacementTransform(tangent_1.copy(), _t2, run_time=3)
        )
        self.on(h_graph, hx1, hx2, tangent_2)
        self.remove(_h, _hx1, _hx2, _t2)
        self.wait()

        cs1 = self.cross_center(fx1, fx2)
        cs2 = self.cross_center(hx1, hx2)

        dashed_line_config = dict(dash_length=0.2, stroke_width=7)
        dy_line_1 = DashedLine(start=cs1, end=fx2, **dashed_line_config).set_color(YELLOW)
        dy_line_2 = DashedLine(start=cs2, end=hx2, **dashed_line_config).set_color(YELLOW)
        dy_label = BraceLabel(dy_line_1, r"\Delta y_{f}", RIGHT)
        dy_label.label.set_color(YELLOW)
        dy_label_f = BraceLabel(dy_line_2, r"\Delta y_{h}", RIGHT)
        dy_label_f.label.set_color(YELLOW)
        dx_line_1 = DashedLine(start=fx1, end=cs1, **dashed_line_config).set_color(RED_E)
        dx_line_2 = DashedLine(start=hx1, end=cs2, **dashed_line_config).set_color(RED_B)
        dx_label_1 = BraceLabel(dx_line_1, r"\Delta x_{f}", DOWN)
        dx_label_1.label.set_color(RED_E)
        dx_label_2 = BraceLabel(dx_line_2, r"\Delta x_{h}", DOWN)
        dx_label_2.label.set_color(RED_B)

        equation = VGroup(
            Tex(r"\Delta y_{h}", "=", r"\Delta y_{f}"),
            Tex(r"\Delta x_{h}", "=", r"2\Delta x_{f}"),
            Tex(r"\frac{\Delta y_{h}}{\Delta x_{h}}",
                "=", 
                r"\frac{\Delta y_{f}}{2\Delta x_{f}}",
                "=", #3
                r"\frac{1}{2}\frac{\Delta y_{f}}{\Delta x_{f}}" #4
            )
        ).arrange(DOWN).next_to(formulas[2], DOWN)
        equation[0][0].set_color(YELLOW)
        equation[0][2].set_color(YELLOW)
        equation[1][0].set_color(RED_B)
        equation[1][2].set_color(RED_E)
        equation[2][0][0:3].set_color(YELLOW)
        equation[2][2][0:3].set_color(YELLOW)
        equation[2][0][4:7].set_color(RED_B)
        equation[2][2][5:8].set_color(RED_E)
        equation[2][4][3:6].set_color(YELLOW)
        equation[2][4][7:11].set_color(RED_E)

        self.play(
            ShowCreation(dy_line_1),
            ShowCreation(dy_label),
            self.off(h_graph, f_graph, void=False)
        )
        self.wait()
        self.play(
            TransformFromCopy(dy_line_1.copy(), dy_line_2),
            TransformFromCopy(dy_label.copy(), dy_label_f)
        )
        self.wait()
        # NOTE without 808, 811 and 812 will be wrong, WHY?
        self.add(dy_label.label, dy_label_f.label)
        self.play(
            ShowCreation(equation[0]),
            TransformFromCopy(dy_label.label.copy(), equation[0][2].copy()),
            TransformFromCopy(dy_label_f.label.copy(), equation[0][0].copy()),
        )
        self.remove(dy_label.label, dy_label_f.label)

        self.play(
            ShowCreation(dx_line_1),
            ShowCreation(dx_label_1),
            self.off(dy_line_1, dy_line_2, dy_label, dy_label_f, void=False)
        )
        self.wait()
        self.play(
            TransformFromCopy(dx_line_1.copy(), dx_line_2), 
            # What?
            TransformFromCopy(dx_label_1.copy(), dx_label_2),
        )
        self.add(dx_label_2.label, dx_label_1.label)
        self.play(
            ShowCreation(equation[1]),
            TransformFromCopy(dx_label_1.label.copy(), equation[1][2].copy()),
            TransformFromCopy(dx_label_2.label.copy(), equation[1][0].copy()),
        )
        self.wait()
        self.play(
            ShowCreation(blackboard_3), 
            self.on(dy_line_1, dy_line_2, dy_label, dy_label_f, void=False)
        )
        equation[2].next_to(blackboard_3.get_left())
        self.play(Write(equation[2][0:3]))
        self.wait(1)
        equation[2][3:5].next_to(equation[2][0])
        self.play(ReplacementTransform(equation[2][1:3], equation[2][3:5]))
 
