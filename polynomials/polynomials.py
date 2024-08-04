from numbers import Number, Integral


class Polynomial:

    def __init__(self, coefs):
        self.coefficients = coefs

    def degree(self):
        return len(self.coefficients) - 1

    def __str__(self):
        coefs = self.coefficients
        terms = []

        if coefs[0]:
            terms.append(str(coefs[0]))
        if self.degree() and coefs[1]:
            terms.append(f"{'' if coefs[1] == 1 else coefs[1]}x")

        terms += [f"{'' if c == 1 else c}x^{d}"
                  for d, c in enumerate(coefs[2:], start=2) if c]

        return " + ".join(reversed(terms)) or "0"

    def __repr__(self):
        return self.__class__.__name__ + "(" + repr(self.coefficients) + ")"

    def __eq__(self, other):

        return isinstance(other, Polynomial) and\
             self.coefficients == other.coefficients

    def __add__(self, other):

        if isinstance(other, Polynomial):
            common = min(self.degree(), other.degree()) + 1
            coefs = tuple(a + b for a, b in zip(self.coefficients,
                                                other.coefficients))
            coefs += self.coefficients[common:] + other.coefficients[common:]

            return Polynomial(coefs)

        elif isinstance(other, Number):
            return Polynomial((self.coefficients[0] + other,)
                              + self.coefficients[1:])
            
        else:
            return NotImplemented

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        
        if isinstance(other, Polynomial):
            coeff = tuple(-val for val in other.coefficients)
            temp = Polynomial(coeff)
        elif isinstance(other, Number):
            temp = -other
        else:
            return NotImplemented
            
        return self + temp
    
    def __rsub__(self, other):
        return self - self - self + other
    
    def __mul__(self, other):
        if isinstance(other, Number):
            temp = Polynomial(tuple([other * val for val in self.coefficients]))
            return temp
        elif isinstance(other, Polynomial):
            # new degree is sum of degrees
            deg_self = self.degree()
            deg_other = other.degree()
            deg = deg_self + deg_other
            # append 0s to tuples till they have deg + 1 terms
            a = self.coefficients + (0,)*(deg - deg_self+1)
            b = other.coefficients + (0,)*(deg - deg_other+1)
            # coefficient is the cauchy product
            coeff = [0 for i in range(deg+1)]
            for n in range(deg+1):
                for i in range(n+1):
                    coeff[n] += a[i]*b[n-i]
            coeff = tuple(coeff)
            return Polynomial(coeff)
        else:
            return NotImplemented
    
    def __rmul__(self, other):
        return self * other
    
    def __pow__(self, n):
        new_poly = Polynomial(self.coefficients)
        if isinstance(n, Integral):
            if n >0:
                for i in range(n-1):
                    new_poly *= self
                return new_poly
        return NotImplemented
    
    def __call__(self, val):
        if isinstance(val, Number):
            return sum([coeff * (val**i) for i, coeff in enumerate(self.coefficients)])