from math import log, exp
import random

seed = 1
m = 2147483647
a = 16807

def schrage():
    global seed, m, a
    rand = -(m % a) * (seed // (m // a)) + a * (seed % (m // a))
    seed = (rand if rand > 0 else rand + m)
    return seed / m
    

def generate_poisson(rate):
    # This part is using the Schrage algorithm.
    '''
    rand = schrage()
    '''
    # This part is using the random package.
    
    rand = random.random()
    
    return -1 / rate * log(1 - rand)
    

def generate_decide(rate_in, rate_out):
    # This part is using the Schrage algorithm.
    '''
    return (1 if schrage() * (rate_in + rate_out) < rate_in else -1)
    '''
    # This part is using the random package.
    
    return (1 if random.random() * (rate_in + rate_out) < rate_in else -1)
    

def generate_which_death(rate_out, current_states):
    col_list = [rate_out[0] * bool(current_states[0])]
    for _ in range(1, len(rate_out)):
        col_list.append(col_list[-1] + rate_out[_] * bool(current_states[_]))

    # This part is using the Schrage algorithm.
    '''
    col = schrage() * col_list[-1]
    '''
    # This part is using the random package.
    
    col = random.random() * col_list[-1]
    

    for _ in range(0, len(col_list)):
        if col <= col_list[_]:
            return _

#------------------------------------------#
# JSQ stands for "Join the Shortest Queue".#
#------------------------------------------#

"""
jsq_a = 100

def jsq_which_join(current_states):
    col_list = [exp(-jsq_a * current_states[0])]
    for _ in range(1, len(current_states)):
        col_list.append(col_list[-1] + exp(-jsq_a * current_states[_]))
    if current_states[1] > 370:
        print(col_list)

    # This part is using the Schrage algorithm.
    '''
    col = schrage() * col_list[-1]
    '''
    # This part is using the random package.
    
    col = random.random() * col_list[-1]
    

    for _ in range(0, len(col_list)):
        if col <= col_list[_]:
            return _
"""

def jsq_which_join(current_states):
    temp = min(current_states)
    temp_list = []
    for _ in range(0, len(current_states)):
        if current_states[_] == temp:
            temp_list.append(_)

    # This part is using the Schrage algorithm.
    '''
    rand = schrage()
    '''
    # This part is using the random package.
    
    rand = random.random()
    

    return temp_list[int(rand * len(temp_list))]

#---------------------------------------#
# PTC stands for "Power of Two Choices".#
#---------------------------------------#

def ptc_which_join(current_states):
    m = len(current_states)

    # This part is using the Schrage algorithm.
    '''
    i_1 = int(schrage() * m)
    i_2 = int(schrage() * (m - 1))
    if i_2 >= i_1:
        i_2 += 1
    rand = schrage() # generate another RV in case of the current states of the two chosen lines are equal
    '''
    # This part is using the random package.
    
    i_1 = int(random.random() * m)
    i_2 = int(random.random() * (m - 1))
    if i_2 >= i_1:
        i_2 += 1
    rand = random.random() # generate another RV in case of the current states of the two chosen lines are equal
    

    return (i_1 if current_states[i_1] < current_states[i_2] else i_2 if current_states[i_1] > current_states[i_2] else i_1 if rand < 0.5 else i_2)

#--------------------------------#
# UR stands for "Uniform-Random".#
#--------------------------------#

def ur_which_join(current_states):
    m = len(current_states)

    # This part is using the Schrage algorithm.
    '''
    return int(schrage() * m)
    '''
    # This part is using the random package.
    
    return int(random.random() * m)
    
