# Volatility Factor

The algorithm to generate the **Volatility Factor (VF)** can be broken into seven discrete steps, outlined below. For all steps, the following is true:

$f[k]$ refers to the equity price in a 5-year window. The price can be either `"Close"` or `"Adj Close"`.

## Step 1: 200d Moving Average Filter

$$
M_n[f[k]] =
  \begin{cases}
    f[k]       & \quad k \lt n\\
    \frac{1}{n} \displaystyle\sum_{i=k-n}^{k} f[i]  & \quad k \ge n
  \end{cases}
$$

Letting $n = 200$ as a simple moving average...

$$
M_{200}[f[k]] =
  \begin{cases}
    f[k]       & \quad k \lt 200\\
    \frac{1}{200} \displaystyle\sum_{i=k-n}^{k} f[i]  & \quad k \ge 200
  \end{cases}
  = M_{200}[k]
$$

Ultimately, Step 1 yields the 200-day simple moving average signal.

## Step 2: Apply a "High Pass" Filter to the Price Signal

Knowing the variance and standard deviation typically requires a normal-distribution, and knowing that price action of an equity rarely has a normal distribution without potentially significant kurtosis and/or skew, it's not ideal to use variance or standard deviation directly. For that, we'll apply a "high pass" filter to the price data, effectively subtracting $M_{200}[k]$ from step 1:

$$ L_n[f[k], M_n[k]] = f[k] - M_n[k] |_0^{5y} $$
$$ L_{200}[k] = f[k] - M_{200}[k] |_0^{5y} $$

## Step 3: Fourier Transform

Step 2 yields a high-pass-filtered price set, one that still maintains some skew and kurtosis, but ultimately has a new property: $L_{200}[k] > 0$ for uptrend price action ("active" with a valid stop loss), and $L_{200}[k] < 0$ for "stopped out" downward trend price action. We'll take $L_{200}[k]$ and find which time periods that are significant (besides the entire data set length). Why? If we are to apply a moving variance calculation, we'll want to find a period that closely resembles _smaller but normal_ price action so as to not cause aliasing in the variance signal itself.

To find periods of choice, we'll do the fourier transform on $L_{200}[k]$ data set to obtain the frequency spectrum $H[x]$:

$$ H[x] = \displaystyle\sum_{k=0}^{N-1} L_{200}[k]e^{-i2\pi xk/N} $$

## Step 4: $a^{th}$ Period Transform

We'll take the frequency spectrum $H[x]$ and find the $a^{th}$ maximum density period. Experimentally, the 10th was chosen:

$$ T_a = \frac{1}{[H[x]]_a} = \frac{1}{[H[x]]_{10}} = T_{10} $$

## Step 5: Standard Deviation of Signals Over Time

As noted in steps 2 and 3, we'll be finding the variance or standard deviation over time for the $L_{200}[k]$ signal. In this particular variation,we'll be using standard deviation (or the square-root of the variance):

$$
\sigma _c[k] =
  \begin{cases}
    \sqrt{\frac{1}{C} \displaystyle\sum_{i=0}^{C-1} \Big(L_{200}[i] - \frac{1}{C} \displaystyle\sum_{j=0}^{C-1} L_{200}[j]\Big)}       & \quad k \lt C\\
    \sqrt{\frac{1}{C} \displaystyle\sum_{i=k-C}^{k} \Big(L_{200}[i] - \frac{1}{C} \displaystyle\sum_{j=k-C}^{k} L_{200}[j]\Big)}  & \quad k \ge C
  \end{cases}
$$

Where $ c = 50$, so $ \sigma _{50}[k] $ and $ c = T_{10} $, so $ \sigma _{T_{10}}[k]$

We'll use both a period of 50 (50 day window for the standard deviation) and the $T_{10}$ period derived from step 4. Both standard deviation data sets will be used in step 6.

## Step 6: Above & Below Separation Analysis

We'll separate the standard deviation data sets into "above" [the long moving average from step 1] and "below":

* Above: $A_c[k] = \sigma _c[k] \text{ if } f[k] > M_{200}[k]$
* Below: $B_c[k] = \sigma _c[k] \text{ if } f[k] > M_{200}[k]$

... for both $c = 50$ and $c = T_{10}$. We'll calculate the average of the separated signals:

* $\bar{A}_c = A_{c_{mean}} = \frac{1}{N} \displaystyle\sum_{i=0}^{N-1}A_c[i]$
* $\bar{B}_c = B_{c_{mean}} = \frac{1}{N} \displaystyle\sum_{i=0}^{N-1}B_c[i]$

## Step 7: Volatility Factor and Stop Loss

Finally, we'll calculate the parts we've wanted to derive this whole time: the **Volatility Factor**. From here, we'll be able to calculate a stop loss if the equity is in an "active" (non-stopped-out) state.

$ \text{Root-mean-squared: } R_c = \sqrt{\bar{A}_c^2 + \bar{B}_c^2} $

$ \text{Volatility Factor: } V_c = 100 * \frac{3R_c}{\frac{1}{N} \displaystyle\sum_{i=0}^{N-1}f[i]} $

$ \text{Stop Loss: } W_c = max(f[k] |_0^N) * (1 - \frac{V_c}{100}) $

# Summary of Algorithm

1. Use price $f[k]$ to derive $M_{200}[k]$ 200-day simple moving average.
2. Use price $f[k]$, $M_{200}[k]$ to derive the high-pass-filtered $L_{200}[k]$.
3. Use high-pass-filtered $L_{200}[k]$ to derive the fourier-transformed $H[x]$.
4. Use fourier-transformed $H[x]$ to derive period scalar $T_{10}$.
5. Use high-pass-filtered $L_{200}[k]$ and $T_{10}$ to derive standard deviation $\sigma _c[k]$.
6. Use standard deviation $\sigma _c[k]$ to derive means $\bar{A}_c$ and $\bar{B}_c$.
7. Use means $\bar{A}_c$ and $\bar{B}_c$ to derive **VF** $V_c$ and **Stop Loss** $W_c$.