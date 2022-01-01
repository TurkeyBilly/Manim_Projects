from types import FunctionType
from manimlib import *


# manimgl C:\Users\jiant\anaconda3\envs\manim\projects\GL\advanced_square_curve.py
# Numbox Referenced from https://www.bilibili.com/video/BV1Sf4y147s2?spm_id_from=333.999.0.0, by author widcardw
class TextBox(Scene):
    def construct(self):
        flash_dict = {
            "line_length": 0.5,
            "num_lines": 12,
            "flash_radius": 0.5,
            "line_stroke_width": 3,
            "run_time": 2,
        }
        nb = NumberBox(scale_factor=1).move_to(2*UP, DOWN)
        self.add(nb)
        self.wait()
        nb.start_tracing(self, flash_dict)
        self.embed()


class Happy2022(Scene):
    def construct(self):
        flash_dict = {
            "line_length": 0.5,
            "num_lines": 12,
            "flash_radius": 0.5,
            "line_stroke_width": 3,
            "run_time": 2,
        }
        TWO = NumberBoxGroup([3, 4, 10, 11])
        self.add(TWO)
        # TWO.start_tracing(self, flash_dict)


class FinalWay2022(Scene):
    def construct(self):
        flash_dict = {
            "line_length": 0.5,
            "num_lines": 12,
            "flash_radius": 0.5,
            "line_stroke_width": 3,
            "run_time": 2,
        }
        nb = VGroup()
        nb_sub = VGroup()
        v = [2*UP, UP, ORIGIN, DOWN, 2*DOWN]
        h = [LEFT, ORIGIN, RIGHT]
        for i in v:
            for j in h:
                nb_sub.add(NumberBox(scale_factor=0.5).move_to(i+j))
            nb.add(nb_sub)
        nb = nb[0]
        nb2 = nb.copy()
        # NumberBox().start_tracing(self, flash_dict, 4, False)
        emp_list = [3, 4, 10, 11]
        emp_list2 = [4,7,10]
        just = 0
        for i in emp_list:
            nb.remove(nb[i-just])
            just += 1
        just = 0
        for k in emp_list2:
            nb2.remove(nb2[k-just])
            just += 1
        nb3 = nb.copy()
        nb4 = nb.copy() 
        self.add(nb.shift(5*RIGHT), nb2.shift(1.7*LEFT), nb3.shift(1.7*RIGHT), nb4.shift(5*LEFT))
        for i in range(len(nb)):
            if isinstance(nb[i], NumberBox):
                nb[i].start_tracing(self, flash_dict, 4, False)


class Hope(Scene):
    def construct(self):
        flash_dict = {
            "line_length": 0.5,
            "num_lines": 12,
            "flash_radius": 0.5,
            "line_stroke_width": 3,
            "run_time": 2,
        }
        nb = VGroup()
        nb_sub = VGroup()
        v = [2*UP, UP, ORIGIN, DOWN, 2*DOWN]
        h = [LEFT, ORIGIN, RIGHT]
        for i in v:
            for j in h:
                nb_sub.add(NumberBox(scale_factor=0.5).move_to(i+j))
            nb.add(nb_sub)
        nb = nb[0]
        emp_list = [3, 4, 10, 11]
        just = 0
        for i in emp_list:
            nb.remove(nb[i-just])
            just += 1
        def get_2():
            return nb.copy()
        def doit(mob):
            for i in range(len(mob)):
                mob[i].start_tracing(self, flash_dict, 4, False)
        a = get_2()
        self.add(a)
        doit(a)
        self.wait(4)


