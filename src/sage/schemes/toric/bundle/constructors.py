r"""
Construct toric vector bundles.

A toric vector bundle (on a toric variety) is a vector bundle that is
equivarint with respect to the algebraic torus action.
"""


#*****************************************************************************
#       Copyright (C) 2011 Volker Braun <vbraun.name@gmail.com>
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of 
#  the License, or (at your option) any later version.  
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from sage.schemes.toric.variety import is_ToricVariety
from sage.modules.filtered_vector_space import FilteredVectorSpace

def TangentBundle(X):
    r"""
    Construct the tangent bundle of a toric variety.

    EXAMPLES:

        sage: toric_varieties.dP7().tangent_bundle()
        Rank 2 bundle on 2-d CPR-Fano toric variety covered by 5 affine patches.
    """
    assert is_ToricVariety(X)
    base_ring = X.base_ring()
    fan = X.fan()
    filtration = [ [[1,[i]], [2,[]]] for i in range(0,fan.nrays()) ]
    import klyachko
    return klyachko.Bundle_from_rays_filtrations(X, fan.rays(), filtration, base_field=base_ring)
    


def CotangentBundle(X):
    assert is_ToricVariety(X)
    raise NotImplementedError

def TrivialBundle(X, r):
    r"""
    Return the trivial bundle of rank ``r``.

    EXAMPLES::

        sage: I3 = TrivialBundle(toric_varieties.P2(), 3);  I3
        Rank 3 bundle on 2-d CPR-Fano toric variety covered by 3 affine patches.
        sage: I3.cohomology(m=(0,0), dim=True)
        (3, 0, 0)
    """
    assert is_ToricVariety(X)
    from sage.modules.free_module import VectorSpace
    base_ring = X.base_ring()
    filtration = [ FilteredVectorSpace(r, 0, base_field=base_ring) ] * X.fan().nrays()
    import klyachko
    return klyachko.Bundle_from_filtered_vector_spaces(X, filtration)


def LineBundle(X, D):
    """
    Construct the rank-1 bundle `O(D)`.
    
    EXAMPLES::

        sage: X = toric_varieties.dP8()
        sage: D = X.divisor(0)
        sage: O_D = LineBundle(X, D)
        sage: O_D.cohomology(dim=True, m=(0,0))
    """
    assert is_ToricVariety(X)
    from sage.modules.free_module import VectorSpace
    base_ring = X.base_ring()
    filtration = [ FilteredVectorSpace(1, D.function_value(i), base_field=base_ring) 
                   for i in range(0, X.fan().nrays()) ]
    import klyachko
    return klyachko.Bundle_from_filtered_vector_spaces(X, filtration)
    
    
        
