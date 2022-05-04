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