class NumberBox(VGroup):
    def __init__(self, line_width: int = 0.6, scale_factor: int = 3.5, *vmobjects, **kwargs):
        super().__init__(*vmobjects, **kwargs)
        x, y = RIGHT, UP
        self.line_width = line_width
        self.scale_factor = scale_factor
        color_code = f"""
            vec3 blue = vec3{tuple(hex_to_rgb(BLUE))};
            vec3 red = vec3{tuple(hex_to_rgb(RED))};
            vec3 green = vec3{tuple(hex_to_rgb(GREEN))};
            color.rgb = mix(blue, red, (point.x));
            """
        self.square = Square().scale(self.scale_factor).set_color_by_code(
            color_code
        )
        self.dot_a = Dot(color=BLUE).move_to((-x+y)*self.scale_factor).scale(scale_factor*1.5)
        self.dot_b = Dot(color=RED).move_to((x+y)*self.scale_factor).scale(scale_factor*1.5)
        self.dot_c = Dot(color=RED).move_to((x-y)*self.scale_factor).scale(scale_factor*1.5)
        self.dot_d = Dot(color=BLUE).move_to((-x-y)*self.scale_factor).scale(scale_factor*1.5)
        self.dot_a.add_updater(
            lambda mob: mob.move_to(self.square.get_center() + (-x+y)*self.scale_factor)
        )
        self.dot_b.add_updater(
            lambda mob: mob.move_to(self.square.get_center() + (x+y)*self.scale_factor)
        )
        self.dot_c.add_updater(
            lambda mob: mob.move_to(self.square.get_center() + (x-y)*self.scale_factor)
        )
        self.dot_d.add_updater(
            lambda mob: mob.move_to(self.square.get_center() + (-x-y)*self.scale_factor)
        )
        self.dots = VGroup(
            self.dot_a,
            self.dot_b,
            self.dot_c,
            self.dot_d
        )
        self.ab = Line().set_color_by_code(color_code)
        self.bc = Line().set_color(RED)
        self.cd = Line().set_color_by_code(color_code)
        self.da = Line().set_color(BLUE)
        self.lines = VGroup(
            self.ab,
            self.bc,
            self.cd,
            self.da
        )
        self.trace = VGroup()
        self.add(
            self.square,
            self.trace,
            *self.dots
        )
        # self.scale(0.1)
    '''
    def move_to(self, point_or_mobject, aligned_edge=ORIGIN, coor_mask=np.array([1, 1, 1])):
        x, y = RIGHT, UP
        self.square.move_to(point_or_mobject, aligned_edge=aligned_edge, coor_mask=coor_mask)
        self.trace.move_to(point_or_mobject, aligned_edge=aligned_edge, coor_mask=coor_mask)
        self.dot_a.move_to(point_or_mobject + (-x+y)*self.scale_factor)
        self.dot_b.move_to(point_or_mobject + (x+y)*self.scale_factor)
        self.dot_c.move_to(point_or_mobject + (x-y)*self.scale_factor)
        self.dot_d.move_to(point_or_mobject + (-x-y)*self.scale_factor)
        return self 
        '''

    def _get_dot_updater(self, tar: Mobject, rate: int = 0.07) -> FunctionType:
        return lambda mob, dt: mob.shift((tar.get_center() - mob.get_center()) * dt* rate * 1/self.scale_factor)

    @staticmethod
    def _get_line_connection_updater(a: Dot, b: Dot):
        return lambda line: line.put_start_and_end_on(a.get_center(), b.get_center())

    def _get_center(self):
        return (sum(self.square.get_center()))

    def start_tracing(self, scene: Scene, flash_dict: dict = None, _time: float = 4, end_effect = True):
        # NOTE Using add(self.dots) will appear bugs!! Have to add them all
        self.add(*self.dots, self.lines)
        self.dot_a.clear_updaters()
        self.dot_b.clear_updaters()
        self.dot_c.clear_updaters()
        self.dot_d.clear_updaters()
        # self.add_updater(lambda mob, dt: mob.shift(dt*LEFT))
        # assert(self.dots[0] is self.dot_a)
        self.dot_a.add_updater((self._get_dot_updater(self.dot_b)))
        self.dot_b.add_updater((self._get_dot_updater(self.dot_c)))
        self.dot_c.add_updater((self._get_dot_updater(self.dot_d)))
        self.dot_d.add_updater((self._get_dot_updater(self.dot_a)))
        self.ab.add_updater(NumberBox._get_line_connection_updater(self.dot_a, self.dot_b))
        self.bc.add_updater(NumberBox._get_line_connection_updater(self.dot_b, self.dot_c))
        self.cd.add_updater(NumberBox._get_line_connection_updater(self.dot_c, self.dot_d))
        self.da.add_updater(NumberBox._get_line_connection_updater(self.dot_d, self.dot_a))
        self.trace.add_updater(
            lambda a, dt: a.add(
                *[mob.copy().clear_updaters().set_stroke(width=self.line_width) for mob in self.lines]
            )
        )
        if end_effect:
            scene.wait(_time)
            # scene.play(*[FadeOut(mb) for mb in [*self.dots]])
            scene.play(
                Flash(
                    self.get_center(),
                    **flash_dict
                ) if flash_dict else
                Flash(
                    self.get_center(),
                )
            )
        return self

