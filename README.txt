This simulation program was written by Benjamin Ding (zding8).

The program was typed in Python Language, containing six files in total, which are generator.py, mm1.py, mm1_simulator.py, mm1_analyzer.py, mmm_simulator.py, and mmm_analyzer.py.

To successfully run the files on your computer, please install the following necessary packages first: random, matplotlib, numpy, math, and xlwt.
You can simply type these lines in cmd, as an administrator:
`pip install matplotlib==3.1.1`
`pip install numpy==1.16.2`
`pip install xlwt`

If something goes wrong with the installation of xlwt package, you can simply comment everything related to that in both mm1_analyzer.py and mmm_analyzer.py files.

To run the program and obtain the results, you can either run mm1_analyzer.py and mmm_analyzer.py in IDE, or simply run the corresponding exe files.

The mm1_analyzer.py is for the first section (Warm Up), and the mmm_analyzer.py is for the second section (Plot Thickens).

The generator.py file contains methods to generate Exponential random variables, generate random variabes with other distributions, and others for use of joining which queueing line in mmm system.
It provided two approaches to generate a uniformly distributed random variable over [0, 1) in general, the standard random package and the Schrage algorithm. The difference is that the former one generates random variable exactly over [0, 1), while the latter one over (0, 1). In all the methods of generator.py, the value 0 is valid and needed, thus I chose the random package for each of them.

The mm1.py file contains two approaches to simulate the process of mm1. The first approach is that, generate the sojourn time in a state (that is, a random variable exponentially distributted with rate lambda plus miu), then choose whether it is a death or birth. The second approach is that, generate the two kinds of sojourn time from the very beginning (after which time, a death occurs or a birth occurs), then apply the smaller one.

The mm1_simulator.py file contains all the methods needed when doing all the computation, and the task of mm1_analyzer.py file is to create a user input interface in order to compute by a user's input order. The same is of mmm_simulator.py and mmm_analyzer.py.
You can make an order of either of the following ones: show current parameters, reset all parameters, compute and show results, save all statistics, and exit.