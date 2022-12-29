# intellistop
Library to determine a smart stop-loss for technical analysis of funds.

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
2. Slope of the "smart moving average" (their trendline) must rise above a specific threshold

(VQ may only need about a year's worth of data to compute, according to docs.)

## Thoughts on SmMA

* Line should be a strong support/resistance line for major bounces along **major** trends
* Slope trigger threshold (above) should be inversely proportional to length of average (higher the VQ, the shorter the period)
    * Slope threshold will likely be some % (maybe >= 50%?) of the max [positive] slope detected over a long period
* From local peak to local minima, threshold drop should be some function of `x * VQ`, where x is some value likely between 0 and 1
* SmMA should find least variance on the "trend-based extrema" points within some small percent (perhaps <=10% of VQ?) of the trend line
* "Trend-based extrema" implies local minima on up trends and local maxima on down trends

Other thought: if a shorter SMA fits tighter to a signal, and therefore is more volatile with a more volatile signal, does this mean that, in fact, the SmMA period value is _proportional_ to the VQ? (i.e. a more volatile security should have a higher period, and a more stable security will have a smaller period?) This may actually not be true, as we're looking for trends of support / resistance purely volatility.

### Alternative Idea

Using the "created" SmMA, we'll look at a few conditions. Our targeted **BUY** signal is after the following 4 conditions are achieved:

1. Price rides 1 VQ (%) above bottom / minimum
2. Price rides above the SmMA
3. SMA-15(Slope(SmMA[k])) > 0
4. SMA-50(Slope(SmMA[k])) > 0 and SMA-15 > SMA-50

### Prospective algorithm

1. Calculate VQ
2. Fetch larger data set.
3. Set extrema mask percent (threshold between local maxima and minima, some % of VQ).
4. Generate list of extrema points.
5. Iteratively determine what period of SmMA fits the extrema criteria the best (with the lowest overall variance)
6. Find the Green-Yellow-Red zones of a fund

# Other Links

* [Tradesmith bootcamps](https://tradesmith.zendesk.com/hc/en-us/sections/5551499479956-TradeSmith-Bootcamp-Beginner-Lessons)
* [Smart Moving Average (SmMA)](https://tradestops.com/blog/when-to-get-back-in/#:~:text=The%20Smart%20Moving%20Average%20tells,a%20bottom%20is%20in%20place.)