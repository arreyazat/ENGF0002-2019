from math import sqrt
class Complex:
    def __init__(self, r, i):
        self.r = r
        self.i = i

    def abs(self):
        return sqrt(self.r ** 2 + self.i ** 2)

    def add(self, c):
        new_c = Complex(self.r + c.r,  self.i + c.i)
        return new_c

    def multiply(self, c):
        r = self.r * c.r - self.i * c.i
        i = self.r * c.i + self.i * c.r
        return Complex(r, i)
    
    def __str__(self):
        s = str(self.r) + " + " + str(self.i) + "i"
        return s

def test_complex():
    c1 = Complex(1,1)
    assert(c1.abs() == sqrt(2))
    assert(c1.r == 1)
    assert(c1.i == 1)
    

    c2 = Complex(2,0)
    assert(c2.abs() == 2)

    c3 = c1.add(c2)
    assert(c3.r == 3)
    assert(c3.i == 1)

    assert(str(c3) == "3 + 1i")

    c4 = c2.multiply(Complex(0,1))
    assert(c4.abs() == 2)
    assert(str(c4) == "0 + 2i")
