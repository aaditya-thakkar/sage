"""
Construct Elliptic Curves as Jacobians

An elliptic curve is a genus one curve with a designated point. The
Jacobian of a genus-one curve can be defined as the set of line
bundles on the curve, and is isomorphic to the original genus-one
curve. It is also an elliptic curve with the trivial line bundle as
designated point. The utility of this construction is that we can
construct elliptic curves without having to specify which point we
take as the origin.

EXAMPLES::

    sage: R.<u,v,w> = QQ[]
    sage: Jacobian(u^3+v^3+w^3)
    Elliptic Curve defined by y^2 = x^3 - 27/4 over Rational Field
    sage: Jacobian(u^4+v^4+w^2)
    Elliptic Curve defined by y^2 = x^3 - 4*x over Rational Field

    sage: C = Curve(u^3+v^3+w^3)
    sage: Jacobian(C)
    Elliptic Curve defined by y^2 = x^3 - 27/4 over Rational Field

    sage: P2.<u,v,w> = ProjectiveSpace(2, QQ)
    sage: C = P2.subscheme(u^3+v^3+w^3)
    sage: Jacobian(C)
    Elliptic Curve defined by y^2 = x^3 - 27/4 over Rational Field

One can also define Jacobians of varieties that are not genus-one
curves. These are not implemented in this module, but we call the
relevant functionality::

    sage: R.<x> = PolynomialRing(QQ)
    sage: f = x**5 + 1184*x**3 + 1846*x**2 + 956*x + 560
    sage: C = HyperellipticCurve(f)
    sage: Jacobian(C)
    Jacobian of Hyperelliptic Curve over Rational Field defined
    by y^2 = x^5 + 1184*x^3 + 1846*x^2 + 956*x + 560

REFERENCES:

..  [WpJacobianVariety]
    http://en.wikipedia.org/wiki/Jacobian_variety
"""

##############################################################################
#       Copyright (C) 2013 Volker Braun <vbraun.name@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#  The full text of the GPL is available at:
#
#                  http://www.gnu.org/licenses/
##############################################################################

from sage.rings.all import QQ
from sage.schemes.elliptic_curves.constructor import EllipticCurve




def Jacobian(X, **kwds):
    """
    Return the Jacobian.

    INPUT:

    - ``X`` -- polynomial, algebraic variety, or anything else that
      has a Jacobian elliptic curve.

    - ``kwds`` -- optional keyword arguments.

    The input ``X`` can be one of the following:

    * A polynomial, see :func:`Jacobian_of_equation` for details.

    * A curve, see :func:`Jacobian_of_curve` for details.

    EXAMPLES::

        sage: R.<u,v,w> = QQ[]
        sage: Jacobian(u^3+v^3+w^3)
        Elliptic Curve defined by y^2 = x^3 - 27/4 over Rational Field

        sage: C = Curve(u^3+v^3+w^3)
        sage: Jacobian(C)
        Elliptic Curve defined by y^2 = x^3 - 27/4 over Rational Field

        sage: P2.<u,v,w> = ProjectiveSpace(2, QQ)
        sage: C = P2.subscheme(u^3+v^3+w^3)
        sage: Jacobian(C)
        Elliptic Curve defined by y^2 = x^3 - 27/4 over Rational Field

        sage: Jacobian(C, morphism=True)
        Scheme morphism:
          From: Closed subscheme of Projective Space of dimension 2 over Rational Field defined by:
          u^3 + v^3 + w^3
          To:   Elliptic Curve defined by y^2 = x^3 - 27/4 over Rational Field
          Defn: Defined on coordinates by sending (u : v : w) to
                (u*v^7*w + u*v^4*w^4 + u*v*w^7 :
                 v^9 + 3/2*v^6*w^3 - 3/2*v^3*w^6 - w^9 :
                 -v^6*w^3 - v^3*w^6)
    """
    try:
        return X.jacobian(**kwds)
    except AttributeError:
        pass

    morphism = kwds.pop('morphism', False)
    from sage.rings.all import is_MPolynomial
    if is_MPolynomial(X):
        if morphism:
            from sage.schemes.plane_curves.constructor import Curve
            return Jacobian_of_equation(X, curve=Curve(X), **kwds)
        else:
            return Jacobian_of_equation(X, **kwds)

    from sage.schemes.all import is_Scheme
    if is_Scheme(X) and X.dimension() == 1:
        return Jacobian_of_curve(X, morphism=morphism, **kwds)


