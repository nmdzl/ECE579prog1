import generator as gen


# This is the first method of simulating mm1.

def sojourn_and_transit(k, rate_in, rate_out):
    if k:
        sojourn_time = gen.generate_poisson(rate_in + rate_out)
        return (sojourn_time, gen.generate_decide(rate_in, rate_out))
    else:
        sojourn_time = gen.generate_poisson(rate_in)
        return (sojourn_time, 1)


# This is the second method of simulating mm1.

def each_step(k, rate_in, rate_out):
    if k:
        clock_in = gen.generate_poisson(rate_in)
        clock_out = gen.generate_poisson(rate_out)
        return ((clock_in, 1) if clock_in < clock_out else (clock_out, -1))
    else:
        clock_in = gen.generate_poisson(rate_in)
        return (clock_in, 1)
