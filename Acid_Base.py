from typing import Final
from manimlib import *
from tkinter import Tk, simpledialog
from tkinter import messagebox


__python_version__ = 3.9

__doc__ = r'''
Run the code in the follwing format in command line / anaconda prompt
    manimgl [file_path] [Scene_name]

manimgl C:\Users\jiant\anaconda3\envs\manim\projects\GL\Acid_Base.py FinalScene
'''

# manimgl C:\Users\jiant\anaconda3\envs\manim\projects\GL\Acid_Base.py WeakAcidStrongBase
class WeakAcidStrongBase(Scene):
    def construct(self, pKa: float = 4.74, acid_volume: float = 10.0, 
                molarity_titrated: float = 0.5, molarity_titrant: float = 0.1, demo: bool = False
        ) -> None:
        fr: CameraFrame = self.camera.frame
        fr.scale(2).shift(4*UP+6*RIGHT)

        def functionAcid(pKa, AMinus, HA, addedBase):
            #A- and HA and addedBase are in moles, not molarity
            return pKa + math.log10((AMinus + addedBase) / (HA - addedBase))

        def functionBase(pKb, B, BHPlus, addedAcid):
            #Still all in moles, not molarity
            return 14 - (pKb + math.log10((B + addedAcid) / (BHPlus - addedAcid)))

        def ice_table_WASB(molar_A_minus: float, ka: float, reverse: bool = True) -> float:
            kb = 1/ka if reverse else ka
            c = - molar_A_minus * kb
            x = (kb + math.sqrt(kb**2 - 4 * c))/2
            return x

        def calc_pH_WASB(pKa: float, strong_base_volume: float, strong_base_molarity: float,
                        weak_acid_volume: float, weak_acid_molarity: float, reverse: bool = False
            ) -> typing.Sequence[float]:
            """ 
            Calculate pH for Weak Acid Strong Base
            Const: pKa, both molarities, and weak acid volume
            Changing: strong base volume
            Extra arg: reverse to change it to Weak Base Strong Acid TODO
            Returns: Tuple(pH, [A], [HA-], pOH)
            """

            total_volume = weak_acid_volume + strong_base_volume
            # mole of initial base (NaOH for example)
            mole_base = strong_base_molarity * strong_base_volume
            # mole of HA initial (CH3COOH for example)
            mole_acid = weak_acid_molarity * weak_acid_volume
            # mole of A- initial (CH3COO- for example)
            mole_A_minus = 0
            molarity_A_minus = mole_A_minus / total_volume
            molarity_acid = mole_acid / total_volume
            # Tuple of ([A], [HA-], pOH)
            return_tuple = (molarity_acid, molarity_A_minus)
            # To determine if its before equiv, at equiv, or after
            if mole_base == 0:
                return ice_table_WASB(mole_acid / total_volume, 10**(-pKa)), *(molarity_acid, molarity_A_minus)

            elif mole_acid > mole_base:
                # Before equiv
                mole_acid -= mole_base
                mole_A_minus += mole_base
                molarity_A_minus = mole_A_minus / total_volume
                molarity_acid = mole_acid / total_volume
            elif mole_acid == mole_base:
                mole_acid -= mole_base
                mole_A_minus += mole_base
                molarity_A_minus = mole_A_minus / total_volume
                molarity_acid = mole_acid / total_volume
                return 14.0 + math.log10(ice_table_WASB(mole_base / total_volume, 10**(-pKa))), *(molarity_acid, molarity_A_minus)
            elif mole_acid <= mole_base:
                return 14.0 + math.log10((mole_base - mole_acid) / total_volume), *(0.0, mole_acid / total_volume)

            return pKa + math.log10((mole_A_minus) / (mole_acid)), *(molarity_acid, molarity_A_minus)

        # Volume of Acid needed in mL
        # acid_volume = 10.0
        # Molarity of Acid
        # molarity_titrated = .5
        # Molarity of Titrant
        # molarity_titrant = .1
        
        equivlibrium_mL_for_base = (molarity_titrated * acid_volume) / molarity_titrant
        # print(equivlibrium_mL_for_base)
        titrated = equivlibrium_mL_for_base * 2


        # pKa: Final = 4.74

        common_plane_config = dict(
            x_range=[0, titrated, titrated/10],
            height=FRAME_HEIGHT*1.6, width=FRAME_WIDTH*1.6
        )

        n_conf = {"y_axis_config": {"decimal_number_config": {
            "num_decimal_places": 3,
            "font_size": 36,
        }}}

        plane = NumberPlane(
            **common_plane_config, y_range=[0, 14.0, 2.0],
        ).scale(0.5).shift(0.5*LEFT)
        plane.add_coordinate_labels()
        self.add(
            plane.get_x_axis_label("mL", direction=RIGHT),
            plane.get_y_axis_label("pH", direction=UP)
        )

        y_max = molarity_titrated * titrated / (titrated)
        # y_max = 1

        a_conentration_plane = NumberPlane(
            **common_plane_config, **n_conf,
            y_range=[0, y_max, y_max / 7.],
        ).scale(0.5).shift(0.5*LEFT + 7.5*UP)
        a_conentration_plane.add_coordinate_labels()
        a_conentration_plane.add(
            a_conentration_plane.get_x_axis_label("mL", direction=RIGHT),
            a_conentration_plane.get_y_axis_label("[A-](M)", direction=UP)
        )

        ha_concentration_plane = NumberPlane(
            **common_plane_config, **n_conf,
            y_range=[0, y_max, y_max / 7.],
        ).scale(0.5).shift(13.*RIGHT + 7.5* UP)
        ha_concentration_plane.add_coordinate_labels()
        self.add(
            ha_concentration_plane.get_x_axis_label("mL", direction=UP),
            ha_concentration_plane.get_y_axis_label("[HA](M))", direction=UP)
        )

        oh_concentration_plane = NumberPlane(
            **common_plane_config, y_range=[0, 14, 2],
        ).scale(0.5).shift(13.*RIGHT)
        oh_concentration_plane.add_coordinate_labels()
        self.add(
            oh_concentration_plane.get_x_axis_label("mL", direction=RIGHT),
            oh_concentration_plane.get_y_axis_label("pOH", direction=UP)
        )

        self.add(plane, a_conentration_plane, ha_concentration_plane, oh_concentration_plane)

        graph = plane.get_graph(
            lambda x: calc_pH_WASB(pKa, x + 0.1, molarity_titrant, acid_volume, molarity_titrated)[0],
            use_smoothing=False, # step_size=.10,
            x_range=[0, titrated-1]
        )

        a_conc_graph = a_conentration_plane.get_graph(
            lambda x: calc_pH_WASB(pKa, x + 0.1, molarity_titrant, acid_volume, molarity_titrated)[2],
            use_smoothing=False, # step_size=.10,
            x_range=[0, titrated-1]
        )

        ha_conc_graph = ha_concentration_plane.get_graph(
            lambda x: calc_pH_WASB(pKa, x + 0.1, molarity_titrant, acid_volume, molarity_titrated)[1],
            use_smoothing=False, # step_size=.10,
            x_range=[0, titrated-1]
        )

        oh_conc_graph = oh_concentration_plane.get_graph(
            lambda x: 14 - calc_pH_WASB(pKa, x + 0.1, molarity_titrant, acid_volume, molarity_titrated)[0],
            use_smoothing=False, # step_size=.10,
            x_range=[0, titrated-1]
        )

        self.add(graph, a_conc_graph, ha_conc_graph, oh_conc_graph)
        if demo:
            self.wait(60)
            sys.exit()



