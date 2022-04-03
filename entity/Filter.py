class Filter:
    def __init__(self, zona: str, orario: str, tipo_cucina: str, punteggio: int, pesi: int) -> None:
        self.zona = zona
        self.orario = orario
        self.tipo_cucina = tipo_cucina
        self.punteggio = punteggio
        self.pesi = pesi

    def make_query(self) -> str:
        query = ""
        if self.zona != "":
            query += "zona = '" + self.zona + "' AND "
        if self.orario != "":
            query += "orario = '" + self.orario + "' AND "
        if self.tipo_cucina != "":
            query += "tipo_cucina = '" + self.tipo_cucina + "' AND "
        if self.punteggio != 0:
            query += "punteggio >= " + str(self.punteggio) + " AND "
        # if self.pesi != 0:
        #     query += "pesi >= " + str(self.pesi) + " AND "
        query = query[:-5]
        return query


