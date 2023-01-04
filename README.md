# intellistop

Library tool to determine a smart stop-loss for technical analysis of funds. This utilizes the ***[Volatility Factor (VF)](#vf)***.

<img alt="spy-stop-loss" src="static/spy_stop_loss.png" width=600/>

---

# What is Intellistop?

Intellistop is a tool that derives some mathematical features of a fund's price that can help an investor better understand when to **buy** and **sell** a particular equity.

First, the obvious disclaimer: ***the Intellistop tool and its author are not liable for any personal investing performance***. After all, there are a myriad of tools out there that can help an investor make investing decisions, and all of them basically say the same thing - _you're on your own_.

Now, back to the tool...

The tool centers around two philosophies:

* Stop losses should be used to protect gains and assets, and
* Price action remains within a factor of volatility _unless_ a major change to the trend occurs.

Fellow Technical Analysts or Quants might deduce from the above that if an equity drops beyond its normal volatility range, then a larger change in trend might be starting. Since it's a drop, it might signal the start of a larger downward trend. If this conjecture is reasonable, then it would also be reasonable to suggest that the stop loss value should be somehow related to this normal volatility range.

So... If there was a way to derive the correct normal volatility factor of a given equity, then it be possible to set a stop loss that would balance the benefit letting an equity have room to move around in a normal capacity with the protection of avoiding large losses on a larger downward trend. In this same vein, this similar method would be able suggest when a larger downward trend is ending and when it's a good time to re-enter a trade.

This conjecture, at its heart, is the main function of **Intellistops**.

Intellistops generates a [_volatility factor_](#vf) (VF) that is used to derive both a _stop loss for upward-trending equities_ and a _re-entry signal after a downward trend concludes_.

---

# Installation

To run the `IntelliStop` library as an import [in something else], simply run pip install as you normally would:

```sh
pip install .

# For MacOS / or zsh
pip install '.'
```

To run the standalone program, the one that will generate a plot image with a requested input ticker, install the additional `app` installations. (This primarily includes `matplotlib`):

```sh
pip install .[app]

# For MacOS / or zsh
pip install '.[app]'
```

# Entry Signal Triggers

1. An equity's price must rise more than 1 Volatility Factor (**VF**) from its lowest bottom since it hit the red/stop zone
2. _Slope_ of the "intelligent moving average" (the equity's trend line) must rise above a specific threshold

The second of these triggers is derived from a Intelligent Moving Average, or IMA.

## Intelligent Moving Average (IMA)

### Algorithm

Using the "created" IMA, we'll look at a few conditions. Our targeted **BUY** signal is after the following 5 conditions are achieved:

1. Price rides 1 VF (%) above bottom / minimum
2. Price rides above the IMA
3. $SMA_{15}[Slope[IMA[k]]] > 0$
4. $SMA_{50}[Slope(IMA[k]]] > 0$
5. $SMA_{15} > SMA_{50}$

# <a name="vf"></a>Volatility Factor (VF)

Now it's math time. How is the Volatility Factor (VF) calculated?

[The Whitepaper](./static/volatility_factor.md)
