# -*- coding: utf-8 -*-

# Združljivost s Python 2
try:
    long
except NameError:
    long = int

class AbstractMatrix:
    """
    Razred z osnovnimi funkcionalnostmi za matrike.
    """

    def __init__(self, data = None, nrow = None, ncol = None,
                 byrow = None, bycol = None, sl = None, copy = True):
        """
        Konstruktor za matrike.

        Sestavi matriko iz danih podatkov.
        Manjkajoče podatke nadomesti z ničlami.

        Parametri:
        - data: podatki za matriko (seznam ali slovar seznamov ali slovarjev,
                seznam števil, slovar z dvojnimi indeksi, število, matrika
                ali None)
        - nrow: zahtevano število vrstic
        - ncol: zahtevano število stolpcev
        - byrow: podatki so podani po vrsticah
        - bycol: podatki so podani po stolpcih
        - sl: par rezin, ki naj se uporabi za gradnjo podmatrike
        - copy: ali naj se ustvari kopija osnovnih podatkov
        """
        if byrow is None:
            byrow = not bycol
        if bycol is None:
            bycol = not byrow
        assert byrow ^ bycol, \
               "Natanko en od parametrov byrow in bycol mora biti resničen!"
        if nrow is not None:
            assert nrow >= 0, "Število vrstic mora biti nenegativno!"
        if ncol is not None:
            assert ncol >= 0, "Število stolpcev mora biti nenegativno!"
        if isinstance(data, dict):
            if len(data) == 0:
                self._init_data(nrow, ncol, sl = sl, copy = copy)
            elif sl is None:
                keys = data.keys()
                if all(isinstance(k, tuple) and len(k) == 2 for k in keys):
                    assert min(i for i, j in keys) >= 0 and \
                           min(j for i, j in keys) >= 0, \
                           "Negativni indeksi niso dovoljeni!"
                    if nrow is None:
                        nrow = 1 + max(i for i, j in keys)
                    if ncol is None:
                        ncol = 1 + max(j for i, j in keys)
                    self._init_empty(nrow, ncol)
                    for i, j in keys:
                        self._data[i][j] = data[i, j]
                else:
                    assert min(keys) >= 0 and \
                           min(min(r.keys()) for r in data.values() if
                                   isinstance(r, dict) and len(r) > 0) >= 0, \
                           "Negativni indeksi niso dovoljeni!"
                    if byrow:
                        if nrow is None:
                            nrow = 1 + max(keys)
                        if ncol is None:
                            ncol = max(1 + max(r.keys())
                                       if isinstance(r, dict) and len(r) > 0
                                       else len(r) for r in data.values())
                        self._init_empty(nrow, ncol)
                        self._fill_rows(data.items(), ncol)
                    else:
                        if ncol is None:
                            ncol = 1 + max(keys)
                        if nrow is None:
                            nrow = max((1 + max(c.keys()))
                                       if isinstance(c, dict) and len(c) > 0
                                       else len(c) for c in data.values())
                        self._init_empty(nrow, ncol)
                        self._fill_cols(data.items(), nrow)
            else:
                data = self.__class__(data, nrow = nrow, ncol = ncol,
                                      byrow = byrow, copy = False)
        elif isinstance(data, (list, tuple)):
            if byrow:
                if len(data) == 0:
                    if nrow is not None:
                        assert nrow == 0, "Število vrstic se ne ujema!"
                    self._init_data(nrow, ncol, sl = sl, copy = copy)
                elif sl is None:
                    if all(isinstance(r, (list, tuple, dict)) for r in data):
                        if nrow is None:
                            nrow = len(data)
                        else:
                            assert nrow == len(data), \
                                   "Število vrstic se ne ujema!"
                        if ncol is None:
                            ncol = max((1 + max(r.keys()))
                                       if isinstance(r, dict) and len(r) > 0
                                       else len(r) for r in data)
                        assert all(min(r.keys()) >= 0 for r in data
                                   if isinstance(r, dict) and len(r) > 0), \
                               "Negativni indeksi niso dovoljeni!"
                        self._init_empty(nrow, ncol)
                        self._fill_rows(enumerate(data), ncol)
                    else:
                        if ncol is None:
                            if nrow is None:
                                nrow = 1
                            ncol = len(data) // nrow
                        elif nrow is None:
                            nrow = len(data) // ncol
                        assert len(data) == nrow * ncol, \
                               "Napačna dolžina podatkov!"
                        self._init_empty(nrow, ncol)
                        for h, x in enumerate(data):
                            self._data[h // ncol][h % ncol] = x
                else:
                    data = self.__class__(data, nrow = nrow, ncol = ncol,
                                          byrow = byrow, copy = False)
            else:
                if len(data) == 0:
                    if ncol is not None:
                        assert ncol == 0, "Število stolpcev se ne ujema!"
                    self._init_data(nrow, ncol, sl = sl, copy = copy)
                elif sl is None:
                    if all(isinstance(c, (list, tuple, dict)) for c in data):
                        if ncol is None:
                            ncol = len(data)
                        else:
                            assert ncol == len(data), \
                                   "Število stolpcev se ne ujema!"
                        if nrow is None:
                            nrow = max((1 + max(c.keys()))
                                       if isinstance(c, dict) and len(c) > 0
                                       else len(c) for c in data)
                        assert all(min(c.keys()) >= 0 for c in data
                                   if isinstance(c, dict) and len(c) > 0), \
                               "Negativni indeksi niso dovoljeni!"
                        self._init_empty(nrow, ncol)
                        self._fill_cols(enumerate(data), nrow)
                    else:
                        if nrow is None:
                            if ncol is None:
                                ncol = 1
                            nrow = len(data) // ncol
                        elif ncol is None:
                            ncol = len(data) // nrow
                        assert len(data) == nrow * ncol, \
                               "Napačna dolžina podatkov!"
                        self._init_empty(nrow, ncol)
                        for h, x in enumerate(data):
                            self._data[h % nrow][h // nrow] = x
                else:
                    data = self.__class__(data, nrow = nrow, ncol = ncol,
                                          byrow = byrow, copy = False)
        elif not isinstance(data, AbstractMatrix):
            self._init_data(nrow, ncol, val = data, sl = sl, copy = copy)
        if isinstance(data, AbstractMatrix):
            nrow, ncol = data._check_dims(nrow, ncol)
            if sl is not None:
                sr, sc = sl
                sr = normalize_slice(sr, nrow)
                sc = normalize_slice(sc, ncol)
            if copy:
                if sl is None:
                    sr = slice(0, nrow, 1)
                    sc = slice(0, ncol, 1)
                self._init_empty(slicelen(sr), slicelen(sc))
                for i, r in enumerate(data._data[data._rslice][sr]):
                    self._data[i][:] = r[data._cslice][sc]
            else:
                if sl is None:
                    self._rslice = data._rslice
                    self._cslice = data._cslice
                else:
                    rstop = data._rslice.start + data._rslice.step * \
                            (-1 if sr.stop is None else sr.stop)
                    cstop = data._cslice.start + data._cslice.step * \
                            (-1 if sc.stop is None else sc.stop)
                    if rstop < 0:
                        rstop = None
                    if cstop < 0:
                        cstop = None
                    self._rslice = slice(data._rslice.start + 
                                         data._rslice.step * sr.start,
                                         rstop, data._rslice.step * sr.step)
                    self._cslice = slice(data._cslice.start + 
                                         data._cslice.step * sc.start,
                                         cstop, data._cslice.step * sc.step)
                self._data = data._data
        self._nrow = slicelen(self._rslice)
        self._ncol = slicelen(self._cslice)

    def _init_data(self, nrow, ncol, val = None, sl = None, copy = True):
        """
        Inicializacija podatkov.
        """
        n = 0 if val is None else 1
        if sl is None:
            if nrow is None:
                nrow = n
            if ncol is None:
                ncol = n
            self._init_empty(nrow, ncol, val = val)
        else:
            sr, sc = sl
            if nrow is None:
                sr = normalize_slice(sr, steps = n)
                nrow = slicemax(sr)
            else:
                sr = normalize_slice(sr, nrow)
                assert sr.end >= nrow, "Število vrstic se ne ujema!"
            if ncol is None:
                sc = normalize_slice(sc, steps = n)
                ncol = slicemax(sc)
            else:
                sc = normalize_slice(sc, ncol)
                assert sc.end >= ncol, "Število stolpcev se ne ujema!"
            if copy:
                self._init_empty(slicelen(nrow), slicelen(ncol), val = val)
            else:
                self._init_empty(nrow, ncol, val = val, sl = (sr, sc))

    def _init_empty(self, nrow, ncol, val = None, sl = None):
        """
        Inicializacija konstantne matrike.
        """
        if val is None:
            val = 0
        self._data = [[val] * ncol for i in range(nrow)]
        if sl is None:
            self._rslice = slice(0, nrow, 1)
            self._cslice = slice(0, ncol, 1)
        else:
            sr, sc = sl
            self._rslice = normalize_slice(sr, nrow)
            self._cslice = normalize_slice(sc, ncol)

    def _fill_rows(self, it, ncol):
        """
        Polnjenje po vrsticah.
        """
        for i, r in it:
            if isinstance(r, dict):
                for j, x in r.items():
                    self._data[i][j] = x
            else:
                assert len(r) == ncol, "Napačna dolžina vrstice!"
                self._data[i][:] = r

    def _fill_cols(self, it, nrow):
        """
        Polnjenje po stolpcih.
        """
        for j, c in it:
            if isinstance(c, dict):
                for i, x in c.items():
                    self._data[i][j] = x
            else:
                assert len(c) == nrow, "Napačna dolžina stolpca!"
                for i, x in enumerate(c):
                    self._data[i][j] = x

    def _check_dims(self, nrow, ncol):
        """
        Preverjanje dimenzij.
        """
        if nrow is None:
            nrow = self._nrow
        else:
            assert nrow == self._nrow, "Napačno število vrstic!"
        if ncol is None:
            ncol = self._ncol
        else:
            assert ncol == self._ncol, "Napačno število stolpcev!"
        return (nrow, ncol)

    def __repr__(self):
        """
        Znakovna predstavitev.
        """
        if self._nrow == 0 or self._ncol == 0:
            return 'Matrika dimenzij %d x %d' % (self._nrow, self._ncol)
        l = max(max(len(str(x)) for x in r[self._cslice])
                for r in self._data[self._rslice])
        fmtd = '%{}d'.format(l)
        out = ''
        for r in self._data[self._rslice]:
            out += '[ %s ]\n' % '  '.join(fmtd % x for x in r[self._cslice])
        return out[:-1]

    def __eq__(self, other):
        """
        Enakost matrik.

        Matriki sta enaki, če imata enako število vrstic in stolpcev
        ter enake istoležne vrednosti.
        """
        if self is other:
            return True
        if not isinstance(other, AbstractMatrix):
            try:
                other = self.__class__(other, nrow = self._nrow,
                                       ncol = self._ncol)
            except:
                return False
        elif self._nrow != other._nrow or self._ncol != other._ncol:
            return False
        return all(rs[self._cslice] == ro[other._cslice]
                   for rs, ro in zip(self._data[self._rslice],
                                     other._data[other._rslice]))

    def __getitem__(self, key):
        """
        Dostop do komponent in podmatrik.

        Dostop do vsebine matrike M je mogoč z dvojnim indeksom M[i, j],
        kjer sta i in j pozitivni števili oziroma rezini.
        Če sta i in j števili, je rezultat poizvedbe
        število v vrstici i in stolpcu j.
        V nasprotnem primeru je rezultat podmatrika,
        ki ustreza izbranim vrsticam in stolpcem.
        Podmatrika ima dostop do podatkov matrike, iz katere je izpeljana
        -- spreminjanje podmatrike torej spremeni tudi originalno matriko.

        Indeksi vrstic in stolpcev gredo od 0 do n-1,
        kjer je n število vrstic oziroma stolpcev.
        Negativni indeksi niso podprti.
        """
        sr, sc = key
        if not (isinstance(sr, slice) or isinstance(sc, slice)):
            return self._data[self._rslice][sr][self._cslice][sc]
        if not isinstance(sr, slice):
            sr = slice(sr, sr+1, 1)
        if not isinstance(sc, slice):
            sc = slice(sc, sc+1, 1)
        return self.__class__(self, sl = (sr, sc), copy = False)

    def __setitem__(self, key, value):
        """
        Spreminjanje komponent matrike.

        Na izbrana mesta zapiše vrednosti iz matrike ustreznih dimenzij.
        Indeksi so podani na isti način kot pri __getitem__.
        """
        sr, sc = key
        if not (isinstance(sr, slice) or isinstance(sc, slice)):
            if isinstance(value, AbstractMatrix):
                assert value._nrow == 1 and value._ncol == 1, \
                       "Dimenzije se ne ujemajo!"
                value = value[0, 0]
            self._data[self._rslice.start + self._rslice.step * sr] \
                      [self._cslice.start + self._cslice.step * sc] = value
            return
        M = self[key]
        if not isinstance(value, AbstractMatrix) or self._data is value._data:
            value = self.__class__(value, nrow = M._nrow, ncol = M._ncol,
                                   copy = True)
        if M._data is value._data and M._rslice == value._rslice \
                and M._cslice == value._cslice:
            return
        si = M._rslice.start
        vi = value._rslice.start
        for i in range(M._nrow):
            M._data[si][M._cslice] = value._data[vi][value._cslice]
            si += M._rslice.step
            vi += value._rslice.step

    def __iadd__(self, other):
        """
        Prištevanje k matriki.

        K trenutni matriki prišteje istoležne vrednosti podane matrike.
        Če imata matriki skupno nadmatriko,
        se pred računanjem ustvari kopija podane matrike.
        """
        if not isinstance(other, AbstractMatrix) or self._data is other._data:
            other = self.__class__(other, nrow = self._nrow, ncol = self._ncol,
                                   copy = True)
        oi = other._rslice.start
        for r in self._data[self._rslice]:
            sj = self._cslice.start
            oj = other._cslice.start
            for j in range(self._ncol):
                r[sj] += other._data[oi][oj]
                sj += self._cslice.step
                oj += other._cslice.step
            oi += other._rslice.step
        return self

    def __add__(self, other):
        """
        Seštevanje matrik.

        Vrne novo matriko, katerih vrednosti so vsote istoležnih vrednosti
        trenutne in podane matrike.
        Če imata matriki skupno nadmatriko,
        se pred računanjem ustvari kopija podane matrike.
        """
        res = self.__class__(self, nrow = self._nrow, ncol = self._ncol,
                             copy = True)
        res += other
        return res

    def __isub__(self, other):
        """
        Odštevanje od matrike.

        Od trenutne matrike odšteje istoležne vrednosti podane matrike.
        Če imata matriki skupno nadmatriko,
        se pred računanjem ustvari kopija podane matrike.
        """
        if not isinstance(other, AbstractMatrix) or self._data is other._data:
            other = self.__class__(other, nrow = self._nrow, ncol = self._ncol,
                                   copy = True)
        oi = other._rslice.start
        for r in self._data[self._rslice]:
            sj = self._cslice.start
            oj = other._cslice.start
            for j in range(self._ncol):
                r[sj] -= other._data[oi][oj]
                sj += self._cslice.step
                oj += other._cslice.step
            oi += other._rslice.step
        return self

    def __sub__(self, other):
        """
        Odštevanje matrik.

        Vrne novo matriko, katerih vrednosti so razlike istoležnih vrednosti
        trenutne in podane matrike. Če imata matriki skupno nadmatriko,
        se pred računanjem ustvari kopija podane matrike.
        """
        res = self.__class__(self, copy = True)
        res -= other
        return res

    def __rsub__(self, other):
        """
        Odštevanje matrik.

        Vrne novo matriko, katerih vrednosti so razlike istoležnih vrednosti
        podane in trenutne matrike. Če imata matriki skupno nadmatriko,
        se pred računanjem ustvari kopija podane matrike.
        """
        res = self.__class__(other, nrow = self._nrow, ncol = self._ncol,
                             copy = True)
        res -= self
        return res

    def __imul__(self, other):
        """
        Primnožitev matrike ali skalarja.

        Trenutni matriki z desne primnoži podano matriko oziroma skalar.
        Pri množenju matrik se uporabi metoda multiply,
        ki rezultat najprej zapiše v novo matriko,
        nato pa trenutno matriko prepiše z izračunanimi vrednostmi.
        Če imata matriki skupno nadmatriko,
        se pred računanjem ustvari kopija podane matrike.
        """
        if isinstance(other, (int, long, float)):
            for r in self._data[self._rslice]:
                sj = self._cslice.start
                for j in range(self._ncol):
                    r[sj] *= other
                    sj += self._cslice.step
        else:
            if not isinstance(other, AbstractMatrix) \
                or self._data is other._data:
                other = self.__class__(other, nrow = self._ncol,
                                       ncol = self._ncol, copy = True)
            else:
                assert self._ncol == other._nrow and self._ncol == other._ncol, \
                       "Dimenzije matrik ne dopuščajo množenja!"
            res = self.__class__(nrow = self._nrow, ncol = self._ncol)
            res.multiply(self, other)
            self[:, :] = res
        return self

    def __mul__(self, other):
        """
        Množenje z matriko ali skalarjem.

        Vrne novo matriko, ki je enaka produktu trenutne matrike
        in podane matrike oziroma skalarja.
        Pri množenju matrik se uporabi metoda multiply.
        Če imata matriki skupno nadmatriko,
        se pred računanjem ustvari kopija podane matrike.
        """
        if isinstance(other, (int, long, float)):
            res = self.__class__(self, copy = True)
            res *= other
        else:
            if not isinstance(other, AbstractMatrix) \
                    or self._data is other._data:
                other = self.__class__(other, nrow = self._ncol, copy = True)
            else:
                assert self._ncol == other._nrow, \
                       "Dimenzije matrik ne dopuščajo množenja!"
            res = self.__class__(nrow = self._nrow, ncol = other._ncol)
            res.multiply(self, other)
        return res

    def __rmul__(self, other):
        """
        Množenje z matriko ali skalarjem.

        Vrne novo matriko, ki je enaka produktu podane matrike
        oziroma skalarja s trenutno matriko.
        Pri množenju matrik se uporabi metoda multiply.
        Če imata matriki skupno nadmatriko,
        se pred računanjem ustvari kopija podane matrike.
        """
        if isinstance(other, (int, long, float)):
            res = self.__class__(self, copy = True)
            res *= other
        else:
            if not isinstance(other, AbstractMatrix) \
                    or self._data is other._data:
                other = self.__class__(other, ncol = self._nrow, copy = True)
            else:
                assert other._ncol == self._nrow, \
                       "Dimenzije matrik ne dopuščajo množenja!"
            res = self.__class__(nrow = other._nrow, ncol = self._ncol)
            res.multiply(other, self)
        return res

    __radd__ = __add__

    def copy(self):
        """
        Vrne kopijo trenutne matrike brez dostopa do istih podatkov.
        """
        return self.__class__(self, copy = True)

    def multiply(self, left, right):
        """
        V trenutno matriko zapiše produkt podanih matrik.

        Metoda ni implementirana.
        """
        raise NotImplementedError("Množenje matrik ni implementirano!")

    def nrow(self):
        """
        Vrne število vrstic.
        """
        return self._nrow

    def ncol(self):
        """
        Vrne število stolpcev.
        """
        return self._ncol

def normalize_slice(sl, end = None, begin = None, steps = 0):
    """
    Normalizira rezino in preveri ustreznost glede na podane omejitve.
    """
    assert sl.step != 0, "Korak mora biti neničeln!"
    step = 1 if sl.step is None else sl.step
    if step > 0:
        start = 0 if sl.start is None else sl.start
        if end is None:
            end = start + step * steps
        stop = end if sl.stop is None else \
                    (start + step * ((sl.stop - start + step - 1) // step))
        if begin is None:
            begin = 0
        assert start >= begin and stop - step < end, \
               "Indeks je izven meja dimenzije!"
    else:
        if sl.start is None:
            if begin is None:
                begin = 0
            stop = (begin - 1) if sl.stop is None else sl.stop
            if end is None:
                end = stop - step * steps + 1
            start = end - 1
        else:
            start = sl.start
            if begin is None:
                begin = max(0, start + step * steps)
            stop = (begin - 1) if sl.stop is None else \
                        (start + step * ((sl.stop - start + step + 1) // step))
            if end is None:
                end = start + 1
        assert start < end and stop - step >= begin, \
               "Indeks je izven meja dimenzije!"
    if stop < begin:
        stop = None
    return slice(start, stop, step)

def slicelen(sl):
    """
    Vrne število indeksiranih elementov za normalizirano rezino.
    """
    n = 1 if sl.step < 0 else -1
    stop = -1 if sl.stop is None else sl.stop
    return max(0, (stop - sl.start + sl.step + n) // sl.step)

def slicemax(sl):
    """
    Vrne največji indeks, ki ga indeksira normalizirana rezina.
    """
    return sl.stop if sl.step > 0 else (sl.start + 1)
