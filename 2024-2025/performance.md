# March Madness Prediction Report — 2024–25

## Overall Accuracy

| Metric | Value |
| --- | --- |
| MAE (mean abs error) | 0.787 wins |
| RMSE | 1.129 wins |
| Bias (actual − predicted) | -0.093 (model overshot) |
| Correlation (r) | 0.535 |

## Coverage

| Metric | Value | Ideal |
| --- | --- | --- |
| Within ±1 std dev | 85.3% | ~68% |
| Within ±2 std devs | 95.6% | ~95% |
| Mean |Z-score| | 0.67 | ~0.80 |

## Results by Seed Group

| SeedGroup | Teams | MAE | Bias | Within1Sigma |
| --- | --- | --- | --- | --- |
| 13–16 (underdogs) | 18 | 0.227 | -0.079 | 1.000 |
| 1–4 (favorites) | 16 | 1.234 | 0.839 | 0.812 |
| 5–8 (mid-high) | 16 | 0.958 | -0.771 | 0.812 |
| 9–12 (mid-low) | 18 | 0.796 | -0.333 | 0.778 |

## Biggest Upsets (Actual >> Predicted)

| Team | Seed | Predicted | StdDev | Actual | ZScore |
| --- | --- | --- | --- | --- | --- |
| Houston | 1 | 1.167 | 1.030 | 5 | 3.722 |
| Florida | 1 | 1.917 | 1.443 | 6 | 2.829 |
| Colorado State | 12 | -0.167 | 0.577 | 1 | 2.021 |
| McNeese | 12 | -0.083 | 0.669 | 1 | 1.620 |
| New Mexico | 10 | 0.167 | 0.577 | 1 | 1.443 |

## Biggest Busts (Actual << Predicted)

| Team | Seed | Predicted | StdDev | Actual | ZScore |
| --- | --- | --- | --- | --- | --- |
| Kansas | 7 | 2.583 | 1.730 | 0 | -1.493 |
| North Carolina | 11 | 2.583 | 1.881 | 0 | -1.373 |
| Clemson | 5 | 2.083 | 1.621 | 0 | -1.285 |
| Louisville | 8 | 2.167 | 1.992 | 0 | -1.087 |
| Gonzaga | 8 | 2.167 | 1.193 | 1 | -0.978 |

## Full Team Breakdown

