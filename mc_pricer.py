import numpy as np
from matplotlib import pyplot as plt
from BSM import BS_CALL

# Initial version of the mc_pricing function before optimisation
def mc_pricer(T, steps, N, volatility, drift, strike, S0, r, call = True):
    dt = T/steps
    S = np.zeros((steps, N))
    payoffs = np.zeros(N)
    for episode in range(N):
        S_old = np.log(S0)
        for t in range(steps):
            # GBM update rule where S_new = ln(S_t) and S_old = ln(S_{t-1}). S_new raised to the exponent
            # and stored in S.
            S_new = S_old + (drift - 0.5*volatility**2)*dt + volatility*np.sqrt(dt)*np.random.normal(0,1)
            S[t, episode] = np.exp(S_new)
            S_old = S_new
        
        # calculate the payoff for each episode depending on the option type
        payoffs[episode] = np.maximum(S[-1, episode] - strike, 0) if call else np.maximum(strike - S[-1, episode], 0)
    
    # calculate the option price using the E[payoff] identified through mc
    option_price = np.exp(-r*T)*payoffs.mean()
    
    return S, payoffs, option_price

# An optimsied version of the monte-carlo options pricing function using vectorised variables,
# and using numpy broadcasting with np.cumsum().
def mc_pricer_optimised(T, steps, N, volatility, drift, strike, S0, r, call = True):
    dt = T/steps
    S = np.zeros((steps, N))
    Z = np.random.normal(size = (steps, N))

    # GBM update rule where S_new = ln(S_t) and S_old = ln(S_{t-1}). S_new raised to the exponent
    # and stored in S.
    S_log = np.log(S0) + np.cumsum((drift - 0.5*volatility**2)*dt + volatility*np.sqrt(dt)*Z, axis=0)
    S = np.exp(S_log)
        
    # calculate the payoff for each episode depending on the option type
    payoffs = np.maximum(S[-1, :] - strike, 0) if call else np.maximum(strike - S[-1, :], 0)
    
    # calculate the option price using the E[payoff] identified through mc
    option_price = np.exp(-r*T)*payoffs.mean()
    return S, payoffs, option_price

if __name__ == '__main__':

    volatility = 0.25
    r = 0.05
    q = 0.02
    drift = r - q
    strike = 110
    S0 = 100
    
    N = 10000
    T = 0.5
    steps = 100
    
    call = BS_CALL(S0,strike,T,r-q,volatility)
    
    print(f"BSM: {call}")
    S, payoffs, op = mc_pricer_optimised(T, steps, N, volatility, drift, strike, S0, r)

    print(f"Mean payoff: {payoffs.mean()}\nOption Price: {op}")
    plt.plot(S, linewidth=0.5, alpha=0.6)
    plt.plot(S.mean(1), color="red", linewidth=2, label="Mean Path")
    plt.xlabel("Steps")
    plt.ylabel("Asset Price, a.u.")
    plt.legend()
    plt.figure()
    plt.hist(payoffs, bins=10, edgecolor="black")
    plt.title("Distribution of Payoffs")
    plt.xlabel("Payoff, a.u.")
    plt.ylabel("Frequency")
    
    # Plotting payoff against N to check convergence
    plt.figure()
    results = []
    calls = []
    min_sim = 1
    max_sim = 500
    for N_sim in range(min_sim, max_sim+1, 1):
        if N_sim % 100 == 0 or N_sim == min_sim or N_sim == max_sim: print(f"{N_sim} / {max_sim}")
        _, payoffs, _ = mc_pricer_optimised(T, steps, N_sim, volatility, drift, strike, S0, r)
        call = BS_CALL(S0,strike,T,r-q,volatility)
        results.append(payoffs.mean())
        calls.append(call)
    
    plt.plot(range(min_sim, max_sim+1, 1), results)
    plt.plot(range(min_sim, max_sim+1, 1), calls, color = 'k')
    plt.title("Convergence of Option Price with N")
    plt.legend(["Monte-Carlo", "Black-Scholes"])
    plt.xlabel("Number of Simulations, N")
    plt.ylabel("Payoff, a.u.")
    
    plt.show()