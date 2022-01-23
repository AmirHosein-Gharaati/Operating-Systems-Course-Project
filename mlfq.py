from myLib.algorithm import Algorithm
from round_robin import RoundRobin
from fcfs import FCFS
from myLib.process import Process

class MLFQ(Algorithm):

    def __init__(self, label="MLFQ") -> None:
        super().__init__(label)

        self.file_path = ""

    def read_csv(self, file_path: str):

        self.file_path = file_path

        with open(file_path, 'r') as f:
            data = f.read().split()

            for i in range(1, len(data)):
                d = data[i].split(',')
                attr = list(map(int, d))
                self.processes.append(Process(*attr))


    def run(self):

        self.processes.sort()

        first_queue = RoundRobin(time_quantum=8, one_time=True)
        first_queue.set_processes(self.processes)
        first_queue.run()
        first_time = first_queue.get_time()
        first_idle_time = first_queue.get_all_idle_times()


        fake_arrivals = first_queue.get_fake_arrival_time()
        processes = first_queue.get_queue_not_finished()
        self.add_queue_finished(first_queue.get_queue_finished())

        second_queue = RoundRobin(time_quantum=16, one_time=True, processes=processes)
        second_queue.set_fake_arrival_time(fake_arrivals)
        second_queue.run()
        second_time = second_queue.get_time()
        second_idle_time = second_queue.get_all_idle_times()

        fake_arrivals = second_queue.get_fake_arrival_time()
        processes = second_queue.get_queue_not_finished()
        self.add_queue_finished(second_queue.get_queue_finished())
        

        third_queue = FCFS(processes=processes, one_time=True)
        third_queue.set_fake_arrival_time(fake_arrivals)
        third_queue.run()
        third_time = third_queue.get_time()
        third_idle_time = third_queue.get_all_idle_times()

        self.add_queue_finished(third_queue.get_queue_finished())

        self.time = max(first_time, max(second_time, third_time))
        idle_timee = first_idle_time + second_idle_time + third_idle_time
        sett = set(idle_timee)

        self.idle_time = abs(len(idle_timee) - len(sett))
        