import simpy
import random
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class NetworkSimulator4G:
    def __init__(self, environment, num_users):
        self.env = environment
        self.num_users = num_users
        self.base_station = BaseStation4G(environment)
        self.users = [UserEquipment4G(environment, f"Usuário {i + 1}", self.base_station) for i in range(num_users)]

    def run(self):
        for user in self.users:
            yield self.env.process(user.generate_traffic())


class BaseStation4G:
    def __init__(self, environment):
        self.env = environment
        self.capacity = 300

    def connect(self, ue):
        logging.info(f'{ue.name} está se conectando ao eNodeB 4G em {self.env.now}')

        yield self.env.timeout(random.uniform(0.01, 0.1))

    def send_data(self, ue, amount):
        logging.info(f'{ue.name} está enviando {amount}MB em {self.env.now}')

        yield self.env.timeout(amount / self.capacity)

        logging.info(f'{ue.name} terminou de enviar dados em {self.env.now}')


class UserEquipment4G:
    def __init__(self, environment, name, base_station):
        self.env = environment
        self.name = name
        self.base_station = base_station

    def generate_traffic(self):
        while True:
            sleep_time = random.randint(5, 15)

            logging.info(f'{self.name} está ocioso por {sleep_time} segundos em {self.env.now}')

            yield self.env.timeout(sleep_time)

            data_size = random.randint(20, 300)

            logging.info(f'{self.name} gerou {data_size}MB de dados em {self.env.now}')

            yield self.env.process(self.base_station.connect(self))
            yield self.env.process(self.base_station.send_data(self, data_size))


def simulate_4g_network():
    env = simpy.Environment()
    sim_4g = NetworkSimulator4G(env, num_users=5)

    env.process(sim_4g.run())
    env.run(until=20)


if __name__ == '__main__':
    simulate_4g_network()
