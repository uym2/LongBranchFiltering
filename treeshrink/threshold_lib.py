from scipy.stats import gaussian_kde,lognorm
from math import log, exp
from statistics import mean,stdev

EPS = 1e-5

def find_threshold_loglnorm(data,quantiles):
    x = [log(log(y)) for y in data]
    mu = mean(x)
    sigma = stdev(x)
    return [exp(t) for t in lognorm.ppf(quantiles, sigma, scale=exp(mu))]

def find_threshold_lkernel(data,quantiles):
    x = sorted([log(y) for y in data])
    kernel = gaussian_kde(x,'silverman')
    
    # compute cdf
    cdf = [kernel.integrate_box_1d(-float("inf"),x[0])]
    for i in range(len(x)-1):
        cdf.append(cdf[-1]+kernel.integrate_box_1d(x[i],x[i+1]))
    cdf.append(cdf[-1]+kernel.integrate_box_1d(x[-1],float("inf")))

    thresholds = [0]*len(quantiles)
    for i,q in enumerate(quantiles):
        cutoff_idx = __find_cutoff_idx__(cdf,q)
        if cutoff_idx < 0:
            t = exp(x[0]) - EPS
        else:    
            t = exp(x[cutoff_idx]) + EPS
        thresholds[i] = t
    return thresholds         


def __find_cutoff_idx__(cdf,q):
    # normalize cdf
    s = cdf[-1]
    cdf = [y/s for y in cdf]
    
    # find the cutoff
    for i,c in enumerate(cdf):
        if c > q:
            return i-1
    # only get here if q == 1.0                        
    return i-1       
