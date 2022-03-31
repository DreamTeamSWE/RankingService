from entity.Restaurant import Restaurant


class RepositoryInternal:
    def __init__(self):
        pass

    def __save_new_restaurant(self):
        pass

    def get_restaurant_info(self, name: str) -> Restaurant:
        print(name)
        return Restaurant()

    def update_restaurant_info(self, restaurant: Restaurant):
        pass

    def refresh_ranking(self, param):
        pass
