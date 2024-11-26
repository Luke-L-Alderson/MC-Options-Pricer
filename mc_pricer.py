import numpy as np
from matplotlib import pyplot as plt

def mc_pricer(T, t_steps, N, volatility, drift, strike, S0):
    dt = T/t_steps
    S = np.ndarray((t_steps, N))
    payoffs = np.ndarray(N)
    for episode in range(N):
        S_old = np.log(S0)
        for t in range(t_steps):
            S_new = S_old + (drift - 0.5*volatility**2)*dt + volatility*np.sqrt(dt)*np.random.normal(0,1)
            S[t, episode] = np.exp(S_new)
            S_old = S_new
        
        # calculate the payoff for each episode
        payoffs[episode] = np.max(S[-1, episode]-strike, 0)
    
    # find the expected payoff by averaging over episodes
    exp_payoff = payoffs.mean()
    return S, exp_payoff

if __name__ == '__main__':
    # dummy example
    volatility = 0.25
    drift = 0.02
    N = 1000
    T = 5
    t_steps = 1000
    strike = 105
    S0 = 100
    
    S1, gain = mc_pricer(T, t_steps, N, volatility, drift, strike, S0)
    print(f"The asset gain is: {gain}")
    plt.plot(S1, linewidth=0.5)
    plt.figure()
    plt.plot(S1.mean(1))
    
    plt.show()