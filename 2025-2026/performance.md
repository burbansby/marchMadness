# March Madness Prediction Report — 2025–26

## Overall Accuracy

| Metric | Value |
| --- | --- |
| MAE (mean abs error) | 0.742 wins |
| RMSE | 0.968 wins |
| Bias (actual − predicted) | -0.230 (model overshot) |
| Correlation (r) | 0.704 |

## Coverage

| Metric | Value | Ideal |
| --- | --- | --- |
| Within ±1 std dev | 88.2% | ~68% |
| Within ±2 std devs | 98.5% | ~95% |
| Mean |Z-score| | 0.58 | ~0.80 |

## Results by Seed Group

| SeedGroup | Teams | MAE | Bias | Within1Sigma |
| --- | --- | --- | --- | --- |
| 1-4 (favorites) | 16 | 1.088 | 0.208 | 0.812 |
| 13-16 (underdogs) | 18 | 0.372 | -0.372 | 1.000 |
| 5-8 (mid-high) | 16 | 0.879 | -0.646 | 0.812 |
| 9-12 (mid-low) | 18 | 0.683 | -0.108 | 0.889 |

## Championship & Deep-Run Forecast

- **Model's title pick:** Houston (19.2% to win it all)
- **Actual champion:** Michigan (6 wins)
- **Champion Brier score:** 0.0148 (lower is better)
- **Final-4 Brier score:** 0.0493

> Title odds are rescaled to sum to 100% across the field. The model's raw `P(Champions)` column sums to 192% — its per-team distributions are not jointly normalized, so it over-allocates championship share (and deep runs generally; see calibration below).

Model's top title contenders (normalized odds) vs. how they finished:

| Team | Seed | TitleOdds | Actual |
| --- | --- | --- | --- |
| Houston | 2 | 19.189 | 2 |
| Iowa St. | 2 | 16.641 | 2 |
| Florida | 1 | 13.053 | 1 |
| Arizona | 1 | 10.400 | 4 |
| Duke | 1 | 9.308 | 3 |
| Illinois | 3 | 8.944 | 4 |
| Purdue | 2 | 7.904 | 3 |
| Michigan | 1 | 5.460 | 6 |

## Round-Reach Calibration

Expected = model's projected number of teams to reach each round; Actual = how many did.

| Round | Expected | Actual | Diff |
| --- | --- | --- | --- |
| Round of 32 (≥1 win) | 33.8 | 32 | -1.8 |
| Sweet 16 (≥2 wins) | 19.9 | 16 | -3.9 |
| Elite 8 (≥3 wins) | 12.6 | 8 | -4.6 |
| Final 4 (≥4 wins) | 6.8 | 4 | -2.8 |
| Title game (≥5 wins) | 3.7 | 2 | -1.7 |
| Champion (≥6 wins) | 1.9 | 1 | -0.9 |

## Conference Performance

