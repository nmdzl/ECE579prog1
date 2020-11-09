import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import generator as gen
import numpy as np
import mm1

rate_in = 7
rate_out = [1] * 10
seed = 2019
intervals = 200
policy_dict = { 'jsq':gen.jsq_which_join, 'ptc':gen.ptc_which_join, 'ur':gen.ur_which_join }
policy = 'jsq'
a = 10


#-----------------------------------------------------------#
# Simulate MMm using both methods and applying all policies.#
#-----------------------------------------------------------#

def simulate_mmm(N, seed = seed, rate_in = rate_in, rate_out = rate_out, policy = policy, a = a, which_method = 1, bool = False):
                # The bool here means do you want to see plots or just convey values.
                # To just convey values, let it be False or just leave as default.
                # Or if you do need it to plot, insert bool as True.
    gen.seed = seed
    gen.random.seed(seed)
    #gen.jsq_a = a
    m = len(rate_out)
    func = [mm1.sojourn_and_transit, mm1.each_step]
    method = which_method - 1
    state = 0
    number = 0
    current_states = [0] * m
    timeline = 0
    TIMES = [[0] for _ in range(0, m)]
    STATES = [[0] for _ in range(0, m)]
    while number < N:
        effective_rate_out = 0
        for _ in range(0, m):
            if current_states[_]:
                effective_rate_out += rate_out[_]
        interval, transit = func[method](state, rate_in, effective_rate_out)
        timeline += interval
        state += transit
        if transit == -1:
            death = gen.generate_which_death(rate_out, current_states)
            current_states[death] -= 1
            TIMES[death].append(timeline)
            STATES[death].append(current_states[death])
        else:
            join = policy_dict[policy](current_states)
            current_states[join] += 1
            TIMES[join].append(timeline)
            STATES[join].append(current_states[join])
            number += 1
    if bool:
        ax = plt.axes(projection = '3d')
        ax.set_xlabel('Time')
        ax.set_ylabel('State')
        ax.set_zlabel('Line')
        for _ in range(0, m):
            ax.plot3D(TIMES[_], STATES[_], [_ + 1] * len(TIMES[_]))
        ax.set_title("N = %d  seed = %d  rate_in = %.2f  policy = %s" % (N, seed, rate_in, policy))
        plt.show()
    else:
        return (TIMES, STATES) # each in format of list[which_queue]=list_of_statistics

#*****Decomment the following lines to plot MMm using the first method.*****#
#simulate_mmm(500, rate_in = 13, policy = 'jsq', which_method = 1, bool = True)
#simulate_mmm(500, rate_in = 7, policy = 'ptc', which_method = 1, bool = True)
#simulate_mmm(500, rate_in = 7, policy = 'ur', which_method = 1, bool = True)
#simulate_mmm(500, rate_in = 8, policy = 'jsq', which_method = 1, bool = True)
#simulate_mmm(500, rate_in = 8, policy = 'ptc', which_method = 1, bool = True)
#simulate_mmm(500, rate_in = 8, policy = 'ur', which_method = 1, bool = True)
#simulate_mmm(500, rate_in = 9, policy = 'jsq', which_method = 1, bool = True)
#simulate_mmm(500, rate_in = 9, policy = 'ptc', which_method = 1, bool = True)
#simulate_mmm(500, rate_in = 9, policy = 'ur', which_method = 1, bool = True)
#simulate_mmm(500, rate_in = 9.5, policy = 'jsq', which_method = 1, bool = True)
#simulate_mmm(500, rate_in = 9.5, policy = 'ptc', which_method = 1, bool = True)
#simulate_mmm(500, rate_in = 9.5, policy = 'ur', which_method = 1, bool = True)

#*****Decomment the following lines to plot MMm using the second method.*****#
#simulate_mmm(500, rate_in = 7, policy = 'jsq', which_method = 2, bool = True)
#simulate_mmm(500, rate_in = 7, policy = 'ptc', which_method = 2, bool = True)
#simulate_mmm(500, rate_in = 7, policy = 'ur', which_method = 2, bool = True)
#simulate_mmm(500, rate_in = 8, policy = 'jsq', which_method = 2, bool = True)
#simulate_mmm(500, rate_in = 8, policy = 'ptc', which_method = 2, bool = True)
#simulate_mmm(500, rate_in = 8, policy = 'ur', which_method = 2, bool = True)
#simulate_mmm(500, rate_in = 9, policy = 'jsq', which_method = 2, bool = True)
#simulate_mmm(500, rate_in = 9, policy = 'ptc', which_method = 2, bool = True)
#simulate_mmm(500, rate_in = 9, policy = 'ur', which_method = 2, bool = True)
#simulate_mmm(500, rate_in = 9.5, policy = 'jsq', which_method = 2, bool = True)
#simulate_mmm(500, rate_in = 9.5, policy = 'ptc', which_method = 2, bool = True)
#simulate_mmm(500, rate_in = 9.5, policy = 'ur', which_method = 2, bool = True)



