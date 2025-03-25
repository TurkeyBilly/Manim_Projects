from manimlib import *



# manimgl C:\Users\jiant\anaconda3\envs\manim\projects\GL\revolution_of_functions.py

class Produced(ThreeDScene):
    def construct(self):
        def get_y(x):
            if x>=2 and x<=4:
                return -x**2+ 6*x - 8

        a = FunctionGraph(get_y, [2, 4, 0.1], stroke_opacity=0.1, stroke_width=1.5)
        a.close_path()
        #a.set_opacity(0.1)
        fr: CameraFrame = self.camera.frame
        b = ThreeDAxes([-5, 5, 1],[-5, 5, 1],[-5, 5, 1])
        b.add_coordinate_labels()
        self.add(b.get_axis_labels())
        self.add(a, b)
        fr.set_euler_angles(45*DEGREES, 25*DEGREES, -45*DEGREES)
        b = VGroup()
        for i in range(0, 3600, 1):
            b.add(a.rotate_about_origin(i*DEGREES/10, axis=Y_AXIS).copy())
        self.add(b)
        k = a.copy().shift(3.5*UP+3.5*LEFT).set_opacity(0.5)
        self.add(k)
        b2 = BraceLabel(k, r'h=-x^{2}+6x-8', RIGHT)
        b3 = BraceLabel(k, r'dx', DOWN)
        self.add(b2, b3)


class Planner(Scene):
    def construct(self):
        def get_y(x):
            if x>=2 and x<=4:
                return -x**2+ 6*x - 8

        fr: CameraFrame = self.camera.frame
        fr.scale(0.35).shift(1.7*RIGHT+0.5*UP)
        a = FunctionGraph(get_y, [2, 4, 0.1], fill_opacity=0.8)
        a.close_path()
        b = NumberPlane()
        b.add_coordinate_labels()
        self.add(b.get_axis_labels())
        dot1 = Dot([2.3, get_y(2.3), 0], color=BLUE).scale(0.35)
        dot0 = Dot([0, get_y(2.3), 0], color=YELLOW).scale(0.35)
        dl1 = DashedLine(dot0, dot1)
        dot2 = Dot([3.7, get_y(3.7), 0], color=RED).scale(0.35)
        dl2 = DashedLine(dot2, dot1, color=RED)
        dl3 = Line(dot2, dot0)
        brace1 = BraceLabel(dl1, 'r', UP, label_scale=0.35, font_size=30, buff=0.1, label_buff=0.1)
        brace2 = BraceLabel(dl3, 'R', DOWN, label_scale=0.35, font_size=30, buff=0.1, label_buff=0.1)
        brace3 = BraceLabel(dl2, 'x', UP, label_scale=0.35, font_size=30, buff=0.1, label_buff=0.1)
        function_lable = Tex(
            r'y=-x^{2}+6x-8\left\{2\le x\le4\right\}'
        ).move_to(a.get_top()+0.2*UP).scale(0.35)
        point_lable1 = Tex('y').next_to(dot0, LEFT)

        def solve_x(y):
            return [3+math.sqrt(1-y), 3+math.sqrt(1-y)]

        dotx1 = Dot([2.3, 0, 0], color=RED).scale(0.35)
        dotx2 = Dot([3.7, 0, 0], color=RED).scale(0.35)
        point_lable2 = Tex('y').next_to(dot0, 0.2*LEFT).scale(0.35)
        point_lablex10 = Tex(r'x_{1}', color=RED).next_to(dotx1, 0.1*DOWN+0.025*LEFT).scale(0.35)
        point_lablex11 = Tex(r'3-\sqrt{1-1y}').next_to(point_lablex10, 0.1*DOWN).scale(0.35)
        point_lablex20 = Tex(r'x_{2}', color=RED).next_to(dotx2, 0.1*DOWN+0.025*LEFT).scale(0.35)
        point_lablex21 = Tex(r'3+\sqrt{1-1y}').next_to(point_lablex20, 0.1*DOWN).scale(0.35)
        self.add(
            brace2, a, b, dot1, dot0, dl1, brace1, dl2, dot2, function_lable,
            dotx1, dotx2, point_lable2, point_lablex10, point_lablex11, point_lablex20,
            point_lablex21, BackgroundRectangle(point_lablex11, color=RED), 
            BackgroundRectangle(point_lablex21, color=RED), brace3,
            DashedLine(dotx1, dot1), DashedLine(dotx2, dot2)
        )


class TestCopy(Scene):
    def construct(self):
        cir = Circle()
        brace0 = BraceLabel(cir, 'r')
        self.add(brace0)
        print(True)
        brace1 = brace0.copy()
        print(True)
        self.add(brace1.shift(UP))