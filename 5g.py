import simpy
import random
import logging
from datetime import timedelta


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S')


def format_sim_time(seconds):
    td = timedelta(seconds=seconds)
    return str(td)[:-3]


class NetworkSimulator:
    def __init__(self, environment, num_users):
        self.env = environment
        self.num_users = num_users
        self.base_station = BaseStation(environment)
        self.users = [UserEquipment(environment, f"Usuário {i + 1}", self.base_station) for i in range(num_users)]

    def run(self):
        for user in self.users:
            yield self.env.process(user.generate_traffic())


class BaseStation:
    def __init__(self, environment):
        self.env = environment
        self.capacity = 1000  # Mbps

    def connect(self, ue):
        logging.info(f'{ue.name} está conectando à estação base no tempo {format_sim_time(self.env.now)}')

        yield self.env.timeout(random.uniform(0.005, 0.02))

    def send_data(self, ue, amount):
        logging.info(f'{ue.name} está enviando {amount}MB no tempo {format_sim_time(self.env.now)}')
        yield self.env.timeout(amount / self.capacity)
        logging.info(f'{ue.name} terminou de enviar os dados no tempo {format_sim_time(self.env.now)}')


class UserEquipment:
    def __init__(self, environment, name, base_station):
        self.env = environment
        self.name = name
        self.base_station = base_station

    def generate_traffic(self):
        while True:
            sleep_time = random.randint(3, 10)

            logging.info(f'{self.name} está ocioso por {sleep_time} segundos no tempo {format_sim_time(self.env.now)}')

            yield self.env.timeout(sleep_time)

            data_size = random.randint(100, 1000)

            logging.info(f'{self.name} gerou {data_size}MB de dados no tempo {format_sim_time(self.env.now)}')

            yield self.env.process(self.base_station.connect(self))
            yield self.env.process(self.base_station.send_data(self, data_size))


def simulate_5g_network():
    env = simpy.Environment()
    sim = NetworkSimulator(env, num_users=5)

    env.process(sim.run())
    env.run(until=20)


if __name__ == '__main__':
    simulate_5g_network()
