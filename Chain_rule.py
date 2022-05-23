from manimlib import *


__manimlib_version__ = "1.5.0"
__python_version__ = "3.9.0"
__start_date__ = "2022.1.24"

commend_line = r'''
manimgl C:\Users\jiant\anaconda3\envs\manim\projects\GL\chain_rule_new.py
-o: save and open
-n10: start from scene 10
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
        
        self.play(Write(self.chainrule)); self.wait()
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

        self.play(Write(fg1))
        self.wait()

        no_transed.shift(2*DOWN)
        self.wait(3)

        arr = CurvedArrow(fg0.get_left(), transed.get_left() + 2*DOWN).set_color(BLUE)
        what_happened = Text('发生了什么？', font='仿宋').move_to(arr.get_center() + 2.5* LEFT)
        self.play(TransformMatchingTex(fg1, fg0),)
        self.play(
            TransformMatchingTex(fg0.copy(), __copied:=transed.copy().shift(2*DOWN)),
            *[ShowCreation(mob) for mob in [arr, what_happened]],
            transed.animate.shift(2*DOWN)
        )
        self.remove(__copied)
        self.wait(3)
        title = Text('Part 1', font='仿宋')
        title2 = Text('纯线性组合', font='仿宋')
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
        self.wait(2)
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