class NumberBoxGroup(VGroup):
    def __init__(
        self, 
        null_array: list =[],
        scale_factor_: float=.5, 
        *vmobjects, 
        **kwargs):
        super().__init__(*vmobjects, **kwargs)
        # self.scale_factor_ = scale_factor_
        self.nb = NumberBox(scale_factor=scale_factor_)
        self.null_array = null_array
        num_array: VGroup = (self.nb*15).arrange_in_grid(5, 3, buff=0)
        # num_array: VGroup = self._form_group()
        '''for i in range(num_array.__len__()):
            if i in null_array:
                num_array[i].set_color(BLACK)'''
        self.add(*num_array)

    def _form_group(self, row=5, col=3):
        nb = VGroup()
        v = [2*UP, UP, ORIGIN, DOWN, 2*DOWN]
        h = [LEFT, ORIGIN, RIGHT]
        for n1, i in enumerate(v):
            for n2, j in enumerate(h):
                if not (n1*3+n2) in self.null_array:
                    nb.add(NumberBox(scale_factor=0.5).move_to(i+j))
        return nb

    def start_tracing(self, scene: Scene, flash_dict: dict = None, _time: float = 4, end_effect=True):
        print(len(self))
        for i in range(len(self)):
            self[i].start_tracing(
                scene,
                flash_dict,
                # end_effect=False
            )
            if not end_effect:
                return self
        scene.wait(_time)
        scene.play(
            *[Flash(
                n._get_center(),
                **flash_dict
            ) if flash_dict else
            Flash(
                n._get_center(),
            ) for n in self]
        )


class CoolNumber(VGroup):
    def __init__(self, emp_list = [3, 4, 10, 11], *vmobjects, **kwargs):
        self.flash_dict = {
            "line_length": 0.5,
            "num_lines": 12,
            "flash_radius": 0.5,
            "line_stroke_width": 3,
            "run_time": 2,
        }
        super().__init__(*vmobjects, **kwargs)
        self.nb = VGroup()
        self.nb_sub = VGroup()
        v = [2*UP, UP, ORIGIN, DOWN, 2*DOWN]
        h = [LEFT, ORIGIN, RIGHT]
        for i in v:
            for j in h:
                self.nb_sub.add(NumberBox(scale_factor=0.5).move_to(i+j))
            self.nb.add(self.nb_sub)
        self.nb = self.nb[0]
        print(*self.nb)
        # NumberBox().start_tracing(self, flash_dict, 4, False)
        self.emp_list = emp_list
        just = 0
        for i in self.emp_list:
            self.nb.remove(self.nb[i-just])
            just += 1
        self.add(*self.nb)

    def start_tracing(self):
        for i in range(len(self.nb)):
            if isinstance(self.nb[i], NumberBox):
                self.nb[i].start_tracing(self, self.flash_dict, 4, False)


