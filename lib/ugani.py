__author__ = 'Franko'



def Random(stevilka,params):
        R=params
        glavna_stevilka=3691
        stevilka=int(stevilka)
        glavna_stevilka=int(glavna_stevilka)
        if stevilka < glavna_stevilka:
            tekst = "up"
        elif stevilka > glavna_stevilka:
            tekst = "down"
        else:
            tekst = "ok"
        parametri={"uganil":tekst,"zadnji":stevilka}
        R.update(parametri)
        return R