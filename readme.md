# Financial Analysis using Linear Algebra

## Overview

This project explores a simple quantitative approach to financial analysis using linear algebra.

We assume that the price of an asset is influenced by its fundamental data, and we model this relationship as **linear**.

![Example Output](./assets/AAPL.png)

*Comparison between predicted and actual prices using a linear model trained on fundamental data.*

---

## Model Assumption

We assume that the price at time $i$, denoted as $p_i$, can be expressed as a linear combination of:

* the previous price $p_{i-1}$
* a set of fundamental features $f_1, ..., f_n$

$$
p_i = w_0 \cdot p_{i-1} + w_1 \cdot f_{i,1} + \dots + w_n \cdot f_{i,n}
$$

In vector form:

$$
p_i = \vec{f_i} \cdot \vec{w}
$$

where:

$$
\vec{f_i} = \begin{bmatrix} p_{i-1} & f_{i,1} & \dots & f_{i,n} \end{bmatrix}
\quad
\vec{w} = \begin{bmatrix} w_0 \ w_1 \ \dots \ w_n \end{bmatrix}
$$

---

## Building the Linear System

By stacking multiple observations, we obtain a linear system:

$$
A \cdot \vec{w} = \vec{p}
$$

where:

$$
A =
\begin{bmatrix}
p_0 & f_{1,1} & \dots & f_{1,n} \\
p_1 & f_{2,1} & \dots & f_{2,n} \\
\vdots & \vdots & \ddots & \vdots \\
p_{k-1} & f_{k,1} & \dots & f_{k,n}
\end{bmatrix}
\quad
\vec{p} =
\begin{bmatrix}
p_1 \\
p_2 \\
\vdots \\
p_k
\end{bmatrix}
$$

To solve the system, we use a least squares approach by computing the Moore–Penrose pseudoinverse of $A$:

$$
\vec{w} = A^{+} \vec{p}
$$

This provides the best linear approximation when the system is overdetermined.

---

## Data Assumptions

* Fundamental data is available every 3–4 months
* The dataset includes BYD, NFLX, AAPL starting from 01/01/2015
* The price at index $i$ is approximated as the average price between two fundamental data releases

---

## Training Strategy

Two approaches are implemented:

### 1. Fixed Weights

* Compute weights using a fixed window of size `off`
* Use the same weights for future predictions

### 2. Rolling Weights

* Recompute weights at each step using updated data
* Allows adaptation to changing market conditions

---

## Plot Usage

```python
import matplotlib.pyplot as plt
import tickers
from plot import plot

plt.style.use("dark_background")

if __name__ == "__main__":
    plot(0, 22, tickers.AAPL)
```

---

## Data Usage

```python
from yahoo.ticker import MyTicker
import tickers

tk = MyTicker(tickers.NFLX)

start = 0
off = 20

# Fixed weights approach
expected_prices = tk.get_results(start, 38, off)

# Rolling weights approach
expected_prices_s = tk.get_coefficients_result(
    tk.get_coefficients(start, off),
    start,
    38
)
```

---

## Results

* Tested on multiple assets (AAPL, NFLX, BYD)
* Compared predicted vs actual prices
* Observed limitations of linear assumptions in volatile markets

---

## Notes

This is a simplified model and does not aim to provide accurate financial predictions.
Its purpose is to demonstrate how linear algebra can be applied to real-world data modeling problems.
