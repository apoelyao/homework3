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

#Define the partial derivative of option price with respect to volatility.
def vega(S, K, r, vol, T, i):
    return S(i) * norm.pdf(d1(S(i), K(i), r(i), vol(i), T(i))) * math.sqrt(T(i))


def volatility_calculators_newton(market_price, S, K, r, T, type):
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
    guess_vol = 0.25 * np.ones((1, len(market_price)))
    delta_vol = np.zeros((1, len(market_price)))
    tol = 0.00001

    #Define a function of differnces between therotical and practical option price.
    def f_call(vol, i):
        return market_price[i] - callpx(S[i], K[i], r[i], vol[i], T[i])

    def f_put(vol, i):
        return market_price[i] - putpx(S[i], K[i], r[i], vol[i], T[i])
    #iteration
    for i in range(len(type)):
        #f_call function
        if type[i] == 1:
            while abs(f_call(guess_vol, i)) >= tol:
                itr[i] += 1
                #update values by newton's method
                delta_vol[i] = f_call(guess_vol, i) / vega(S, K, r, guess_vol, T, i)
                guess_vol[i] = delta_vol[i] + guess_vol[i]
            imp_vol[i] = guess_vol[i]
        #f_put
        elif type[i] == 0:
            while abs(f_put(guess_vol, i)) >= tol:
                itr[i] += 1
                delta_vol[i] = f_put(guess_vol, i) / vega(S, K, r, guess_vol, T, i)
                guess_vol[i] = delta_vol[i] + guess_vol[i]
            imp_vol[i] = guess_vol[i]

    return imp_vol, itr
