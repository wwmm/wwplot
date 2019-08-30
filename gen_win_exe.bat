pyinstaller wwplot.in ^
--onefile ^
--hidden-import=numpy.random.common ^
--hidden-import=numpy.random.bounded_integers ^
--hidden-import=numpy.random.common ^
--hidden-import=numpy.random.entropy ^
--hidden-import=PySide2.QtXml ^
--add-data="WWplot/ui;WWplot/ui"