def Jacobian_of_curve(curve, morphism=False):
    """
    Return the Jacobian of a genus-one curve

    INPUT:

    - ``curve`` -- a one-dimensional algebraic variety of genus one.

    OUTPUT:

    Its Jacobian elliptic curve.

    EXAMPLES::

        sage: R.<u,v,w> = QQ[]
        sage: C = Curve(u^3+v^3+w^3)
        sage: Jacobian(C)
        Elliptic Curve defined by y^2 = x^3 - 27/4 over Rational Field
    """
    eqn = None
    try:
        eqn = curve.defining_polynomial()
    except AttributeError:
        pass
    if len(curve.defining_polynomials()) == 1:
        eqn = curve.defining_polynomials()[0]
    if eqn is not None:
        if morphism:
            return Jacobian_of_equation(eqn, curve=curve)
        else:
            return Jacobian_of_equation(eqn)
    raise NotImplementedError('Jacobian for this curve is not implemented')


def Jacobian_of_equation(polynomial, variables=None, curve=None):
    r"""
    Construct the Jacobian of a genus-one curve given by a polynomial.

    INPUT:

    - ``F`` -- a polynomial defining a plane curve of genus one. May
      be homogeneous or inhomogeneous.

    - ``variables`` -- list of two or three variables or ``None``
      (default). The inhomogeneous or homogeneous coordinates. By
      default, all variables in the polynomial are used.

    - ``curve`` -- the genus-one curve defined by ``polynomial`` or #
      ``None`` (default). If specified, suitable morphism from the
      jacobian elliptic curve to the curve is returned.

    OUTPUT:

    An elliptic curve in short Weierstrass form isomorphic to the
    curve ``polynomial=0``. If the optional argument ``curve`` is
    specified, a rational multicover from the Jacobian elliptic curve
    to the genus-one curve is returned.

    EXAMPLES::

        sage: R.<a,b,c> = QQ[]
        sage: f = a^3+b^3+60*c^3
        sage: Jacobian(f)
        Elliptic Curve defined by y^2 = x^3 - 24300 over Rational Field
        sage: Jacobian(f.subs(c=1))
        Elliptic Curve defined by y^2 = x^3 - 24300 over Rational Field

    If we specify the domain curve the birational covering is returned::

        sage: h = Jacobian(f, curve=Curve(f));  h
        Scheme morphism:
          From: Projective Curve over Rational Field defined by a^3 + b^3 + 60*c^3
          To:   Elliptic Curve defined by y^2 = x^3 - 24300 over Rational Field
          Defn: Defined on coordinates by sending (a : b : c) to
                (216000*a*b^7*c + 12960000*a*b^4*c^4 + 777600000*a*b*c^7 :
                 216000*b^9 + 19440000*b^6*c^3 - 1166400000*b^3*c^6 - 46656000000*c^9 :
                 -216000*b^6*c^3 - 12960000*b^3*c^6)
        sage: h([1,-1,0])
        (0 : 1 : 0)

    Plugging in the polynomials defining `h` allows us to verify that
    it is indeed a rational morphism to the elliptic curve::

        sage: E = h.codomain()
        sage: E.defining_polynomial()(h.defining_polynomials()).factor()
        (-10077696000000000) * c^3 * b^3 * (a^3 + b^3 + 60*c^3) * (b^6 + 60*b^3*c^3 + 3600*c^6)^3

    By specifying the variables, we can also construct an elliptic
    curve over a polynomial ring::

        sage: R.<u,v,t> = QQ[]
        sage: Jacobian(u^3+v^3+t, variables=[u,v])
        Elliptic Curve defined by y^2 = x^3 + (-27/4*t^2) over
        Multivariate Polynomial Ring in u, v, t over Rational Field

    TESTS::

        sage: from sage.schemes.elliptic_curves.jacobian import Jacobian_of_equation
        sage: Jacobian_of_equation(f, variables=[a,b,c])
        Elliptic Curve defined by y^2 = x^3 - 24300 over Rational Field
    """
    from sage.schemes.toric.weierstrass import WeierstrassForm
    f, g = WeierstrassForm(polynomial, variables=variables)
    try:
        K = polynomial.base_ring()
        f = K(f)
        g = K(g)
    except (TypeError, ValueError):
        pass
    E = EllipticCurve([f, g])
    if curve is None:
        return E
    X, Y, Z = WeierstrassForm(polynomial, variables=variables, transformation=True)
    from sage.schemes.elliptic_curves.weierstrass_transform import WeierstrassTransformation
    return WeierstrassTransformation(curve, E, [X*Z, Y, Z**3], 1)

