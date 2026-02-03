# Adding a New Math Function — ChemWorkBench v2.2
LLM‑friendly commentary included throughout.

This guide explains how to safely add new spectral math functions to the
universal math layer. The goal is to make extensions easy for both human
developers and LLMs.

---

## Design Principles

### 1. **Pure Functions**
- No mutation of inputs  
- No global state  
- No caching  
- No side effects  

### 2. **Technique‑Agnostic**
Math functions must not assume:
- UV‑Vis  
- IR  
- MS  
- NMR  
- Raman  

They operate purely on `x` and `y`.

### 3. **Vectorized Where Possible**
Use NumPy operations instead of Python loops.

### 4. **Consistent Signatures**
Every function should follow:

`
def func_name(
    x: Sequence[float],
    y: Sequence[float],
    **kwargs,
) -> Tuple[np.ndarray, np.ndarray]:
5. Return New Arrays
Never modify x or y in place.

Steps to Add a New Math Function
1. Implement the function in math_spectral.py
Example:
def derivative(x, y, order=1):
    x_arr = np.asarray(x)
    y_arr = np.asarray(y)
    dy = np.gradient(y_arr, x_arr)
    return x_arr, dy


2. Add it to a unified wrapper (optional)
If the function belongs to a family (e.g., smoothing):
def smooth(...):
    if method == "derivative":
        return derivative(x, y, **kwargs)


3. Add LLM‑friendly docstrings
Explain:
- purpose
- inputs
- outputs
- edge cases
4. Add tests
Tests should verify:
- shape consistency
- no mutation
- correct numerical behavior
5. Update processor configs (optional)
If processors should expose the new function, add a config field.

Example: Adding a Derivative Function
Step 1 — Implement
def derivative(x, y, order=1):
    x_arr = np.asarray(x)
    y_arr = np.asarray(y)
    dy = np.gradient(y_arr, x_arr)
    return x_arr, dy


Step 2 — Add to wrapper
elif method == "derivative":
    return derivative(x, y, **kwargs)


Step 3 — Add config
derivative_order: int = 1


Step 4 — Add block in processor
if cfg.derivative_enabled:
    x, y = derivative(x, y, order=cfg.derivative_order)



Summary
Adding new math functions is safe, simple, and deterministic.
The math layer is designed for LLM‑driven expansion, and this guide ensures that new operations remain consistent with the v2.2 architecture.