#--------------------------------------------------------------#
# Simulate MMm for K times and return all concerned statistics.#
#--------------------------------------------------------------#

def generate_statistics(N = 50000, K = 10, seed = seed, rate_in = rate_in, rate_out = rate_out, policy = policy, a = a, which_method = 1):
    m = len(rate_out)
    times = []
    states = []
    for _ in range(0, K):
        x, y = simulate_mmm(N, (int)(seed * (97 ** _)) % gen.m, rate_in, rate_out, policy, a, which_method) # Note that the seed policy here can be improved some way.
        times.append(x)
        states.append(y)
    w = [[] for _ in range(0, K)]
    for k in range(0, K):
        for q in range(0, m):
            server_customer = 0
            w_kq = []
            for _ in range(1, len(times[k][q])):
                if states[k][q][_] > states[k][q][_ - 1]:
                    w_kq.append(times[k][q][_])
                else:
                    w_kq[server_customer] = times[k][q][_] - w_kq[server_customer]
                    server_customer += 1
            while server_customer < len(w_kq):
                w_kq.pop()
            w[k].append(w_kq)
    return w # in format of list[which_round][which_queue]=list_of_samples


def get_together(Origin):
    m = len(Origin[0])
    Together = [[] for _ in range(0, m)]
    for ListList in Origin:
        for _ in range(0, m):
            Together[_] += ListList[_]
    return Together

def get_everything_together(Origin):
    m = len(Origin[0])
    Together = []
    for ListList in Origin:
        for _ in range(0, m):
            Together += ListList[_]
    return Together


def get_ccdf_continuous(C):
    C = C.copy()
    try:
        m = len(C)
        ccdf_C = [[m]]
        for _ in range(0, m):
            l = len(C[_])
            C[_].sort()
            dict_P = { C[_][0]:1 }
            for i in range(1, l):
                if C[_][i] > C[_][i - 1]:
                    dict_P[C[_][i]] = (l - i) / l
            ccdf_C.append([dict_P[num] if num in dict_P else dict_P[min(filter(lambda k: k > num, dict_P.keys()))] for num in np.linspace(0, C[_][-1], intervals + 1)])
            ccdf_C[0].append((intervals, C[_][-1]))
        return ccdf_C # in format of list[which_queue]=list_of_ccdf
    except:
        C.sort()
        l = len(C)
        dict_P = { C[0]:1 }
        for _ in range(1, l):
            if C[_] > C[_ - 1]:
                dict_P[C[_]] = (l - _) / l
        return ([[1, (intervals, C[-1])], [dict_P[num] if num in dict_P else dict_P[min(filter(lambda k: k > num, dict_P.keys()))] for num in np.linspace(0, C[-1], intervals + 1)]])



#--------------------------------#
# A sample for plotting all ccdf.#
#--------------------------------#

def sample_plot_separate(N = 100000, K = 10, seed = seed, rate_in = rate_in, rate_out = rate_out, policy = policy, a = a, which_method =1):
    ccdf = get_ccdf_continuous(get_together(generate_statistics(N, K, seed, rate_in, rate_out, policy, a, which_method)))
    for _ in range(1, len(ccdf)):
        fig, ax = plt.subplots()
        fig.suptitle("Line: %d" % _)
        ax.set_xlabel('Waiting time')
        ax.set_ylabel('CCDF')
        x = np.linspace(0, ccdf[0][_][1], ccdf[0][_][0] + 1).tolist()
        ax.plot(x, ccdf[_])
    plt.show()

def sample_plot_collected(N = 100000, K = 10, seed = seed, rate_in = rate_in, rate_out = rate_out, policy = policy, a = a, which_method =1):
    ccdf = get_ccdf_continuous(get_together(generate_statistics(N, K, seed, rate_in, rate_out, policy, a, which_method)))
    m = len(ccdf)
    fig, ax = plt.subplots()
    fig.suptitle("All Lines")
    ax.set_xlabel('Waiting time')
    ax.set_ylabel('CCDF')
    for _ in range(1, len(ccdf)):
        x = np.linspace(0, ccdf[0][_][1], ccdf[0][_][0] + 1).tolist()
        ax.plot(x, ccdf[_], label = 'Line %d' % _)
    ax.legend()
    plt.show()

#*****Decomment the following line to obtain specific results as mentioned in the report.*****#
#sample_plot_separate()
#sample_plot_collected()
