import numpy as np
from matplotlib import pyplot as plt
from BSM import black_scholes_call

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

if __name__ == '__main__':
    
    # Volatility and drift to be sourced empirically from pricing sources
    volatility = 0.25
    r = 0.05
    q = 0.02
    drift = r - q
    strike = 110
    S0 = 100
    
    N = 10000
    T = 0.5
    steps = 100
    
    call = black_scholes_call(S0,strike,T,r,q,volatility)
    print(f"BSM: {call}")
    S, payoffs, op = mc_pricer(T, steps, N, volatility, drift, strike, S0, r)

    print(f"Mean payoff: {payoffs.mean()}\nOption Price: {op}")
    plt.plot(S, linewidth=0.5, alpha=0.6)
    plt.plot(S.mean(1), color="red", linewidth=2, label="Average Path")
    plt.xlabel("Months")
    plt.ylabel("Asset Price, a.u.")
    plt.legend()
    plt.figure()
    plt.hist(payoffs, bins=20, edgecolor="black")
    plt.title("Distribution of Payoffs")
    plt.xlabel("Payoff")
    plt.ylabel("Frequency")
    
    # Plotting payoff against N to check convergence
    plt.figure()
    results = []
    calls = []
    max_sim = 5000
    for N_sim in range(100, max_sim, 100):
        print(f"{N_sim} / {max_sim}")
        _, payoff, _ = mc_pricer(T, steps, N_sim, volatility, drift, strike, S0, r)
        call = black_scholes_call(S0,strike,T,r,q,volatility)
        results.append(payoff.mean())
        calls.append(call)
        
    plt.plot(range(100, 5000, 100), results)
    plt.plot(range(100, 5000, 100), calls, color = 'k')
    plt.title("Convergence of Option Price with N")
    plt.xlabel("Number of Simulations")
    plt.ylabel("Payoff")

    plt.show()