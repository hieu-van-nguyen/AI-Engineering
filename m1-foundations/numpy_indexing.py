"""Inspecting, reshaping and indexing NumPy arrays, plus a small exercise.

    uv run python m1-foundations/numpy_indexing.py
"""

import numpy as np
from numpy.typing import NDArray


def show(name: str, arr: NDArray[np.generic]) -> None:
    """Print an array with its shape and dtype."""
    print(f"\n--- {name}   shape={arr.shape} dtype={arr.dtype}")
    print(arr)


def inspect() -> None:
    print("=== 1. Inspect: shape, dtype, ndim ===")
    a = np.arange(12)
    m = np.ones((3, 4), dtype=np.float32)
    examples: list[tuple[str, NDArray[np.generic]]] = [
        ("np.arange(12)", a),
        ("np.ones((3, 4), float32)", m),
    ]
    for name, arr in examples:
        print(f"{name:<26} shape={arr.shape} dtype={arr.dtype} ndim={arr.ndim} "
              f"size={arr.size} itemsize={arr.itemsize} bytes")


def reshape_and_transpose() -> None:
    print("\n=== 2. reshape and .T ===")
    a = np.arange(12)
    show("a.reshape(3, 4)", a.reshape(3, 4))
    show("a.reshape(2, -1)   (-1 = work it out: 12 / 2 = 6)", a.reshape(2, -1))
    show("a.reshape(3, 4).T   (rows <-> columns)", a.reshape(3, 4).T)
    try:
        a.reshape(5, 2)
    except ValueError as e:
        print(f"\na.reshape(5, 2) -> ValueError: {e}")

    # reshape and .T return views when they can: they share memory with `a`.
    v = a.reshape(3, 4)
    v[0, 0] = 99
    print(f"After v[0, 0] = 99 on the reshaped view, a[0] = {a[0]}  (same memory)")


def slicing() -> None:
    print("\n=== 3. Slicing: arr[rows, cols], each part is start:stop:step ===")
    m = np.arange(20).reshape(4, 5)
    show("m", m)
    show("m[1]        row 1", m[1])
    show("m[:, 2]     column 2 (1-D)", m[:, 2])
    show("m[:, 2:3]   column 2, kept 2-D", m[:, 2:3])
    show("m[1:3, 1:4] rows 1-2, cols 1-3", m[1:3, 1:4])
    show("m[::2, ::-1] every other row, columns reversed", m[::2, ::-1])

    # Slices are views: writing to one changes the original. Use .copy() to avoid that.
    s = m[0, :2]
    s[:] = -1
    print(f"\nAfter s[:] = -1 on slice m[0, :2], m[0] = {m[0]}  (slice is a view)")


def boolean_masks() -> None:
    print("\n=== 4. Boolean masks ===")
    x = np.array([3, -1, 4, -1, 5, -9, 2, 6])
    mask = x > 0
    print(f"x            = {x}")
    print(f"mask = x > 0 = {mask}")
    print(f"x[mask]      = {x[mask]}   (always a 1-D copy)")
    print(f"x[(x > 0) & (x % 2 == 0)] = {x[(x > 0) & (x % 2 == 0)]}   (use & | ~, with parentheses)")
    print(f"count of positives = {mask.sum()}, np.where(x > 0)[0] = {np.where(x > 0)[0]}")
    clipped = np.where(x > 0, x, 0)  # keep positives, replace the rest with 0
    print(f"np.where(x > 0, x, 0) = {clipped}")


def fancy_indexing() -> None:
    print("\n=== 5. Fancy indexing (index with a list/array of positions) ===")
    m = np.arange(20).reshape(4, 5)
    show("m", m)
    show("m[[0, 2, 3]]     rows 0, 2, 3", m[[0, 2, 3]])
    show("m[:, [4, 0]]     columns 4 then 0", m[:, [4, 0]])
    show("m[[0, 1, 3], [1, 2, 4]]  pairs (0,1) (1,2) (3,4)", m[[0, 1, 3], [1, 2, 4]])
    show("m[np.ix_([0, 3], [1, 4])]  rows x cols grid", m[np.ix_([0, 3], [1, 4])])
    # Unlike slices, fancy indexing returns a copy.


def exercise() -> None:
    print("\n=== Exercise: (6, 4) random array ===")
    rng = np.random.default_rng(42)
    arr = rng.normal(size=(6, 4))
    show("arr", arr)

    second_col = arr[:, 1]  # index 1 = the 2nd column
    last_two_rows = arr[-2:]  # same as arr[-2:, :]
    positives = arr[arr > 0]

    show("2nd column: arr[:, 1]", second_col)
    show("last two rows: arr[-2:]", last_two_rows)
    show("values > 0: arr[arr > 0]", positives)

    # Quick checks that the answers are right.
    assert second_col.shape == (6,)
    assert last_two_rows.shape == (2, 4)
    assert (positives > 0).all() and positives.size == (arr > 0).sum()
    print(f"\n{positives.size} of {arr.size} values are > 0; all checks passed.")


def main() -> None:
    np.set_printoptions(precision=3, suppress=True)
    inspect()
    reshape_and_transpose()
    slicing()
    boolean_masks()
    fancy_indexing()
    exercise()


if __name__ == "__main__":
    main()