class WeakBaseStrongAcid(Scene):
    def construct(self, pKb: float = 4.74, base_volume: float = 40.0, 
            base_molarity: float = .1, molarity_titrant: float = .1, demo: bool = False
        ) -> None:
        fr: CameraFrame = self.camera.frame
        fr.scale(2).shift(4*UP+6*RIGHT)

        def ice_table_WASB(molar_A_minus: float, kb: float, reverse: bool = False) -> float:
            kb = 1/kb if reverse else kb
            c = -molar_A_minus * kb
            x = (kb + math.sqrt(kb**2 - 4 * c))/2
            return x

        def calc_pH_WASB(pKb: float, strong_acid_volume: float, strong_acid_molarity: float,
                        weak_base_volume: float, weak_base_molarity: float, reverse: bool = False
            ) -> typing.Sequence[float]:
            """ 
            Calculate pH for Weak Acid Strong Base
            Const: pKa, both molarities, and weak acid volume
            Changing: strong base volume
            Extra arg: reverse to change it to Weak Base Strong Acid TODO
            Returns: Tuple(pH, [A], [HA-], pOH)
            """

            total_volume = weak_base_volume + strong_acid_volume
            # mole of initial base (NaOH for example)
            mole_base = weak_base_molarity * weak_base_volume
            # mole of HA initial (CH3COOH for example)
            mole_acid = strong_acid_molarity * strong_acid_volume
            # mole of A- initial (CH3COO- for example)
            mole_BH_plus = 0
            molarity_BH_plus = mole_BH_plus / total_volume
            molarity_base = mole_base / total_volume
            # To determine if its before equiv, at equiv, or after
            if mole_base == 0:
                return ice_table_WASB(mole_acid, 10**(-pKb), False), *(molarity_base, molarity_BH_plus)

            elif mole_acid < mole_base:
                # Before equiv
                mole_base -= mole_acid
                mole_BH_plus += mole_acid
                molarity_BH_plus = mole_BH_plus / total_volume
                molarity_base = mole_base / total_volume
            elif mole_acid == mole_base:
                mole_base -= mole_acid
                mole_BH_plus += mole_base
                molarity_BH_plus = mole_BH_plus / total_volume
                molarity_base = mole_base / total_volume
                return 14.0 + math.log10(ice_table_WASB(mole_base, 10**(-pKb))), *(molarity_base, molarity_BH_plus)
            elif mole_acid >= mole_base:
                return -math.log10((-mole_base + mole_acid) / total_volume), *(0.0, mole_base / total_volume)

            return 14 - pKb - math.log10((mole_BH_plus) / (mole_base)), *(molarity_base, molarity_BH_plus)

        # Volume of Base needed in mL
        # base_volume = 40.0
        # Molarity of Base
        # base_molarity = .1
        # Molarity of Titrant (Acid)
        # molarity_titrant = .1
        
        equivlibrium_mL_for_base = (base_molarity * base_volume) / molarity_titrant
        # print(equivlibrium_mL_for_base)
        titrated = equivlibrium_mL_for_base * 2


        # pKb = 4.74

        common_plane_config = dict(
            x_range=[0, titrated, titrated/10],
            height=FRAME_HEIGHT*1.6, width=FRAME_WIDTH*1.6
        )

        n_conf = {"y_axis_config": {"decimal_number_config": {
            "num_decimal_places": 3,
            "font_size": 36,
        }}}

        plane = NumberPlane(
            **common_plane_config, y_range=[0, 14.0, 2.0],
        ).scale(0.5).shift(0.5*LEFT)
        plane.add_coordinate_labels()
        self.add(
            plane.get_x_axis_label("mL", direction=RIGHT),
            plane.get_y_axis_label("pH", direction=UP)
        )

        y_max = base_molarity * titrated / (titrated)
        # y_max = 1

        b_conentration_plane = NumberPlane(
            **common_plane_config, **n_conf,
            y_range=[0, y_max, y_max / 7.],
        ).scale(0.5).shift(0.5*LEFT + 7.5*UP)
        b_conentration_plane.add_coordinate_labels()
        b_conentration_plane.add(
            b_conentration_plane.get_x_axis_label("mL", direction=RIGHT),
            b_conentration_plane.get_y_axis_label("[B](M)", direction=UP)
        )

        bh_concentration_plane = NumberPlane(
            **common_plane_config, **n_conf,
            y_range=[0, y_max, y_max / 7.],
        ).scale(0.5).shift(13.*RIGHT + 7.5* UP)
        bh_concentration_plane.add_coordinate_labels()
        self.add(
            bh_concentration_plane.get_x_axis_label("mL", direction=UP),
            bh_concentration_plane.get_y_axis_label("[BH+](M))", direction=UP)
        )

        oh_concentration_plane = NumberPlane(
            **common_plane_config, y_range=[0, 14, 2],
        ).scale(0.5).shift(13.*RIGHT)
        oh_concentration_plane.add_coordinate_labels()
        self.add(
            oh_concentration_plane.get_x_axis_label("mL", direction=RIGHT),
            oh_concentration_plane.get_y_axis_label("pOH", direction=UP)
        )

        self.add(plane, b_conentration_plane, bh_concentration_plane, oh_concentration_plane)

        graph = plane.get_graph(
            lambda x: calc_pH_WASB(pKb, x + 0.1, molarity_titrant, base_volume, base_molarity)[0],
            use_smoothing=False, # step_size=.10,
            x_range=[0, titrated-1]
        )

        b_conc_graph = b_conentration_plane.get_graph(
            lambda x: calc_pH_WASB(pKb, x + 0.1, molarity_titrant, base_volume, base_molarity)[1],
            use_smoothing=False, # step_size=.10,
            x_range=[0, titrated-1]
        )

        bh_conc_graph = bh_concentration_plane.get_graph(
            lambda x: calc_pH_WASB(pKb, x + 0.1, molarity_titrant, base_volume, base_molarity)[2],
            use_smoothing=False, # step_size=.10,
            x_range=[0, titrated-1]
        )

        oh_conc_graph = oh_concentration_plane.get_graph(
            lambda x: 14 - calc_pH_WASB(pKb, x + 0.1, molarity_titrant, base_volume, base_molarity)[0],
            use_smoothing=False, # step_size=.10,
            x_range=[0, titrated-1]
        )

        self.add(graph, b_conc_graph, bh_conc_graph, oh_conc_graph)
        if demo:
            self.wait(60)
            sys.exit()



