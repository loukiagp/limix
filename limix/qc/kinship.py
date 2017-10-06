from __future__ import division

from numpy import copyto


def gower_norm(K, out=None):
    r"""Perform Gower rescaling of covariance matrix ``K``.

    Let :math:`n` be the number of rows (or columns) of ``K`` and let
    :math:`m_i` be the average of the values in the i-th column.
    Gower rescaling is defined as

    .. math::

        \mathrm K \frac{n - 1}{\text{trace}(\mathrm K) - \sum m_i}.

    It works well with `Dask`_ array as log as ``out`` is ``None``.

    Parameters
    ----------
    K : array_like
        Covariance matrix to be normalised.
    out : array_like, optional
        Result destination. Defaults to ``None``.

    Examples
    --------
    .. doctest::

        >>> from numpy import dot, mean, zeros
        >>> from numpy.random import RandomState
        >>> from limix.qc import gower_norm
        >>>
        >>> random = RandomState(0)
        >>> X = random.randn(10, 10)
        >>> K = dot(X, X.T)
        >>> Z = random.multivariate_normal(zeros(10), K, 500)
        >>> print("%.3f" % mean(Z.var(1, ddof=1)))
        9.824
        >>> Kn = gower_norm(K)
        >>> Zn = random.multivariate_normal(zeros(10), Kn, 500)
        >>> print("%.3f" % mean(Zn.var(1, ddof=1)))
        1.008

    .. _Dask: https://dask.pydata.org/
    """

    c = (K.shape[0] - 1) / (K.trace() - K.mean(0).sum())
    if out is None:
        return c * K

    copyto(out, K)
    out *= c
