# Monte-Carlo (MC) Options Pricer
Experimenting with the development of a monte-carlo approach to the pricing of call and put options for personal development in the field of quantitative finance. 

 There are two main files in this repository:
 - mc_pricer.py - the main script and mc_pricer function (optimised and non-optimised versions)
 - BSM.py - an implementation of the Black-Scholes model (not mine) to benchmark monte-carlo performance. See file for credit.

This work has been a key aid in my education in stochastic calculus, and has supplemented the following learning objectives:
- derivation of Ito's Lemma (below) from the Taylor series expansion of a function $f(S_{t}, t)$ to second order terms.

$$df(S_{t}, t) = \left( \frac{\partial f}{\partial t} + \mu \frac{\partial f}{\partial S_t} + \frac{1}{2} \sigma^2 \frac{\partial^2 f}{\partial S_t^2} \right) dt + \sigma \frac{\partial f}{\partial S_t} dW_t$$
 
- application of Ito's Lemma to $f(S_t, t)=ln(S_t)$ and implementation in code.

The output of the mc_pricer.py script is assembled into three plots.

*N paths produced from an asset with a starting value of 100 a.u.*

![](figures/paths.png)

*Histogram of payoffs*

![](figures/hist.png)

*The MC function converges to the BSM as N increases*

![](figures/convergence.png)
