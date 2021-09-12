Manim Cairo-backend version
	2020-12-25
	C:\TDDownload\manim-master
	from manimlib.imports import *
	cmd 命令栏：
		低质量：
			python -m manim [__filename__] -pl 
		高质量：
			python -m manim [__filename__] -p
	Example:
	python -m manim My_Projects\Axes_and_Numberline.py -pl
	
	注意：can only create file under 'C:\TDDownload\manim-master\manimlib', and is usually under 'My_Projects' 
	b站大部分视频都是这个 油管的19年视频也是这个教程 统称旧版


ManimGL
	2021-9-5
	from manimlib import *
	C:\TDDownload\manim_master_2021.9.5\manin_master_9.5
	cmd 命令栏：
		交互画面：
			manimgl
		渲染视频：
			manimgl [__filename__] -o
	self.embed() 可以添加交互式界面

Manim community
	fram manim import *
	C:\Python38\Lib\site-packages\manim\__init__.py
	cmd 命令栏：
		python -m manim render -p manimlib\Projects\manim_physics_example.py 

注意：[manim_physics, manimlib, manim] 可以在任何地方被 import 
	前提是使用 interpreter C:\Python38\python.exe (Python 3.8.7 64-bit)