class StrongAcidStrongBase(Scene):
    def construct(self, demo: bool = False):
        raise Exception
        fr: CameraFrame = self.camera.frame
        fr.scale(2).shift(4*UP+6*RIGHT)

        def calc_pH_WASB(pKb: float, strong_acid_volume: float, strong_acid_molarity: float,
                        weak_base_volume: float, weak_base_molarity: float, reverse: bool = False
            ) -> typing.Sequence[float]:
            """ 
            Calculate pH for Weak Acid Strong Base
            Const: pKa, both molarities, and weak acid volume
            Changing: strong base volume
            Extra arg: reverse to change it to Weak Base Strong Acid TODO
            Returns: Tuple(pH, [A], [HA-], pOH)
            """

            total_volume = weak_base_volume + strong_acid_volume
            # mole of initial base (NaOH for example)
            mole_base = weak_base_molarity * weak_base_volume
            # mole of HA initial (CH3COOH for example)
            mole_acid = strong_acid_molarity * strong_acid_volume
            # mole of A- initial (CH3COO- for example)
            mole_BH_plus = 0
            molarity_BH_plus = mole_BH_plus / total_volume
            molarity_base = mole_base / total_volume
            # To determine if its before equiv, at equiv, or after
            if mole_base == 0:
                return ice_table_WASB(mole_acid, 10**(-pKb), False), *(molarity_base, molarity_BH_plus)

            elif mole_acid < mole_base:
                # Before equiv
                mole_base -= mole_acid
                mole_BH_plus += mole_acid
                molarity_BH_plus = mole_BH_plus / total_volume
                molarity_base = mole_base / total_volume
            elif mole_acid == mole_base:
                mole_base -= mole_acid
                mole_BH_plus += mole_base
                molarity_BH_plus = mole_BH_plus / total_volume
                molarity_base = mole_base / total_volume
                return 14.0 + math.log10(ice_table_WASB(mole_base, 10**(-pKb))), *(molarity_base, molarity_BH_plus)
            elif mole_acid >= mole_base:
                return -math.log10((-mole_base + mole_acid) / total_volume), *(0.0, mole_base / total_volume)

            return 14 - pKb - math.log10((mole_BH_plus) / (mole_base)), *(molarity_base, molarity_BH_plus)

        # Volume of Base needed in mL
        base_volume = 40.0
        # Molarity of Base
        base_molarity = .1
        # Molarity of Titrant (Acid)
        molarity_titrant = .1
        
        equivlibrium_mL_for_base = (base_molarity * base_volume) / molarity_titrant
        # print(equivlibrium_mL_for_base)
        titrated = equivlibrium_mL_for_base * 2


        pKb = 4.74

        common_plane_config = dict(
            x_range=[0, titrated, titrated/10],
            height=FRAME_HEIGHT*1.6, width=FRAME_WIDTH*1.6
        )

        n_conf = {"y_axis_config": {"decimal_number_config": {
            "num_decimal_places": 3,
            "font_size": 36,
        }}}

        plane = NumberPlane(
            **common_plane_config, y_range=[0, 14.0, 2.0],
        ).scale(0.5).shift(0.5*LEFT)
        plane.add_coordinate_labels()
        self.add(
            plane.get_x_axis_label("mL", direction=RIGHT),
            plane.get_y_axis_label("pH", direction=UP)
        )

        oh_concentration_plane = NumberPlane(
            **common_plane_config, y_range=[0, 14, 2],
        ).scale(0.5).shift(13.*RIGHT)
        oh_concentration_plane.add_coordinate_labels()
        self.add(
            oh_concentration_plane.get_x_axis_label("mL", direction=RIGHT),
            oh_concentration_plane.get_y_axis_label("pOH", direction=UP)
        )

        self.add(plane, b_conentration_plane, bh_concentration_plane, oh_concentration_plane)

        graph = plane.get_graph(
            lambda x: calc_pH_WASB(pKb, x + 0.1, molarity_titrant, base_volume, base_molarity)[0],
            use_smoothing=False, # step_size=.10,
            x_range=[0, titrated-1]
        )

        oh_conc_graph = oh_concentration_plane.get_graph(
            lambda x: 14 - calc_pH_WASB(pKb, x + 0.1, molarity_titrant, base_volume, base_molarity)[0],
            use_smoothing=False, # step_size=.10,
            x_range=[0, titrated-1]
        )

        self.add(graph, oh_conc_graph)
        if demo:
            self.wait(60)
            sys.exit()