def Jacobian_magma_equation(F):
    r"""
    Construct the Jacobian of a genus-one plane curve given by a polynomial.

    .. note::

        This function only has historical interest and is useful for
        doctesting. Use :func:`Jacobian` for any real work.

    .. note::

       USES MAGMA - This function will not work on computers that
       do not have Magma installed.

    INPUT:

    - ``F`` -- a polynomial defining a plane curve of genus one.

    OUTPUT:

    An elliptic curve in short Weierstrass form isomorphic to the
    curve `F=0`.

    EXAMPLES::

        sage: R.<x,y,z> = QQ[]
        sage: f = x^3+y^3+60*z^3
        sage: from sage.schemes.elliptic_curves.jacobian import Jacobian_magma_equation
        sage: E = Jacobian_magma_equation(f)  # optional - magma
        sage: E                # optional - magma
        Elliptic Curve defined by y^2  = x^3 - 24300 over Rational Field
        sage: E.conductor()    # optional - magma
        24300

    TESTS::

        sage: Jacobian(f)
        Elliptic Curve defined by y^2 = x^3 - 24300 over Rational Field
    """
    from sage.interfaces.all import magma
    cmd = "P<%s,%s,%s> := ProjectivePlane(RationalField());"%SR(F).variables()
    magma.eval(cmd)
    cmd = 'aInvariants(MinimalModel(EllipticCurve(Curve(Scheme(P, %s)),P!%s)));'%(F, P)
    s = magma.eval(cmd)
    return EllipticCurve(rings.RationalField(), eval(s))


def Jacobian_magma_from_plane_curve(C, P):
    r"""
    Elliptic curve from a smooth plane cubic with a rational point.

    .. note::

        This function only has historical interest and is useful for
        doctesting. Use :func:`Jacobian` for any real work.

    INPUT:

    - ``C`` -- a plane curve of genus one.

    - ``P`` -- a 3-tuple `(x,y,z)` defining a projective point on the
      curve ``C``.

    OUTPUT:

    (elliptic curve) An elliptic curve (in minimal Weierstrass form)
    isomorphic to ``C``.

    .. note::

       USES MAGMA - This function will not work on computers that
       do not have magma installed.

    EXAMPLES:

    First we check that the Fermat cubic is isomorphic to the curve
    with Cremona label '27a1'::

        sage: x,y,z=PolynomialRing(QQ,3,'xyz').gens() # optional - magma
        sage: C=Curve(x^3+y^3+z^3) # optional - magma
        sage: P=C(1,-1,0) # optional - magma
        sage: E=EllipticCurve_from_plane_curve(C,P) # optional - magma
        sage: E # optional - magma
        Elliptic Curve defined by y^2 + y = x^3 - 7 over Rational Field
        sage: E.label() # optional - magma
        '27a1'

    Now we try a quartic example::

        sage: u,v,w=PolynomialRing(QQ,3,'uvw').gens() # optional - magma
        sage: C=Curve(u^4+u^2*v^2-w^4) # optional - magma
        sage: P=C(1,0,1) # optional - magma
        sage: E=EllipticCurve_from_plane_curve(C,P) # optional - magma
        sage: E # optional - magma
        Elliptic Curve defined by y^2  = x^3 + 4*x over Rational Field
        sage: E.label() # optional - magma
        '32a1'
    """
    if C.genus()!=1:
        raise TypeError("The curve C must have genus 1")
    elif P.parent()!=C.point_set(C.base_ring()):
        raise TypeError("The point P must be on the curve C")
    dp=C.defining_polynomial()
    x,y,z = dp.parent().variable_names()
    cmd = "PR<%s,%s,%s>:=ProjectivePlane(RationalField());"%(x,y,z)
    from sage.interfaces.all import magma
    magma.eval(cmd)
    cmd = 'CC:=Curve(PR, %s);'%(dp)
    magma.eval(cmd)
    cmd='aInvariants(MinimalModel(EllipticCurve(CC,CC!%s)));'%([P[0],P[1],P[2]])
    s=magma.eval(cmd)
    return EllipticCurve(rings.RationalField(), eval(s))
