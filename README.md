# intellistop

Library tool to determine a smart stop-loss for technical analysis of funds. This utilizes the ***[Volatility Factor (VF)](#vf)***.

---

# Configuration Keys

The default configurations [to date] are below. See `intellistop/libs/types` for other configuration inputs.
```json
{
    "interval": "1d",
    "period": "5y",
    "momentum_period": 10,
    "momentum_metric": "Close",
    "momentum_calculator": 0,
    "k_ratio_is_log": false,
    "k_ratio_algorithm": 2013,
    "vq_properties_level": 2
}
```

# Entry Signal Triggers

1. Security's price must rise more than 1 VQ from its lowest bottom since it hit the red/stop zone
2. _Slope_ of the "smart moving average" (their trendline) must rise above a specific threshold

(VQ may only need about a year's worth of data to compute, according to docs.)

## Smart Moving Average (SmMA)

### Algorithm

Using the "created" SmMA, we'll look at a few conditions. Our targeted **BUY** signal is after the following 4 conditions are achieved:

1. Price rides 1 VQ (%) above bottom / minimum
2. Price rides above the SmMA
3. SMA-15(Slope(SmMA[k])) > 0
4. SMA-50(Slope(SmMA[k])) > 0
5. SMA-15 > SMA-50

### Prospective algorithm

1. Calculate VQ
2. Fetch larger data set.
3. Set extrema mask percent (threshold between local maxima and minima, some % of VQ).
4. Generate list of extrema points.
5. Iteratively determine what period of SmMA fits the extrema criteria the best (with the lowest overall variance)
6. Find the Green-Yellow-Red zones of a fund

# <a name="vf"></a>Volatility Factor (VF)

# Other Links

* [Tradesmith bootcamps](https://tradesmith.zendesk.com/hc/en-us/sections/5551499479956-TradeSmith-Bootcamp-Beginner-Lessons)
* [Smart Moving Average (SmMA)](https://tradestops.com/blog/when-to-get-back-in/#:~:text=The%20Smart%20Moving%20Average%20tells,a%20bottom%20is%20in%20place.)