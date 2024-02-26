from math import radians, sin, cos, sqrt, atan2

class Order:
    def __init__(self, order_id, from_location, to_location, price):
        self.order_id = order_id
        self.from_location = from_location
        self.to_location = to_location
        self.price = price

class Courier:
    def __init__(self, courier_id, location):
        self.courier_id = courier_id
        self.busy = False
        self.location = location
        self.count = 0

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def assign_orders_to_couriers_optimized(orders, couriers, max_distance_threshold=10.0,
                                        count_increase_for_distant_couriers=2):
    for order in orders:
        # Находим свободных курьеров
        available_couriers = [courier for courier in couriers if not courier.busy]

        if available_couriers:
            # Если есть свободные курьеры, выбираем того, который ближе всего к точке отправления заказа
            closest_courier = min(available_couriers,
                                  key=lambda x: haversine(order.from_location[0], order.from_location[1], x.location[0],
                                                          x.location[1]))

            # Проверяем, превышает ли расстояние пороговое значение
            if haversine(order.from_location[0], order.from_location[1], closest_courier.location[0],
                         closest_courier.location[1]) > max_distance_threshold:
                # Если превышает, увеличиваем каунт на count_increase_for_distant_couriers
                closest_courier.count += count_increase_for_distant_couriers
        else:
            # Если все курьеры заняты, выбираем того, у которого наименьший каунт
            closest_courier = min(couriers, key=lambda x: x.count)

        # Назначаем заказ выбранному курьеру
        closest_courier.busy = True
        closest_courier.count += 1
        closest_courier.location = order.to_location

        # Выводим информацию о назначении
        print(
            f"Order {order.order_id, order.from_location, order.to_location, order.price} assigned to Courier {closest_courier.courier_id, closest_courier.location}")

# Списки
orders = [
    Order(1, (55.7558, 37.6176), (55.7517, 37.6184), 500),
    Order(2, (55.7517, 37.6184), (55.7522, 37.6156), 380),
    Order(3, (55.7522, 37.6156), (55.7540, 37.6200), 690),
    Order(4, (55.7642, 37.6122), (55.7549, 36.1201), 610),
    Order(5, (55.7232, 37.6132), (55.7512, 37.0000), 490),
    Order(6, (55.7772, 37.6111), (55.8521, 39.6200), 490),
    Order(7, (55.7992, 37.6112), (55.9523, 38.6200), 390),
    Order(8, (55.7552, 37.6112), (56.0540, 37.6230), 990),
    Order(9, (55.7512, 37.6111), (57.7540, 37.6123), 590),
    Order(10, (55.8522, 37.6120), (58.7540, 37.6100), 290),
]

couriers = [
    Courier(101, (54.7558, 36.6176)),
    Courier(102, (55.7517, 37.6184)),
    Courier(103, (55.7537, 37.6180)),
    Courier(104, (55.8522, 37.6120)),
    Courier(105, (55.7512, 37.6115)),
    Courier(106, (55.7537, 37.6160)),
]

assign_orders_to_couriers_optimized(orders, couriers)