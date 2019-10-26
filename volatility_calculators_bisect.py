# coding=utf-8
import numpy as np
import math
from scipy.stats import norm

#Define bls option pricing model
def d1(S, K, r, vol, T):
    return (math.log(S / K) + (r + (vol * vol) / 2) * T) / (vol * math.sqrt(T))


def d2(S, K, r, vol, T):
    return d1(S, K, r, vol, T) - (vol * math.sqrt(T))


def callpx(S, K, r, vol, T):
    return S * norm.cdf(d1(S, K, r, vol, T)) - K * math.exp(-r * T) * norm.cdf(d2(S, K, r, vol, T))


def putpx(S, K, r, vol, T):
    return K * math.exp(-r * T) * norm.cdf(-d2(S, K, r, vol, T)) - S * norm.cdf(-d1(S, K, r, vol, T))


def volatility_calculators_bisect(market_price, S, K, r, T, type):
    '''

    :param market_price: the observed market option price
    :param S:
    :param K:
    :param r:
    :param T:
    :param type:type = 1 means call option, type = 0 means put option
    :return:
    '''
    if market_price == None or S == None or r == None or T == None or type == None:
        print('parameter is null')
        return
    # initial paratmeter
    imp_vol = np.zeros((1, len(market_price)))
    itr = np.zeros((1, len(market_price)))
    c = np.zeros((1, len(market_price)))
    min_vol = -2 * np.ones((1, len(market_price)))
    max_vol = 2 * np.ones((1, len(market_price)))
    tol = 0.00001

    #Define a function of differnces between therotical and practical option price.
    def f_call(vol, i):
        return callpx(S[i],K[i],r[i],vol[i],T[i]) - market_price[i]

    def f_put(vol, i):
        return putpx(S[i],K[i],r[i],vol[i],T[i]) - market_price[i]
    #iteration
    for i in range(len(type)):
        #f_call function
        if type[i] == 1:
            while f_call(min_vol,i)*f_call(max_vol, i) < 0 and abs(max_vol[i]-min_vol[i]) >= tol:
                # The followings are how bisection method works.
                c[i] = 0.5 * (min_vol[i] + max_vol[i])
                itr[i] += 1
                if f_call(c, i) * f_call(max_vol, i) <= 0:
                    min_vol[i] = c[i]
                elif f_call(min_vol, i) * f_call(c, i) <= 0:
                    max_vol[i] = c[i]
            #Define the output
            imp_vol[i] = 0.5 * (min_vol[i] + max_vol[i])
        #f_put
        elif type[i] == 0:
            while f_put(min_vol, i) * f_put(max_vol, i) < 0 and abs(max_vol[i] - min_vol[i]) >= tol:
                # The followings are how bisection method works.
                c[i] = 0.5 * (min_vol[i] + max_vol[i])
                itr[i] += 1
                if f_put(c, i) * f_put(max_vol, i) <= 0:
                    min_vol[i] = c[i]
                else:
                    max_vol[i] = c[i]
            # Define the output
            imp_vol[i] = 0.5 * (min_vol[i] + max_vol[i])

    return imp_vol, itr
