from mm1_simulator import generate_statistics, get_ccdf_discrete, get_ccdf_continuous, get_together
import numpy as np
from math import log, e
import matplotlib.pyplot as plt
from generator import m
from xlwt import Workbook

class Analyzer:
    STA_dict = { 0:"t", 1:"w", 2:"X", 3:"D", 4:"B", 5:"I" }

    # default
    N = 10000
    K = 10
    base = 10
    seed = 2019
    which_method = 1
    rate_out = 1

    # modify this list to apply different rate_in
    rate_in_list = [0.7, 0.8, 0.9, 0.95]

    def initialize_statistics(self):
        self.STA = []
        for rate_in in self.rate_in_list:
            t, w, X, D, B, I = generate_statistics(N = self.N, K = self.K, seed = self.seed, rate_in = rate_in, rate_out = self.rate_out, which_method = self.which_method)
            self.STA.append((t, w, X, D, B, I)) #tuple of (t, w, X, D, B, I)
        self.initialize_statistics_XD()
        self.initialize_statistics_XD_th()
        self.initialize_statistics_B()

    def initialize_statistics_XD(self):
        self.CCDF_XD = []
        self.HORIZON_XD = []
        for _ in range(0, len(self.rate_in_list)):
            ccdf_X = get_ccdf_discrete(get_together(self.STA[_][2]))
            ccdf_D = get_ccdf_discrete(get_together(self.STA[_][3]))
            self.CCDF_XD.append((ccdf_X, ccdf_D)) #tuple of (ccdf_X, ccdf_D)
            self.HORIZON_XD.append((range(0, len(ccdf_X)), range(0, len(ccdf_D)))) #tuple of (x_X, x_D)

    def initialize_statistics_XD_th(self):
        self.CCDF_XD_th = []
        for _ in range(0, len(self.rate_in_list)):
            self.CCDF_XD_th.append(([self.rate_in_list[_] ** i for i in self.HORIZON_XD[_][0]], [self.rate_in_list[_] ** i for i in self.HORIZON_XD[_][1]]))            

    def initialize_statistics_B(self):
        self.CCDF_B =[]
        self.HORIZON_B = []
        for _ in range(0, len(self.rate_in_list)):
            ccdf_B, intervals, maxi = get_ccdf_continuous(get_together(self.STA[_][4]))
            self.CCDF_B.append(ccdf_B)
            self.HORIZON_B.append(np.linspace(0, maxi, intervals + 1).tolist())

    def semilogplot_convert_XD(self):
        self.LOG_XD = []
        for (ccdf_X, ccdf_D) in self.CCDF_XD:
            self.LOG_XD.append(([log(_, self.base) for _ in ccdf_X], [log(_, self.base) for _ in ccdf_D])) #tuple of (log_X, log_D)

    def semilogplot_convert_XD_th(self):
        self.LOG_XD_th = []
        for (ccdf_X_th, ccdf_D_th) in self.CCDF_XD_th:
            self.LOG_XD_th.append(([log(_, self.base) for _ in ccdf_X_th], [log(_, self.base) for _ in ccdf_D_th]))

    def semilogplot_convert_B(self):
        self.LOG_B = []
        for ccdf_B in self.CCDF_B:
            self.LOG_B.append([log(_, self.base) for _ in ccdf_B])

    def semilogplot_X(self, ax):
        for _ in range(0, len(self.rate_in_list)):
            ax.plot(self.HORIZON_XD[_][0], self.LOG_XD[_][0], label = 'X - rate_in:%.2f' % self.rate_in_list[_])
    def semilogplot_D(self, ax):
        for _ in range(0, len(self.rate_in_list)):
            ax.plot(self.HORIZON_XD[_][1], self.LOG_XD[_][1], label = 'D - rate_in:%.2f' % self.rate_in_list[_])
    def semilogplot_XD_th(self, ax):
        for _ in range(0, len(self.rate_in_list)):
            ax.plot(self.HORIZON_XD[_][0], self.LOG_XD_th[_][0], '--', color = "red")
            ax.plot(self.HORIZON_XD[_][1], self.LOG_XD_th[_][1], '--', color = "red")
    def semilogplot_B(self, ax):
        for _ in range(0, len(self.rate_in_list)):
            ax.plot(self.HORIZON_B[_], self.LOG_B[_], label = 'rate_in:%.2f' % self.rate_in_list[_])

    def ccdfplot_X(self, ax):
        for _ in range(0, len(self.rate_in_list)):
            ax.plot(self.HORIZON_XD[_][0], self.CCDF_XD[_][0], label = 'X - rate_in:%.2f' % self.rate_in_list[_])
    def ccdfplot_D(self, ax):
        for _ in range(0, len(self.rate_in_list)):
            ax.plot(self.HORIZON_XD[_][1], self.CCDF_XD[_][1], label = 'D - rate_in:%.2f' % self.rate_in_list[_])
    def ccdfplot_B(self, ax):
        for _ in range(0, len(self.rate_in_list)):
            ax.plot(self.HORIZON_B[_], self.CCDF_B[_], label = 'B - rate_in:%.2f' % self.rate_in_list[_])

    def plot(self):
        # create two figures first
        self.fig1, self.ax1 = plt.subplots()
        self.fig2, self.ax2 = plt.subplots()
        self.fig1.suptitle('Q1')
        self.fig2.suptitle('Q2')
        self.ax1.set_xlabel('State')
        self.ax2.set_xlabel('Busy Period')
        # initialize statistics
        self.initialize_statistics()
        self.semilogplot_convert_XD()
        self.semilogplot_convert_B()
        self.semilogplot_convert_XD_th()
        # q1
        self.semilogplot_X(self.ax1)
        self.semilogplot_D(self.ax1)
        self.semilogplot_XD_th(self.ax1)
        # q2
        # Decomment the following line to see the plot of raw statistics of B
        #self.ccdfplot_B(self.ax2)
        self.semilogplot_B(self.ax2)
        # show legends
        self.ax1.legend()
        self.ax2.legend()




