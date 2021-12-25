from types import FunctionType
from manimlib import *


def get_heart(size: float = 0.08):
    kwarg = {'color' : RED, 'fill_opacity' : 1.0}
    sq = Square(**kwarg)
    sq.rotate(PI/4)
    cir1 = Circle(**kwarg)
    cir2 = Circle(**kwarg)
    pos = math.sqrt(2)/2
    cir1.move_to([pos,pos,0])
    cir2.move_to([-pos,pos,0])
    return VGroup(sq.copy(), cir1.copy(), cir2.copy()).scale(size)

class Main(Scene):
    def construct(self):
        mob = Triangle()
        mob
        t1 = Polygon(1.4*UP, -1.7*LEFT, 1.7*LEFT)
        t2 = t1.copy()
        t3 = t1.copy()
        rec = Polygon(0.5*LEFT+2*UP, 0.5*RIGHT+2*UP, 0.5*RIGHT,0.5*LEFT)
        gp = VGroup(t1+t2+t3+rec)
        
        def create_top_to_down_connection_updator(up: Mobject, down: Mobject, dis: int = 0) -> FunctionType:
            return lambda mob: mob.move_to(up.get_bottom()-down.get_top()+down.get_center()+dis*DOWN)
        
        def always_up_aligh_with_mid(up: Mobject, down: Mobject):
            down.add_updater(lambda mob: mob.move_to(up.get_center()-down.get_top()+down.get_center()))
        
        always_up_aligh_with_mid(t1, t2)
        always_up_aligh_with_mid(t2, t3)
        rec.add_updater(create_top_to_down_connection_updator(t3, rec))
        self.play(ShowCreation(t1))
        self.play(t1.animate.shift(0.5*UP), ShowCreation(t2))
        self.play(t1.animate.shift(0.5*UP), ShowCreation(t3))
        self.play(t1.animate.shift(0.5*UP).scale(0.75), t3.animate.scale(1.25))
        self.play(t1.animate.shift(0.5*UP), ShowCreation(rec))
        
        self.play(
            t1.animate.set_color(GREEN).set_fill(GREEN, 1),
            t2.animate.set_color(GREEN).set_fill(GREEN, 1),
            t3.animate.set_color(GREEN).set_fill(GREEN, 1),
            rec.animate.set_color(DARK_BROWN).set_fill(DARK_BROWN, 1)
        )
        self.add(t3)
        self.wait(1)
        self.play(gp.animate.shift(4.5*LEFT))
        
        # Love Scene!
        kwarg_before = {'color' : RED, 'fill_opacity' : 0.3}
        kwarg = {'color' : RED, 'fill_opacity' : 1.0}
        pos = math.sqrt(2)/2
        sq_before = Square(**kwarg_before)
        cir1_before = Circle(**kwarg_before)
        cir2_before = Circle(**kwarg_before)
        self.play(*[ShowCreation(mob) for mob in [sq_before,cir1_before,cir2_before]], run_time = 1.8)
        self.wait()
        anim = (sq_before.animate.rotate(PI/4),
            cir1_before.animate.move_to([pos,pos,0]),
            cir2_before.animate.move_to([-pos,pos,0]),
        )
        self.play(*anim, run_time = 1.8, rate_func = smooth)
        sq = Square(**kwarg)
        sq.rotate(PI/4)
        cir1 = Circle(**kwarg)
        cir2 = Circle(**kwarg)
        cir1.move_to([pos,pos,0])
        cir2.move_to([-pos,pos,0])
        self.wait()
        before = VGroup(sq_before,cir1_before,cir2_before)
        after = VGroup(sq, cir1, cir2)
        self.play(Transform(before, after), run_time = 1.5, rate_func = smooth)
        self.wait()
        self.play(Transform(before, h1:=get_heart()))
        
        # self.add(NumberPlane())
        POS = [3.5*LEFT+0.5*UP, 0.7*UP+5.5*LEFT, 1.3*UP+4*LEFT, 1.6*UP+5*LEFT, 2.5*UP+4.5*LEFT]
        ANGLE = [-35*DEGREES, 45*DEGREES, 60*DEGREES, -35*DEGREES, 0]
        cps = h1*5
        self.play(
            *[i.animate.move_to(p).rotate(ang) for p, ang, i in zip(POS, ANGLE, cps)],
            FadeOut(before)
        )
        # self.play(*[m.animate.shift([-m.get_center()[0], 0, 0]) for m in self.mobjects])
        self.play((gp+cps).animate.move_to(ORIGIN+1.3*UP))
        tx = Text('Merry Christmas!').add_background_rectangle(BLUE).scale(3).shift(2.3*DOWN)
        self.play(Write(tx),
        ShowCreation(SurroundingRectangle(tx, color=YELLOW)),
        run_time=2
        )