| Team | Seed | Region | Predicted | StdDev | Actual | Error | ZScore | WithinOneSigma |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Florida | 1 | West | 1.917 | 1.443 | 6 | 4.083 | 2.829 | ✗ |
| Houston | 1 | Midwest | 1.167 | 1.030 | 5 | 3.833 | 3.722 | ✗ |
| North Carolina | 11 | South | 2.583 | 1.881 | 0 | -2.583 | -1.373 | ✗ |
| Kansas | 7 | West | 2.583 | 1.730 | 0 | -2.583 | -1.493 | ✗ |
| Louisville | 8 | South | 2.167 | 1.992 | 0 | -2.167 | -1.087 | ✗ |
| Clemson | 5 | Midwest | 2.083 | 1.621 | 0 | -2.083 | -1.285 | ✗ |
| Auburn | 1 | South | 2.083 | 1.505 | 4 | 1.917 | 1.274 | ✗ |
| UConn | 8 | West | 2.417 | 2.778 | 1 | -1.417 | -0.510 | ✓ |
| Texas Tech | 3 | West | 1.750 | 1.865 | 3 | 1.250 | 0.670 | ✓ |
| Alabama | 2 | East | 1.750 | 1.485 | 3 | 1.250 | 0.842 | ✓ |
| Duke | 1 | East | 2.750 | 1.960 | 4 | 1.250 | 0.638 | ✓ |
| Colorado State | 12 | West | -0.167 | 0.577 | 1 | 1.167 | 2.021 | ✗ |
| Gonzaga | 8 | Midwest | 2.167 | 1.193 | 1 | -1.167 | -0.978 | ✓ |
| Xavier | 11 | Midwest | 1.083 | 1.165 | 0 | -1.083 | -0.930 | ✓ |
| McNeese | 12 | Midwest | -0.083 | 0.669 | 1 | 1.083 | 1.620 | ✗ |
| Missouri | 6 | West | 1.000 | 1.348 | 0 | -1.000 | -0.742 | ✓ |
| Michigan State | 2 | South | 2.000 | 1.477 | 3 | 1.000 | 0.677 | ✓ |
| Marquette | 7 | South | 1.000 | 1.128 | 0 | -1.000 | -0.886 | ✓ |
| Tennessee | 2 | Midwest | 2.000 | 1.279 | 3 | 1.000 | 0.782 | ✓ |
| Arkansas | 10 | West | 1.000 | 1.279 | 2 | 1.000 | 0.782 | ✓ |
| VCU | 11 | East | 1.000 | 1.279 | 0 | -1.000 | -0.782 | ✓ |
| Oklahoma | 9 | West | 1.000 | 1.348 | 0 | -1.000 | -0.742 | ✓ |
| San Diego State | 11 | South | 1.000 | 1.595 | 0 | -1.000 | -0.627 | ✓ |
| Saint John's | 2 | West | 1.917 | 2.151 | 1 | -0.917 | -0.426 | ✓ |
| Mississippi State | 8 | East | 0.917 | 1.311 | 0 | -0.917 | -0.699 | ✓ |
| Georgia | 9 | Midwest | 0.917 | 1.505 | 0 | -0.917 | -0.609 | ✓ |
| New Mexico | 10 | South | 0.167 | 0.577 | 1 | 0.833 | 1.443 | ✗ |
| BYU | 6 | East | 1.167 | 1.697 | 2 | 0.833 | 0.491 | ✓ |
| Wisconsin | 3 | East | 1.750 | 1.545 | 1 | -0.750 | -0.485 | ✓ |
| Ole Miss | 6 | South | 1.333 | 1.303 | 2 | 0.667 | 0.512 | ✓ |
| Kentucky | 3 | Midwest | 2.667 | 1.923 | 2 | -0.667 | -0.347 | ✓ |
| San Francisco | 16 | South | 0.667 | 0.888 | 0 | -0.667 | -0.751 | ✓ |
| Texas | 11 | Midwest | 0.667 | 0.888 | 0 | -0.667 | -0.751 | ✓ |
| Yale | 13 | South | 0.583 | 0.793 | 0 | -0.583 | -0.736 | ✓ |
| Maryland | 4 | West | 1.417 | 1.165 | 2 | 0.583 | 0.501 | ✓ |
| Memphis | 5 | West | 0.500 | 0.798 | 0 | -0.500 | -0.627 | ✓ |
| Liberty | 12 | East | 0.500 | 1.314 | 0 | -0.500 | -0.380 | ✓ |
| Iowa State | 3 | South | 1.500 | 1.382 | 1 | -0.500 | -0.362 | ✓ |
| Vanderbilt | 10 | East | 0.500 | 1.000 | 0 | -0.500 | -0.500 | ✓ |
| Oregon | 5 | East | 1.417 | 1.165 | 1 | -0.417 | -0.358 | ✓ |
| Drake | 11 | West | 1.417 | 1.379 | 1 | -0.417 | -0.302 | ✓ |
| Purdue | 4 | Midwest | 1.583 | 1.443 | 2 | 0.417 | 0.289 | ✓ |
| Akron | 13 | East | 0.417 | 0.669 | 0 | -0.417 | -0.623 | ✓ |
| Alabama State | 16 | South | -0.417 | 0.515 | 0 | 0.417 | 0.809 | ✓ |
| Texas A&M | 4 | South | 1.333 | 1.303 | 1 | -0.333 | -0.256 | ✓ |
| American University | 16 | East | -0.250 | 0.622 | 0 | 0.250 | 0.402 | ✓ |
| Lipscomb | 14 | South | 0.250 | 0.754 | 0 | -0.250 | -0.332 | ✓ |
| SIU Edwardsville | 16 | Midwest | 0.250 | 0.622 | 0 | -0.250 | -0.402 | ✓ |
| Baylor | 9 | East | 1.250 | 1.055 | 1 | -0.250 | -0.237 | ✓ |
| Norfolk State | 16 | West | -0.250 | 0.622 | 0 | 0.250 | 0.402 | ✓ |
| Michigan | 5 | South | 2.167 | 1.642 | 2 | -0.167 | -0.102 | ✓ |
| UCLA | 7 | Midwest | 1.167 | 1.030 | 1 | -0.167 | -0.162 | ✓ |
| Saint Mary's | 7 | East | 1.167 | 1.030 | 1 | -0.167 | -0.162 | ✓ |
| UC San Diego | 12 | South | 0.167 | 0.389 | 0 | -0.167 | -0.428 | ✓ |
| Wofford | 15 | Midwest | 0.167 | 0.389 | 0 | -0.167 | -0.428 | ✓ |
| Mount St. Mary's | 16 | East | -0.167 | 0.389 | 0 | 0.167 | 0.428 | ✓ |
| High Point | 13 | Midwest | -0.167 | 0.389 | 0 | 0.167 | 0.428 | ✓ |
| Grand Canyon | 13 | West | 0.167 | 0.389 | 0 | -0.167 | -0.428 | ✓ |
| Creighton | 9 | South | 0.917 | 0.996 | 1 | 0.083 | 0.084 | ✓ |
| Robert Morris | 15 | East | 0.083 | 0.289 | 0 | -0.083 | -0.289 | ✓ |
| Omaha | 15 | West | 0.083 | 0.289 | 0 | -0.083 | -0.289 | ✓ |
| Montana | 14 | East | -0.083 | 0.289 | 0 | 0.083 | 0.289 | ✓ |
| UNC Wilmington | 14 | West | 0.083 | 0.289 | 0 | -0.083 | -0.289 | ✓ |
| Utah State | 10 | Midwest | 0.083 | 0.669 | 0 | -0.083 | -0.125 | ✓ |
| Illinois | 6 | Midwest | 1.083 | 1.311 | 1 | -0.083 | -0.064 | ✓ |
| Bryant | 15 | South | 0.000 | 0.426 | 0 | 0.000 | 0.000 | ✓ |
| Troy | 14 | Midwest | 0.000 | 0.603 | 0 | 0.000 | 0.000 | ✓ |
| Arizona | 4 | East | 2.000 | 1.477 | 2 | 0.000 | 0.000 | ✓ |