class NormalNumber(VGroup):
    def __init__(self, emp_list = [3, 4, 10, 11], sf=0.5, *vmobjects, **kwargs):
        self.flash_dict = {
            "line_length": 0.5,
            "num_lines": 12,
            "flash_radius": 0.5,
            "line_stroke_width": 3,
            "run_time": 2,
        }
        super().__init__(*vmobjects, **kwargs)
        self.nb = VGroup()
        self.nb_sub = VGroup()
        v = [2*UP, UP, ORIGIN, DOWN, 2*DOWN]
        h = [LEFT, ORIGIN, RIGHT]
        for i in v:
            for j in h:
                self.nb_sub.add(Square(color=GREY).move_to(i+j).scale(sf))
            self.nb.add(self.nb_sub)
        self.nb = self.nb[0]
        print(*self.nb)
        # NumberBox().start_tracing(self, flash_dict, 4, False)
        self.emp_list = emp_list
        just = 0
        for i in self.emp_list:
            self.nb.remove(self.nb[i-just])
            just += 1
        self.add(*self.nb)


class LastTry(Scene):
    def construct(self):
        a = CoolNumber()
        self.add(a.move_to(5*LEFT))
        b = CoolNumber([4,7,10]).move_to(1.7*LEFT)
        c = CoolNumber().move_to(1.7*RIGHT)
        d = CoolNumber().move_to(5*RIGHT)
        self.add(b, c, d)
        a.start_tracing()
        b.start_tracing()
        c.start_tracing()
        d.start_tracing()
        self.wait(10)


class Final(Scene):
    def construct(self):
        fr: CameraFrame = self.camera.frame
        fr.save_state()
        a0 = NormalNumber()
        self.add(a0.move_to(5*LEFT))
        b0 = NormalNumber([4,7,10]).move_to(1.7*LEFT)
        c0 = NormalNumber().move_to(1.7*RIGHT)
        d0 = NormalNumber().move_to(5*RIGHT)
        e0 = NormalNumber([0,1,3,4,6,7,9,10,12,13]).move_to(5*RIGHT)
        self.add(b0, c0, e0)
        self.wait(2)
        tx1 = Text('新年快乐!', font='楷体', color=RED).scale(3).shift(4.2*UP)
        bx1 = SurroundingRectangle(tx1, color=YELLOW)
        p = VGroup(
            Text('回首2021', font='楷体'),
            Text('也许对你我来说并无乐趣', font='楷体'),
            Text('又或者你遇到了很多烦恼', font='楷体'),
            Text('但即便如此', font='楷体'),
            Text('拥有一个灰色的过去', font='楷体'),
            Text('也丝毫不会另我们', font='楷体'),
            Text('怀疑未来的灿烂色彩', font='楷体'),
        )
        fr.scale(1.5)
        self.play(fr.animate.scale(1.5), fr.animate.shift(4*RIGHT))
        p.arrange(DOWN)
        p.move_to(10.5*RIGHT + UP)
        self.play(Write(p[0]), run_time = 1.5)
        self.play(Write(p[1]), Write(p[2]), run_time =2)
        self.play(
            Write(p[3]),
            TransformMatchingShapes(e0, d0), run_time=3
        )
        a = CoolNumber()
        a.move_to(5*LEFT)
        b = CoolNumber([4,7,10]).move_to(1.7*LEFT)
        c = CoolNumber().move_to(1.7*RIGHT)
        d = CoolNumber().move_to(5*RIGHT)
        olds = [a0, b0, c0, d0]
        news = [a,b,c,d]
        self.play(
            Write(p[4]),
            *[TransformMatchingShapes(m1, m2) for m1, m2 in zip(olds, news)],
            rate_func=rush_into
        )
        self.wait(2)
        self.play(Write(p[5]))
        #a.start_tracing()
        #b.start_tracing()
        #c.start_tracing()
        #d.start_tracing()
        self.wait(1)
        self.play(Write(p[6]), run_time = 3)
        self.play(fr.animate.restore())
        self.play(
            fr.animate.shift(1.3*UP), 
            Write(tx1), 
            ShowCreation(bx1),
            *[FadeOut(mob) for mob in p]
        )
        flash_dict = {
            "line_length": 0.5,
            "num_lines": 12,
            "flash_radius": 0.5,
            "line_stroke_width": 3,
            "run_time": 2,
        }
        self.play(
            *[Flash(po, **flash_dict) for po in [1.7*LEFT, 1.7*RIGHT, 5*LEFT, 5*RIGHT]]
        )
        self.wait(8)


        

