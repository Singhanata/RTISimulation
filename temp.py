
import numpy as np

def test(w, l, n):
    A = np.array([[1,1],[l, -w]])
    b = np.array([n/2, 0])
    ns = np.linalg.solve(A,b)
    return ns

def te(a, **kw):
    for k,v in kw.items():
        print(kw['g'])