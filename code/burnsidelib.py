from sage.rings.quotient_ring import QuotientRing_generic
from sage.rings.quotient_ring_element import QuotientRingElement
from sage.matrix.constructor import matrix
from sage.modules.free_module_element import vector
from sage.structure.parent import Parent
from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
from sage.rings.integer_ring import ZZ


# Current does not assume that elements are stored in reduced form... they could
# arbitrary polynomials. In practice this doesn't seem to ever happen?
# If this can be guaranteed that would allow for some optimization.
class BurnsideRingElement(QuotientRingElement):
    def __init__(self, parent, rep):
        super().__init__(parent, rep)
        lift = self.lift()
        self._marks = vector(
            ZZ, (lift(*col) for col in self.parent().table_of_marks().columns())
        )
        self._coeffs = self._marks * self.parent()._tommat_inv

    def coeffs(self):
        return self._coeffs

    def marks(self):
        return self._marks

    def list(self):
        return list(self._coeffs)

    def res(self, H):
        A_G = self.parent()
        G = A_G.group()
        A_H = BurnsideRing(H)
        if H.Order() == 1:
            return self.marks()[0] * A_H.gens()[0]
        res_H = matrix(
            ZZ,
            A_G._num_cc_subgroups,
            A_H._num_cc_subgroups,
            lambda i, j: (1 if G.IsConjugate(A_G._cc_reps[i], A_H._cc_reps[j]) else 0),
        )
        marks_res_X = self.marks() * res_H
        return A_H.from_marks(marks_res_X)

    def _repr_(self):
        gen_names = self.parent().gen_names()
        return " + ".join(
            f"{c}*{gen_names[i]}" for i, c in enumerate(self._coeffs) if c != 0
        )


class BurnsideRing(QuotientRing_generic, Parent):
    Element = BurnsideRingElement

    # group must be a GAP object
    def __init__(self, group, names=None):
        self._group = group
        self._tom = group.TableOfMarks()
        self._tommat = matrix(ZZ, self._tom.MatTom())
        self._tommat_inv = self._tommat.inverse()
        self._num_cc_subgroups = self._tommat.nrows()
        self._index_of_trivial = next(
            i for i in range(self._num_cc_subgroups) if self._tommat[i, 0] == 1
        )
        self._cc_reps = [
            self._tom.RepresentativeTom(n + 1) for n in range(self._num_cc_subgroups)
        ]
        self._gen_names = [
            f"[{group.StructureDescription()}/{self._cc_reps[i].StructureDescription()}]"
            for i in range(self._num_cc_subgroups)
        ]
        base_ring = PolynomialRing(ZZ, "x", self._num_cc_subgroups)
        base_gens = base_ring.gens()
        relations = [base_gens[self._index_of_trivial] - 1]
        for i in range(self._num_cc_subgroups):
            for j in range(i, self._num_cc_subgroups):
                prod_marks = vector(
                    ZZ,
                    [
                        self._tommat[i][k] * self._tommat[j][k]
                        for k in range(self._num_cc_subgroups)
                    ],
                )
                relations.append(
                    base_gens[i] * base_gens[j]
                    - sum(
                        coeff * base_gens[k]
                        for k, coeff in enumerate(
                            vector(ZZ, prod_marks * self._tommat_inv)
                        )
                    )
                )
        super().__init__(base_ring, base_ring.ideal(relations), None)

    def gen_names(self):
        return self._gen_names

    def group(self):
        return self._group

    # Returns the table of marks as an integral matrix, as computed by GAP
    def table_of_marks(self):
        return self._tommat

    def from_vec(self, v):
        return sum(c * self.gens()[i] for i, c in enumerate(v))

    def from_marks(self, v):
        return self.from_vec(vector(ZZ, vector(v) * self._tommat_inv))

    def _repr_(self):
        return f"Burnside ring of {self._group}"

    def _repr_short(self):
        return f"A({self._group.StructureDescription()})"