def show_params(analyzer):
    print("Current params:")
    print("N = %d     K = %d     base = %f     seed = %d     method = %d\n" % (analyzer.N, analyzer.K, analyzer.base, analyzer.seed, analyzer.which_method))

def reset_params(analyzer):
    switcher_reset = Switcher_reset()
    while True:
        print("Select which to reset:")
        print("1 - N")
        print("2 - K")
        print("3 - base")
        print("4 - seed")
        print("5 - which_method")
        print("0 - Finish reset.")
        if not switcher_reset.case(analyzer, input()):
            show_params(analyzer)
            break

class Switcher:
    def case(self, analyzer, s):
        method_name = 'case_' + s
        method = getattr(self, method_name, False)
        return (method(analyzer) if method else False)
    def case_1(self, analyzer): # show parameters
        show_params(analyzer)
        return True
    def case_2(self, analyzer): # reset parameters
        reset_params(analyzer)
        return True
    def case_3(self, analyzer): # show results
        show(analyzer)
        return True
    def case_4(self, analyzer): # save all
        save(analyzer)
        return True

class Switcher_reset:
    def case(self, analyzer, s):
        method_name = 'case_' + s
        method = getattr(self, method_name, False)
        return (method(analyzer) if method else False)
    def case_1(self, analyzer): # reset N
        N = input("reset N: (current N = %d)" % analyzer.N)
        try:
            N = int(N)
            if N > 0:
                analyzer.N = N
            else:
                print("Be serious.\n")
        except ValueError:
            print("Be serious.\n")
        return True
    def case_2(self, analyzer): # reset K
        K = input("reset K: (current K = %d)" % analyzer.K)
        try:
            K = int(K)
            if K > 0:
                analyzer.K = K
            else:
                print("Be serious.\n")
        except ValueError:
            print("Be serious.\n")
        return True
    def case_3(self, analyzer): # reset base
        base = input("reset base: (current base = %d)" % analyzer.base)
        if base == 'e':
            analyzer.base = e
        else:
            try:
                base = float(base)
                if base > 0:
                    analyzer.base = base
                else:
                    print("Be serious.\n")
            except ValueError:
                print("Be serious.\n")
        return True
    def case_4(self, analyzer): # reset seed
        seed = input("reset seed: (current seed = %d)" % analyzer.seed)
        try:
            seed = int(seed)
            if seed > 0 and seed < m:
                analyzer.seed = seed
            else:
                print("Be serious.\n")
        except ValueError:
            print("Be serious.\n")
        return True
    def case_5(self, analyzer): # reset which_method
        which_method = input("reset which_method: (current which_method = %d)" % analyzer.which_method)
        if which_method in ('1', '2'):
            analyzer.which_method = int(which_method)
        else:
            print("Be serious.\n")
        return True

def show(analyzer):
    analyzer.plot()
    plt.show()

def save(analyzer):
    for _ in range(0, len(analyzer.STA_dict)):
        if save_one(analyzer, _):
            print(analyzer.STA_dict[_] + " successfully saved.")
        else:
            print("Invalid statistics.")
            break

def save_one(analyzer, index):
    try:
        workbook = Workbook()
        for _ in range(0, len(analyzer.rate_in_list)):
            sheet = workbook.add_sheet("rate_in = %.2f" % analyzer.rate_in_list[_])
            one = analyzer.STA[_][index]
            k = 0
            for l in one:
                sheet.write(0, k, "K = %d" % (k + 1))
                for item in range(0, len(l)):
                    sheet.write(item + 1, k, l[item])
                k += 1
        
        workbook.save("MM1_" + analyzer.STA_dict[index] + "_N=%d_K=%d_base=%f_seed=%d_method=%d" % (analyzer.N, analyzer.K, analyzer.base, analyzer.seed, analyzer.which_method) + ".xls")
        return True
    except ValueError:
        return False





if __name__ == '__main__':
    analyzer = Analyzer()
    switcher = Switcher()
    while True:
        print("Choose where to go:")
        print("1 - Show parameters.")
        print("2 - Reset parameters.")
        print("3 - Show results.")
        print("4 - Save all.")
        print("0 - Exit")
        if not switcher.case(analyzer, input()):
            print("Exit?")
            print("0 - No      1 - Confirm")
            if input() == "1":
                break
