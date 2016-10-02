# WWplot

A simple plotting tool for experimental physics classes. It is being developed at [Cefet-NI](http://www.cefet-rj.br/index.php/nova-iguacu).

![](images/linear_fit.png)
![](images/gaussian_distribution.png)
![](images/nonlinear_fit.png) 

Features:

- XY and histogram plot
- Linear and nonlinear fit
- Import and export table in TSV format (tab separated values) 

Required libraries:

- Python 3 with Numpy, Scipy, PyGobject 3, cairocffi, Matplotlib
- Gtk 3.18 or above

After installing the required libraries execute the main.py script in a
terminal:

	python main.py

I develop and test this software on Linux. I am not sure if it runs on Windows. But as only cross-platform libraries are being used it should be possible to make an windows executable.