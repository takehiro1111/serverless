class Company:
    def __init__(self, sales, engeneer):
        self.sales = sales
        self._engeneer = engeneer

    def first_carrer(self):
        print(self.sales)

    def second_carrer(self):
        print(self._engeneer)


class Dream(Company):
    def __init__(self, sales, engeneer, consul, sports="baseball"):
        super().__init__(sales, engeneer)
        self.consul = consul
        self.sports = sports

    @property
    def money(self):
        return self.consul

    @property
    def sport(self):
        if self.sports == "soccer":
            return self.sports
        else:
            raise ValueError


job = Company("btm", "nb")
job.first_carrer()
job.second_carrer()

job_2 = Dream("ses", "sre", "storategy")
job_2.first_carrer()
job_2.second_carrer()

print(job_2.money)

soccer = Dream("ses", "sre", "storategy")
soccer.sport = "soccer"
print(soccer.sport)


# print(dir(frozenset))
