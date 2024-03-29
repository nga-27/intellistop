### `use_memory` Input Argument for "Conservative" Stops

Optionally, as of version `1.2.0`, you can pass a boolean to the optional field of `use_memory` to `stops = IntelliStop()`. This is shown below:

```python
from intellistop import Intellistop

stops = IntelliStop(use_memory=True)
vf_data, has_error = stops.run_analysis_for_ticker(ticker_str)

# Default is to only return 'Close' data
close = stops.return_data(fund)

# Optionally can pass in the exact key (see details of function)
dates = stops.return_data(fund, key='__full__').get('Date', [])
```

When you enable the `use_memory` flag, you allow IntelliStop to create a directory and "database" (JSON file) to store VF information. (In the future, this could enable other functionality.) For now, when this flag is set to `True`, IntelliStop will reference [or create and then reference] the file `/output/__internal_intellistop.json` to keep track of certain volatility factor information.

One such item is what is called a "conservative VF" or "conservative stop loss". Essentially, IntelliStop keeps track of the minimum VF that exists during the existence of the DB file as well as the duration of a positively tracking trend. What sometimes happens to an equity, especially during periods of higher-than-normal volatility, is that the volatility factor will grow enough that the stop loss value will actually _go down_. Remember, in a good trend, we only want stop losses to go _UP_ or hold not down!

For example: say a stock hits a peak a few months prior at $100 with a VF of 10. A few months later, the stock has been trading sideways with increased volatility around $95 and with an updated VF of 14. (Typically, VF values won't increase this significantly over such a period, but this will help illustrate the need for conservative stop losses.) Now, the original stop loss calculated a few months ago was about $90. Today, even though the stock has not exceeded its original max, the new stop loss is at $86. 

Does this mean that the original $90 stop loss was wrong? Probably not. In fact, if this period of volatility is truly out of the ordinary, you won't want to use the updated VF value for this to generate your stop loss. In this case, you probably want to keep the original. But let's say you run IntelliStop only a few times a year, say once a quarter: you might not have remembered what the original VF was. If a VF of 10 and a stop loss of $90 was truly a major support level, then breaking it [on the way to $86] could cause larger losses than you might want. Breaking major supports, after all, typically mean non-insignificant pain and loss ahead and, sometimes, quickly!

In this example, perhaps you catch the closing below $86 at $85.99, so a minimal loss past your stop loss. But recalling that your original level was $90, you still lost over $4 a share past what you expected. In this case, by using the `use_memory` argument every time you run IntelliStop, even if it's quarterly or less often, you can maintain the most conservative or most stable VF and stop loss the equity would have.

Fundamentally, does it matter to have a more aggressive VF or a stop loss that drifts lower than it originally was? No, but it undermines the major concept that IntelliStop tries to address: increased volatility typically means a change in trend, and if that trend is flat or up, you want to protect yourself from unnecessary losses by holding the stop loss firm. If the increased volatility means a change for the positive - great! In this case, the stop loss will rise with the price action regardless. This is what we want. But, again, increased volatility that leads toward the negative is never good, and we want our stop losses to protect us from losses we don't need.

In the upper left corner of the plot window, you'll see the standard VF and stop loss values. For equities that are in a positive price trend, you'll also see the addition of the "Cons" VF and stop loss values. These are reflective of the more stable, less volatile VFs in the history of the equity. Again, this is based on the combination of the existence of the DB file (stored locally on your machine) and the duration of the positive price trend. An example is below:

![conservative_sl_vf](./stable_conservative_vf_sl.png)

You'll also see a third stop loss line in orange. This is the stop loss generated by the conservative / stable VF value. In this way, you can close out a position that crosses this line before it crosses the red, traditional stop loss line. (The red one is based off the traditional VF value.)