# manimgl C:\Users\jiant\anaconda3\envs\manim\projects\GL\Acid_Base.py FinalScene
class FinalScene(StrongAcidStrongBase, WeakAcidStrongBase, WeakBaseStrongAcid):
    def construct(self):
        strongAcid = ["HCl","HBr","HI","HNO3","H2SO4","HClO4"]
        strongBase = ["LiOH","NaOH","KOH","Ca(OH)2","Sr(OH)2","Ba(OH)2"]
        flagStrongAcid = False
        flagStrongBase = False
        pka = 0.0
        pkb = 0.0
        acid = ""
        base = ""
        cAcid = 0.0 #Concentration
        cBase = 0.0
        vAcid = 0.0 #Volume
        vBase = 0.0
        titrationStatus = False # False is titrating acid with base, True is titrating base with acid
        Tk()
        while True:
            acid = simpledialog.askstring("Acid","Please enter an acid", initialvalue="")
            if acid is not None:
                break

        if acid in strongAcid:
            flagStrongAcid=True

        warning = "Decimal ONLY! \n"

        if(not flagStrongAcid):
            try:
                pka = float(simpledialog.askstring(
                    "pKa","Please enter an the pKa for the entered weak acid", initialvalue=""))
            except ValueError:
                pka = float(simpledialog.askstring(
                    "pKa",f"{warning}Please enter an the pKa for the entered weak acid", initialvalue=""))

        while True:
            base = simpledialog.askstring("Base","Please enter a base", initialvalue="")
            if base is not None:
                break

        if base in strongBase:
            flagStrongBase = True

        if(not flagStrongBase):
            try:
                pkb = float(simpledialog.askstring(
                    "Kb","Please enter an the pKb for the entered weak base", initialvalue=""))
            except ValueError:
                pkb = float(simpledialog.askstring(
                    "Kb", f"{warning}Please enter an the pKb for the entered weak base", initialvalue=""))

        if (not flagStrongAcid) and (not flagStrongBase):
            raise Exception("Does not support weak-weak titration, please enter at least a strong base or acid")

        add_initial_value = "Acid"
        if flagStrongAcid and not flagStrongBase:
            add_initial_value = "Acid"

        if not flagStrongAcid and flagStrongBase:
            add_initial_value = "Base"

        t = simpledialog.askstring(
            "Choose Titrant",
            """
            Please enter 
            Acid if you are titrating base with acid
            Base if you are titrating acid with base.
            If initialvalue appears, go positive, do not change
            """, 
            initialvalue=add_initial_value
            )
        try:
            if(t == "Acid"):
                
                cAcid = float(simpledialog.askstring(
                    "Concentration of Acid", "Please enter the concentration of "+ acid, initialvalue=""))
                cBase = float(simpledialog.askstring(
                    "Concentration of Base","Please enter the concentration of "+ base, initialvalue=""))
                vBase = float(simpledialog.askstring(
                    "Volume of Base","Please enter the volume of " + base, initialvalue=""))
            else:
                cAcid = float(simpledialog.askstring(
                    "Concentration of Acid","Please enter the concentration of " + acid, initialvalue=""))
                cBase = float(simpledialog.askstring(
                    "Concentration of Base","Please enter the concentration of " + base, initialvalue=""))
                vAcid = float(simpledialog.askstring(
                    "Volume of Acid","Please enter the volume of " + acid, initialvalue=""))
        except ValueError:
            if(t == "Acid"):
                cAcid = float(simpledialog.askstring(
                    "Concentration of Acid",warning + " Please enter the concentration of " + acid, initialvalue=""))
                cBase = float(simpledialog.askstring(
                    "Concentration of Base","Please enter the concentration of " + base, initialvalue=""))
                vBase = float(simpledialog.askstring(
                    "Volume of Base","Please enter the volume of " + base, initialvalue=""))
            else:
                cAcid = float(simpledialog.askstring(
                    "Concentration of Acid",warning + " Please enter the concentration of " + acid, initialvalue=""))
                cBase = float(simpledialog.askstring(
                    "Concentration of Base","Please enter the concentration of " + base, initialvalue=""))
                vAcid = float(simpledialog.askstring(
                    "Volume of Acid","Please enter the volume of " + acid, initialvalue=""))

        if flagStrongAcid and flagStrongBase: # TODO
            return StrongAcidStrongBase.construct(self)
        elif flagStrongAcid and not flagStrongBase:
            # t == "Acid"
            return WeakBaseStrongAcid.construct(self, pkb, vBase, cBase, cAcid, True)
        elif not flagStrongAcid and flagStrongBase:
            # t == "Base"
            return WeakAcidStrongBase.construct(self, pka, vAcid, cAcid, cBase, True)