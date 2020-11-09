from mmm_simulator import generate_statistics, get_ccdf_continuous, get_together, get_everything_together
from mmm_simulator import policy_dict
import numpy as np
from math import log, e, sqrt
import matplotlib.pyplot as plt
from generator import m
from xlwt import Workbook


class Analyzer:

    # default
    N = 50000
    K = 10
    base = 10
    seed = 2019
    policy = 'jsq'
    a = 10
    which_method = 1
    rate_out = [1] * 10
    mode_dict = { 'combine_all_queues':get_everything_together, 'separate_all_queues':get_together }
    mode = 'combine_all_queues'

    # modify this list to apply different rate_in:
    rate_in_list = [7, 8, 9, 9.5]

    def initialize_statistics(self):
        self.STA = []
        self.CCDF = []
        for rate_in in self.rate_in_list:
            sta = generate_statistics(N = self.N, K = self.K, seed = self.seed, rate_in = rate_in, rate_out = self.rate_out, policy = self.policy, a = self.a, which_method = self.which_method)
            ccdf = get_ccdf_continuous(self.mode_dict[self.mode](sta))
            self.STA.append(sta)
            self.CCDF.append(ccdf)

    def semilogplot_samples(self):
        self.LOG = [[] for _ in range(0, len(self.rate_in_list))]
        self.HORIZON = [[] for _ in range(0, len(self.rate_in_list))]
        self.RAW = [[] for _ in range(0, len(self.rate_in_list))]
        self.m = len(self.CCDF[0]) - 1
        for _ in range(0, len(self.rate_in_list)):
            ccdf = self.CCDF[_]
            for q in range(1, len(ccdf)):
                self.HORIZON[_].append(np.linspace(0, ccdf[0][q][1], ccdf[0][q][0] + 1).tolist())
                self.LOG[_].append([log(_, self.base) for _ in ccdf[q]])
                self.RAW[_].append(ccdf[q])
            # LOG and HORIZON each in format of list[which_rate_in][which_queue]=list_of_samples

    def leastsquare(self, x, y):
        sxy = sx = sy = sxx = syy = 0
        n = len(x)
        for _ in range(0, n):
            sxy += x[_] * y[_]
            sx += x[_]
            sy += y[_]
            sxx += x[_] ** 2
            syy += y[_] ** 2
        a = (sxy - sx * sy / n) / (sxx - sx ** 2 / n)
        b = (sy - a * sx) / n
        r = abs((n * sxy - sx * sy) / sqrt((n * sxx - sx ** 2) * (n * syy - sy ** 2)))
        return (a, b, r)

    def plot_all(self):
        self.mode = 'combine_all_queues'
        self.policy = 'jsq'
        self.initialize_statistics()
        self.semilogplot_samples()
        jsq_h = self.HORIZON.copy()
        jsq_l = self.LOG.copy()
        self.policy = 'ptc'
        self.initialize_statistics()
        self.semilogplot_samples()
        ptc_h = self.HORIZON.copy()
        ptc_l = self.LOG.copy()
        for _ in range(0, len(self.rate_in_list)):
            fig, ax = plt.subplots()
            fig.suptitle("rate_in:%.2f" % self.rate_in_list[_])
            ax.set_xlabel('Waiting Time')
            ax.set_ylabel('Log CCDF')
            ax.plot(jsq_h[_][0], jsq_l[_][0], label = 'Join the Shortest Queue - rate_in:%.2f' % self.rate_in_list[_])
            ax.plot(ptc_h[_][0], ptc_l[_][0], label = 'Power of Two Choices - rate_in:%.2f' % self.rate_in_list[_])
            t = self.leastsquare(jsq_h[_][0], jsq_l[_][0])
            print("Policy: Join the Shortest Queue - rate_in:%.2f - linear fit: y = %f x + %f, r = %f" % (self.rate_in_list[_], t[0], t[1], t[2]))
            t = self.leastsquare(ptc_h[_][0], ptc_l[_][0])
            print("Policy: Power of Two Choices - rate_in:%.2f - linear fit: y = %f x + %f, r = %f" % (self.rate_in_list[_], t[0], t[1], t[2]))
            ax.legend()

    def plot(self):
        self.mode = 'combine_all_queues'
        fig, ax = plt.subplots()
        ax.set_xlabel('Waiting Time')
        ax.set_ylabel('Log CCDF')
        self.plot_semisamples(ax)
        self.plot_th(ax)
        ax.legend()

    def plot_semisamples(self, ax):
        self.policy = 'jsq'
        self.initialize_statistics()
        self.semilogplot_samples()
        for _ in range(0, len(self.rate_in_list)):
            ax.plot(self.HORIZON[_][0], self.LOG[_][0], label = 'Join the Shortest Queue - rate_in:%.2f' % self.rate_in_list[_])
            t = self.leastsquare(self.HORIZON[_][0], self.LOG[_][0])
            print("Policy: Join the Shortest Queue - rate_in:%.2f - linear fit: y = %f x + %f, r = %f" % (self.rate_in_list[_], t[0], t[1], t[2]))
        self.policy = 'ptc'
        self.initialize_statistics()
        self.semilogplot_samples()
        for _ in range(0, len(self.rate_in_list)):
            ax.plot(self.HORIZON[_][0], self.LOG[_][0], label = 'Power of Two Choices - rate_in:%.2f' % self.rate_in_list[_])
            t = self.leastsquare(self.HORIZON[_][0], self.LOG[_][0])
            print("Policy: Power of Two Choices - rate_in:%.2f - linear fit: y = %f x + %f, r = %f" % (self.rate_in_list[_], t[0], t[1], t[2]))
        
    def plot_th(self, ax):
        rate_out = 0
        for _ in range(0, len(self.rate_out)):
            rate_out += self.rate_out[_]
        for _ in range(0, len(self.rate_in_list)):
            x = self.HORIZON[_][0]
            y = []
            for item in x:
                y.append(item * log(self.rate_in_list[_] / rate_out, self.base))
            ax.plot(x, y, '--', label = 'Theoretical of Uniformly-Random - rate_in:%.2f' % self.rate_in_list[_], color = "red")


