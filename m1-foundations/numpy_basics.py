"""Six ways to create NumPy arrays, printing each one's shape and dtype.

    uv run python m1-foundations/numpy_basics.py
"""

import numpy as np
from numpy.typing import NDArray


def show(name: str, arr: NDArray[np.generic]) -> None:
    """Print an array with its shape, dtype and number of dimensions."""
    print(f"\n--- {name}")
    print(f"shape={arr.shape} dtype={arr.dtype} ndim={arr.ndim}")
    print(arr)


def main() -> None:
    np.set_printoptions(precision=3, suppress=True)  # tidier float output

    # 1. np.array: from Python lists. The dtype is inferred from the values.
    show("np.array([1, 2, 3])", np.array([1, 2, 3]))  # int64
    show("np.array([1, 2, 3.5])", np.array([1, 2, 3.5]))  # one float -> all float64
    show("np.array(2x3 nested list)", np.array([[1, 2, 3], [4, 5, 6]]))
    show("np.array(..., dtype=np.float32)", np.array([1, 2, 3], dtype=np.float32))

    # 2. np.zeros / 3. np.ones: filled arrays, float64 by default. Shape is an int or a tuple.
    show("np.zeros(4)", np.zeros(4))
    show("np.zeros((2, 3))", np.zeros((2, 3)))
    show("np.ones((3, 2), dtype=int)", np.ones((3, 2), dtype=int))

    # 4. np.arange(start, stop, step): like range(); stop is EXCLUDED.
    show("np.arange(5)", np.arange(5))
    show("np.arange(2, 10, 2)", np.arange(2, 10, 2))
    # With float steps, rounding makes the element count hard to predict, so use linspace.
    show("np.arange(0, 1, 0.25)", np.arange(0, 1, 0.25))

    # 5. np.linspace(start, stop, num): num evenly spaced points; stop is INCLUDED.
    show("np.linspace(0, 1, 5)", np.linspace(0, 1, 5))
    show("np.linspace(0, 1, 5, endpoint=False)", np.linspace(0, 1, 5, endpoint=False))

    # 6. Random numbers: create a Generator with a seed, so every run gives the same values.
    rng = np.random.default_rng(42)
    samples = rng.normal(loc=0.0, scale=1.0, size=(3, 4))  # mean 0, std 1, 3x4
    show("rng.normal(0, 1, size=(3, 4))", samples)

    big = np.random.default_rng(42).normal(loc=10.0, scale=2.0, size=10_000)
    print(f"\n10,000 draws of normal(10, 2): mean={big.mean():.3f} std={big.std():.3f}")

    # Same seed -> same numbers; that's what makes experiments reproducible.
    a = np.random.default_rng(42).normal(size=3)
    b = np.random.default_rng(42).normal(size=3)
    print(f"Same seed gives same values: {np.array_equal(a, b)}  {a}")

    # Bonus: reshape works on any of the above, as long as the element count matches.
    show("np.arange(12).reshape(3, 4)", np.arange(12).reshape(3, 4))


if __name__ == "__main__":
    main()