| Conf | Teams | PredWins | ActualWins | MAE | Diff |
| --- | --- | --- | --- | --- | --- |
| B10 | 9 | 17.240 | 21.000 | 1.160 | 3.760 |
| SEC | 10 | 13.550 | 13.000 | 0.830 | -0.550 |
| B12 | 8 | 15.070 | 11.000 | 0.770 | -4.070 |
| BE | 3 | 4.080 | 7.000 | 1.630 | 2.920 |
| ACC | 8 | 12.300 | 6.000 | 0.790 | -6.300 |
| A10 | 2 | 1.080 | 2.000 | 0.460 | 0.920 |
| BSth | 1 | 0.440 | 1.000 | 0.560 | 0.560 |
| MWC | 1 | 1.040 | 1.000 | 0.040 | -0.040 |
| WCC | 3 | 4.240 | 1.000 | 1.080 | -3.240 |
| ASun | 1 | 0.490 | 0.000 | 0.490 | -0.490 |
| BW | 1 | 0.370 | 0.000 | 0.370 | -0.370 |
| CAA | 1 | 0.650 | 0.000 | 0.650 | -0.650 |
| Amer | 1 | 0.420 | 0.000 | 0.420 | -0.420 |
| BSky | 1 | 0.280 | 0.000 | 0.280 | -0.280 |
| AE | 1 | 0.350 | 0.000 | 0.350 | -0.350 |
| Ivy | 1 | 0.370 | 0.000 | 0.370 | -0.370 |
| Horz | 1 | 0.480 | 0.000 | 0.480 | -0.480 |
| CUSA | 1 | 0.550 | 0.000 | 0.550 | -0.550 |
| MAAC | 1 | 0.350 | 0.000 | 0.350 | -0.350 |
| MVC | 1 | 0.780 | 0.000 | 0.780 | -0.780 |
| NEC | 1 | 0.220 | 0.000 | 0.220 | -0.220 |
| MEAC | 1 | 0.170 | 0.000 | 0.170 | -0.170 |
| MAC | 2 | 1.110 | 0.000 | 0.550 | -1.110 |
| Pat | 1 | 0.270 | 0.000 | 0.270 | -0.270 |
| OVC | 1 | 0.290 | 0.000 | 0.290 | -0.290 |
| SC | 1 | 0.380 | 0.000 | 0.380 | -0.380 |
| SB | 1 | 0.420 | 0.000 | 0.420 | -0.420 |
| SWAC | 1 | 0.240 | 0.000 | 0.240 | -0.240 |
| Slnd | 1 | 0.620 | 0.000 | 0.620 | -0.620 |
| Sum | 1 | 0.430 | 0.000 | 0.430 | -0.430 |
| WAC | 1 | 0.390 | 0.000 | 0.390 | -0.390 |

## Confidence vs. Accuracy

Correlation between model confidence and absolute error: **-0.398** (higher confidence → lower error).

| ConfBucket | Teams | MAE | Bias |
| --- | --- | --- | --- |
| <40% | 15 | 1.013 | -0.272 |
| 40–60% | 16 | 1.025 | 0.178 |
| 60–80% | 15 | 0.682 | -0.638 |
| 80%+ | 22 | 0.393 | -0.221 |

## Cinderellas (Double-Digit Seeds, Most Wins)

| Team | Seed | Conf | Predicted | Actual | Error |
| --- | --- | --- | --- | --- | --- |
| Texas | 11 | SEC | 0.548 | 2 | 1.452 |
| Texas A&M | 10 | SEC | 0.674 | 1 | 0.326 |
| VCU | 11 | A10 | 0.568 | 1 | 0.432 |
| High Point | 12 | BSth | 0.436 | 1 | 0.564 |
| Santa Clara | 10 | WCC | 0.977 | 0 | -0.977 |

## Chalk Busts (Top-4 Seeds, Fewest Wins)

| Team | Seed | Conf | Predicted | Actual | Error |
| --- | --- | --- | --- | --- | --- |
| Florida | 1 | SEC | 3.338 | 1 | -2.338 |
| Gonzaga | 3 | WCC | 1.766 | 1 | -0.766 |
| Virginia | 3 | ACC | 1.673 | 1 | -0.673 |
| Kansas | 4 | B12 | 1.566 | 1 | -0.566 |
| Houston | 2 | B12 | 3.395 | 2 | -1.395 |

## Biggest Upsets (Actual >> Predicted)

| Team | Seed | Predicted | StdDev | Actual | ZScore |
| --- | --- | --- | --- | --- | --- |
| Connecticut | 2 | 1.593 | 1.393 | 5 | 2.446 |
| Michigan | 1 | 2.995 | 1.773 | 6 | 1.695 |
| Texas | 11 | 0.548 | 1.055 | 2 | 1.376 |
| Iowa | 9 | 1.285 | 1.417 | 3 | 1.210 |
| Tennessee | 6 | 1.845 | 1.471 | 3 | 0.785 |

## Biggest Busts (Actual << Predicted)

| Team | Seed | Predicted | StdDev | Actual | ZScore |
| --- | --- | --- | --- | --- | --- |
| Saint Mary's | 7 | 1.502 | 1.319 | 0 | -1.139 |
| Florida | 1 | 3.338 | 2.100 | 1 | -1.113 |
| Ohio St. | 8 | 1.505 | 1.361 | 0 | -1.106 |
| North Carolina | 6 | 1.469 | 1.400 | 0 | -1.050 |
| Wisconsin | 5 | 1.332 | 1.468 | 0 | -0.908 |

