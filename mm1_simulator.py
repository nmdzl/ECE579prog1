import matplotlib.pyplot as plt
import generator as gen
import numpy as np
import mm1

rate_in = 0.7
rate_out = 1
seed = 2019
intervals = 200


#-----------------------------------------------#
# This block is to simulate poisson distribution#
#-----------------------------------------------#

def plot_poisson(rate):
    x = np.linspace(0, 2 / rate, 101)[:-1]
    delta = 2 / rate / 100
    y = [0] * 100
    points = [gen.generate_poisson(rate) for _ in range(0,1000000)]
    for point in points:
        if point <= 2 / rate:
            y[int(point / delta)] += 1
    plt.scatter(x, y)
    plt.ylim(bottom = 0)
    plt.show()

#*****Decomment the following line to operate this simulation first.*****#
#plot_poisson(1)



#---------------------------------#
# Simulate MM1 using both methods.#
#---------------------------------#

def simulate_mm1(N, seed = seed, rate_in = rate_in, rate_out = rate_out, which_method = 1, bool = False):
                # The bool here means do you want to see plots or just convey values.
                # To just convey values, let it be False or just leave as default.
                # Or if you do need it to plot, insert bool as True.
    gen.seed = seed
    gen.random.seed(seed)
    func = [mm1.sojourn_and_transit, mm1.each_step]
    method = which_method - 1
    number = 0
    state = 0
    TIME = [0]
    STATE = [0]
    while number < N:
        interval, transit = func[method](state, rate_in, rate_out)
        state += transit
        if transit == -1:
            number += 1
        TIME.append(TIME[-1] + interval)
        STATE.append(state)
    if bool:
        ax = plt.axes()
        ax.set_xlabel('Time')
        ax.set_ylabel('State')
        ax.scatter(TIME, STATE)
        ax.set_title("N = %d  seed = %d  rate_in = %.2f" % (N, seed, rate_in))
        plt.show()
    else:
        return (TIME, STATE)

#*****Decomment the following lines to plot MM1 using the first method.*****#
#simulate_mm1(100000, seed, 0.7, which_method = 1, bool = True)
#simulate_mm1(100000, seed, 0.95, which_method = 1, bool = True)
#simulate_mm1(100000, seed, 1, which_method = 1, bool = True)
#simulate_mm1(100000, seed, 1.1, which_method = 1, bool = True)

#*****Decomment the following lines to plot MM1 using the second method.*****#
#simulate_mm1(100000, seed, 0.7, which_method = 2, bool = True)
#simulate_mm1(100000, seed, 0.95, which_method = 2, bool = True)
#simulate_mm1(100000, seed, 1, which_method = 2, bool = True)
#simulate_mm1(100000, seed, 1.1, which_method = 2, bool = True)



#--------------------------------------------------------------#
# Simulate MM1 for K times and return all concerned statistics.#
#--------------------------------------------------------------#

def generate_statistics(N = 10000, K = 10, seed = seed, rate_in = rate_in, rate_out = rate_out, which_method = 1):
    time = []
    state = []
    for _ in range(0, K):
        x, y = simulate_mm1(N, (int)(seed * (97 ** _)) % gen.m, rate_in, rate_out, which_method) # Note that the seed policy here can be improved some way.
        time.append(x)
        state.append(y)
    t = []
    w = []
    X = []
    D = []
    B = []
    I = []
    for k in range(0, K):
        server_customer = 0
        busy_start_index = 0
        t_k = []
        w_k = []
        X_k = []
        D_k = []
        B_k = []
        I_k = []
        for _ in range(1, len(time[k])):
            if state[k][_] > state[k][_ - 1]:
                t_k.append(time[k][_])
                w_k.append(time[k][_])
                X_k.append(state[k][_] - 1)
            else:
                w_k[server_customer] = time[k][_] - w_k[server_customer]
                D_k.append(state[k][_])
                server_customer += 1
            if state[k][_ - 1] == 0:
                busy_start_index = _
                I_k.append(time[k][_] - time[k][_ - 1])
            if state[k][_] == 0 or _ == len(time[k]) - 1:
                B_k.append(time[k][_] - time[k][busy_start_index])
        while server_customer < len(w_k):
            w_k.pop()
        t.append(t_k)
        w.append(w_k)
        X.append(X_k)
        D.append(D_k)
        B.append(B_k)
        I.append(I_k)
    return (t, w, X, D, B, I) # each in format of list[which_round]=list_of_samples