def show_params(analyzer):
    print("These are current params:")
    #print("N = %d     K = %d     policy = %s     base = %f     seed = %d     method = %d     a = %f\n" % (analyzer.N, analyzer.K, analyzer.policy, analyzer.base, analyzer.seed, analyzer.which_method, analyzer.a))
    print("N = %d     K = %d     policy = %s     base = %f     seed = %d     method = %d\n" % (analyzer.N, analyzer.K, analyzer.policy, analyzer.base, analyzer.seed, analyzer.which_method))

def reset_params(analyzer):
    switcher_reset = Switcher_reset()
    while True:
        print("Select which to reset:")
        print("1 - N")
        print("2 - K")
        print("3 - policy")
        print("4 - base")
        print("5 - seed")
        print("6 - which_method")
        """
        print("7 - a")
        """
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
    def case_4(self, analyzer): # show comparison results
        show_all(analyzer)
        return True
    def case_5(self, analyzer): # save all
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
    def case_3(self, analyzer): # reset policy
        s = "reset policy: (current policy = %s)\nValid choices:" % analyzer.policy
        for _ in policy_dict.keys():
            s += (_ + '  ')
        policy = input(s + '\n')
        if policy in policy_dict:
            analyzer.policy = policy
        else:
            print("Be serious.\n")
        return True
    def case_4(self, analyzer): # reset base
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
    def case_5(self, analyzer): # reset seed
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
    def case_6(self, analyzer): # reset which_method
        which_method = input("reset which_method: (current which_method = %d)" % analyzer.which_method)
        if which_method in ('1', '2'):
            analyzer.which_method = int(which_method)
        else:
            print("Be serious.\n")
        return True
    """
    def case_7(self, analyzer): # reset a
        a = input("reset a: (current a = %f)" % analyzer.a)
        try:
            a = float(a)
            analyzer.a = a
        except ValueError:
            print("Be serious.\n")
        return True
    """

def show(analyzer):
    analyzer.plot()
    plt.show()

def show_all(analyzer):
    analyzer.plot_all()
    plt.show()

def save(analyzer):
    try:
        m = len(analyzer.rate_out)
        K = len(analyzer.STA[0])
        workbook = Workbook()
        for _ in range(0, len(analyzer.rate_in_list)):
            sheet = workbook.add_sheet("rate_in = %.2f" % analyzer.rate_in_list[_])
            for q in range(0, m):
                for k in range(0, K):
                    l = analyzer.STA[_][k][q]
                    sheet.write(0, q * K + k, "Line: %d" % (q + 1))
                    sheet.write(1, q * K + k, "K = %d" % (k + 1))
                    for item in range(0, len(l)):
                        sheet.write(item + 2, q * K + k, l[item])
        workbook.save("MMm_w_N=%d_K=%d_policy=%s_base=%f_seed=%d_method=%d" % (analyzer.N, analyzer.K, analyzer.policy, analyzer.base, analyzer.seed, analyzer.which_method) + ".xls")
        print("Successfully saved.\n")
    except AttributeError:
        print("No statistics. \n")





if __name__ == '__main__':
    analyzer = Analyzer()
    switcher = Switcher()
    while True:
        print("Choose where to go:")
        print("1 - Show parameters.")
        print("2 - Reset parameters.")
        print("3 - Show results.")
        print("4 - Show comparison.")
        print("5 - Save all.")
        print("0 - Exit")
        if not switcher.case(analyzer, input()):
            print("Exit?")
            print("0 - No      1 - Confirm")
            if input() == "1":
                break