## Full Team Breakdown

| Team | Seed | Conf | Predicted | StdDev | Actual | Error | ZScore | WithinOneSigma |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Connecticut | 2 | BE | 1.593 | 1.393 | 5 | 3.407 | 2.446 | ✗ |
| Michigan | 1 | B10 | 2.995 | 1.773 | 6 | 3.005 | 1.695 | ✗ |
| Florida | 1 | SEC | 3.338 | 2.100 | 1 | -2.338 | -1.113 | ✗ |
| Iowa | 9 | B10 | 1.285 | 1.417 | 3 | 1.715 | 1.210 | ✗ |
| Ohio St. | 8 | B10 | 1.505 | 1.361 | 0 | -1.505 | -1.106 | ✗ |
| Saint Mary's | 7 | WCC | 1.502 | 1.319 | 0 | -1.502 | -1.139 | ✗ |
| North Carolina | 6 | ACC | 1.469 | 1.400 | 0 | -1.469 | -1.050 | ✗ |
| Texas | 11 | SEC | 0.548 | 1.055 | 2 | 1.452 | 1.376 | ✗ |
| Illinois | 3 | B10 | 2.553 | 2.215 | 4 | 1.447 | 0.653 | ✓ |
| Houston | 2 | B12 | 3.395 | 2.319 | 2 | -1.395 | -0.602 | ✓ |
| Wisconsin | 5 | B10 | 1.332 | 1.468 | 0 | -1.332 | -0.908 | ✓ |
| Iowa St. | 2 | B12 | 3.217 | 2.205 | 2 | -1.217 | -0.552 | ✓ |
| Tennessee | 6 | SEC | 1.845 | 1.471 | 3 | 1.155 | 0.785 | ✓ |
| NC State | 11 | ACC | 1.139 | 1.465 | 0 | -1.139 | -0.777 | ✓ |
| BYU | 6 | B12 | 1.112 | 1.393 | 0 | -1.112 | -0.798 | ✓ |
| Villanova | 8 | BE | 0.980 | 1.366 | 0 | -0.980 | -0.717 | ✓ |
| Santa Clara | 10 | WCC | 0.977 | 1.418 | 0 | -0.977 | -0.689 | ✓ |
| Clemson | 8 | ACC | 0.925 | 1.239 | 0 | -0.925 | -0.747 | ✓ |
| Georgia | 8 | SEC | 0.912 | 1.397 | 0 | -0.912 | -0.653 | ✓ |
| SMU | 11 | ACC | 0.878 | 1.385 | 0 | -0.878 | -0.634 | ✓ |
| Arizona | 1 | B12 | 3.167 | 1.881 | 4 | 0.833 | 0.443 | ✓ |
| Northern Iowa | 12 | MVC | 0.782 | 1.021 | 0 | -0.782 | -0.766 | ✓ |
| Gonzaga | 3 | WCC | 1.766 | 1.432 | 1 | -0.766 | -0.535 | ✓ |
| Virginia | 3 | ACC | 1.673 | 1.468 | 1 | -0.673 | -0.459 | ✓ |
| Louisville | 6 | ACC | 1.670 | 1.375 | 1 | -0.670 | -0.488 | ✓ |
| Hofstra | 13 | CAA | 0.649 | 1.056 | 0 | -0.649 | -0.614 | ✓ |
| Missouri | 10 | SEC | 0.643 | 1.115 | 0 | -0.643 | -0.577 | ✓ |
| McNeese | 12 | Slnd | 0.621 | 0.989 | 0 | -0.621 | -0.628 | ✓ |
| Miami OH | 11 | MAC | 0.592 | 0.983 | 0 | -0.592 | -0.602 | ✓ |
| Nebraska | 4 | B10 | 1.432 | 1.286 | 2 | 0.568 | 0.442 | ✓ |
| Kansas | 4 | B12 | 1.566 | 1.081 | 1 | -0.566 | -0.524 | ✓ |
| High Point | 12 | BSth | 0.436 | 0.859 | 1 | 0.564 | 0.657 | ✓ |
| Kennesaw St. | 14 | CUSA | 0.555 | 0.931 | 0 | -0.555 | -0.595 | ✓ |
| Vanderbilt | 5 | SEC | 1.554 | 1.617 | 1 | -0.554 | -0.342 | ✓ |
| UCF | 10 | B12 | 0.524 | 1.019 | 0 | -0.524 | -0.514 | ✓ |
| Akron | 12 | MAC | 0.515 | 0.924 | 0 | -0.515 | -0.557 | ✓ |
| UCLA | 7 | B10 | 1.497 | 1.481 | 1 | -0.497 | -0.336 | ✓ |
| St. John's | 5 | BE | 1.511 | 1.389 | 2 | 0.489 | 0.352 | ✓ |
| Queens | 15 | ASun | 0.488 | 0.807 | 0 | -0.488 | -0.604 | ✓ |
| Saint Louis | 9 | A10 | 0.515 | 1.027 | 1 | 0.485 | 0.472 | ✓ |
| Wright St. | 14 | Horz | 0.480 | 0.940 | 0 | -0.480 | -0.511 | ✓ |
| Miami FL | 7 | ACC | 1.462 | 1.628 | 1 | -0.462 | -0.284 | ✓ |
| VCU | 11 | A10 | 0.568 | 1.003 | 1 | 0.432 | 0.430 | ✓ |
| North Dakota St. | 14 | Sum | 0.429 | 0.921 | 0 | -0.429 | -0.466 | ✓ |
| Troy | 13 | SB | 0.418 | 0.939 | 0 | -0.418 | -0.444 | ✓ |
| South Florida | 11 | Amer | 0.416 | 0.947 | 0 | -0.416 | -0.439 | ✓ |
| Cal Baptist | 13 | WAC | 0.386 | 0.782 | 0 | -0.386 | -0.494 | ✓ |
| Furman | 15 | SC | 0.380 | 0.896 | 0 | -0.380 | -0.424 | ✓ |
| Alabama | 4 | SEC | 1.624 | 1.607 | 2 | 0.376 | 0.234 | ✓ |
| Arkansas | 4 | SEC | 1.624 | 1.547 | 2 | 0.376 | 0.243 | ✓ |
| Hawaii | 13 | BW | 0.374 | 0.744 | 0 | -0.374 | -0.503 | ✓ |
| Penn | 14 | Ivy | 0.369 | 0.812 | 0 | -0.369 | -0.455 | ✓ |
| UMBC | 16 | AE | 0.353 | 0.845 | 0 | -0.353 | -0.418 | ✓ |
| Siena | 16 | MAAC | 0.347 | 0.838 | 0 | -0.347 | -0.414 | ✓ |
| Texas A&M | 10 | SEC | 0.674 | 1.095 | 1 | 0.326 | 0.298 | ✓ |
| Tennessee St. | 15 | OVC | 0.287 | 0.716 | 0 | -0.287 | -0.401 | ✓ |
| Idaho | 15 | BSky | 0.283 | 0.737 | 0 | -0.283 | -0.384 | ✓ |
| Texas Tech | 5 | B12 | 1.281 | 1.445 | 1 | -0.281 | -0.195 | ✓ |
| Lehigh | 16 | Pat | 0.267 | 0.659 | 0 | -0.267 | -0.406 | ✓ |
| Prairie View | 16 | SWAC | 0.245 | 0.693 | 0 | -0.245 | -0.353 | ✓ |
| LIU | 16 | NEC | 0.224 | 0.675 | 0 | -0.224 | -0.332 | ✓ |
| Kentucky | 7 | SEC | 0.784 | 1.093 | 1 | 0.216 | 0.198 | ✓ |
| TCU | 9 | B12 | 0.803 | 1.079 | 1 | 0.197 | 0.183 | ✓ |
| Purdue | 2 | B10 | 2.813 | 2.002 | 3 | 0.187 | 0.093 | ✓ |
| Michigan St. | 3 | B10 | 1.831 | 1.550 | 2 | 0.169 | 0.109 | ✓ |
| Howard | 16 | MEAC | 0.167 | 0.638 | 0 | -0.167 | -0.262 | ✓ |
| Duke | 1 | ACC | 3.085 | 2.056 | 3 | -0.085 | -0.041 | ✓ |
| Utah St. | 9 | MWC | 1.037 | 1.274 | 1 | -0.037 | -0.029 | ✓ |