def get_together(Origin):
    Together = []
    for List in Origin:
        Together += List
    return Together


def get_ccdf_discrete(D):
    D = D.copy()
    D.sort()
    l = len(D)
    dict_P = { D[0]:1 }
    for i in range(1, l):
        if D[i] > D[i - 1]:
            dict_P[D[i]] = (l - i) / l
    return [dict_P[num] if num in dict_P else dict_P[min(filter(lambda k: k > num, dict_P.keys()))] for num in range(0, D[-1] + 1)]


def get_ccdf_continuous(C):
    C = C.copy()
    C.sort()
    l = len(C)
    dict_P = { C[0]:1 }
    for _ in range(1, l):
        if C[_] > C[_ - 1]:
            dict_P[C[_]] = (l - _) / l
    return ([dict_P[num] if num in dict_P else dict_P[min(filter(lambda k: k > num, dict_P.keys()))] for num in np.linspace(0, C[-1], intervals + 1)], intervals, C[-1])



#--------------------------------#
# A sample for plotting all ccdf.#
#--------------------------------#

def plot_X_and_D(X, D, rate_in):
    # Plot the ccdf of X
    ccdf_X = get_ccdf_discrete(get_together(X))
    x_X = range(0, len(ccdf_X))
    # Plot the ccdf of D
    ccdf_D = get_ccdf_discrete(get_together(D))
    x_D = range(0, len(ccdf_D))
    # Plot the ccdf of steady state
    l = max(len(ccdf_X), len(ccdf_D))
    x_l = range(0, l)
    ccdf_steady_state = []
    for i in range(0, l):
        ccdf_steady_state.append((rate_in / rate_out) ** i)

    plt.plot(x_X, ccdf_X)
    plt.plot(x_D, ccdf_D)
    plt.plot(x_l, ccdf_steady_state)
    plt.title('Q1: rate_in = ' + str(rate_in))
    plt.show()


def plot_B(B, rate_in):
    # Plot the ccdf of B
    ccdf_B, intervals, maxi = get_ccdf_continuous(get_together(B))
    x_B = np.linspace(0, maxi, intervals + 1)

    plt.plot(x_B, ccdf_B)
    plt.title('Q2: rate_in = ' + str(rate_in))
    plt.show()


def sample_plot(N = 10000, K = 10, seed = seed):
    t_1, w_1, X_1, D_1, B_1, I_1 = generate_statistics(N, K, seed, rate_in = 0.7)
    t_2, w_2, X_2, D_2, B_2, I_2 = generate_statistics(N, K, seed, rate_in = 0.8)
    t_3, w_3, X_3, D_3, B_3, I_3 = generate_statistics(N, K, seed, rate_in = 0.9)
    t_4, w_4, X_4, D_4, B_4, I_4 = generate_statistics(N, K, seed, rate_in = 0.95)
    plot_X_and_D(X_1, D_1, 0.7)
    plot_X_and_D(X_2, D_2, 0.8)
    plot_X_and_D(X_3, D_3, 0.9)
    plot_X_and_D(X_4, D_4, 0.95)
    plot_B(B_1, 0.7)
    plot_B(B_2, 0.8)
    plot_B(B_3, 0.9)
    plot_B(B_4, 0.95)

#*****Decomment the following line to obtain specific results as mentioned in the report.*****#
#sample_plot()
