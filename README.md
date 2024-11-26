# Monte-Carlo (MC) Options Pricer
Experimenting with the development of a monte-carlo approach to the pricing of call and put options for personal development in the field of quantiive finance. 

 There are two main files in this repo:
 - mc_pricer.py - the main script and mc_pricer function (optimised and non-optimised versions)
 - BSM.py - an implementation of the black-scholes model (not mine) to benchmark of monte-carlo performance. See file for credit.

This work has been a key aid in my education in stochastic calculus, with the following activity being conducted:
- derivation of Ito's Lemma (below) from the Taylor series expansion of a function f(S(t), t) to second order terms.
 $df(S_{t}, t) = \left( \frac{\partial f}{\partial t} + \mu \frac{\partial f}{\partial S_t} + \frac{1}{2} \sigma^2 \frac{\partial^2 f}{\partial S_t^2} \right) dt + \sigma \frac{\partial f}{\partial S_t} dW_t$
 
- application of Ito's Lemma to $f(S_t, t)=ln(S_t)$ and implementation in code

\section*{Derivation of Ito's Lemma}

Let \( f(S_t, t) \) be a twice-differentiable function of \( t \) and \( S_t \), where \( S_t \) follows a stochastic process. The Taylor series expansion of \( f(S_t, t) \) around a small increment in time \( dt \) is given by:

\[
f(S_{t+dt}, t+dt) = f(S_t, t) + \frac{\partial f}{\partial t} dt + \frac{\partial f}{\partial S_t} dS_t + \frac{1}{2} \frac{\partial^2 f}{\partial S_t^2} (dS_t)^2 + O(dt^3)
\]

Here, \( dS_t \) is the infinitesimal change in \( S_t \), and the term \( (dS_t)^2 \) accounts for the quadratic variation of the stochastic process.

Assume \( S_t \) follows a stochastic differential equation (SDE) of the form:

\[
dS_t = \mu dt + \sigma dW_t
\]

where \( \mu \) is the drift term, \( \sigma \) is the volatility term, and \( dW_t \) is the increment of a Wiener process (Brownian motion). The quadratic variation \( (dS_t)^2 \) is given by:

\[
(dS_t)^2 = \sigma^2 dt
\]

because the increment of the Brownian motion satisfies \( (dW_t)^2 = dt \).

Substitute \( dS_t = \mu dt + \sigma dW_t \) and \( (dS_t)^2 = \sigma^2 dt \) into the Taylor series expansion:

\[
f(S_{t+dt}, t+dt) = f(S_t, t) + \frac{\partial f}{\partial t} dt + \frac{\partial f}{\partial S_t} (\mu dt + \sigma dW_t) + \frac{1}{2} \frac{\partial^2 f}{\partial S_t^2} \sigma^2 dt
\]

Rearranging the terms, we get:

\[
f(S_{t+dt}, t+dt) - f(S_t, t) = \left( \frac{\partial f}{\partial t} + \mu \frac{\partial f}{\partial S_t} + \frac{1}{2} \sigma^2 \frac{\partial^2 f}{\partial S_t^2} \right) dt + \sigma \frac{\partial f}{\partial S_t} dW_t
\]

The left-hand side represents the infinitesimal change in \( f(S_t, t) \), which we denote as \( df(S_t, t) \):

\[
df(S_t, t) = \left( \frac{\partial f}{\partial t} + \mu \frac{\partial f}{\partial S_t} + \frac{1}{2} \sigma^2 \frac{\partial^2 f}{\partial S_t^2} \right) dt + \sigma \frac{\partial f}{\partial S_t} dW_t
\]

This is the standard form of \textit{Ito's Lemma}, which provides the differential of a function \( f(S_t, t) \) when \( S_t \) follows a stochastic process with drift \( \mu \) and volatility \( \sigma \).
