import abc

from myLib.process import Process

class Algorithm(abc.ABC):
    
    def __init__(self, label, processes = []) -> None:
        super().__init__()

        self.processes = processes
        self.label = label
        self.queue_ready = []
        self.queue_running = []
        self.queue_io = []
        self.queue_finished = []

        self.time = 0
        self.idle_time = 0
        self.init_starting_index = 0

    @property
    def no_processes(self):
        return len(self.processes)

    @property
    def cpu_utilization(self):
        return ((self.time - self.idle_time) / self.time) * 100

    @property
    def throughput(self):
        return 1000 * self.no_processes / self.time

    @property
    def burst_time(self):
        return self.time - self.idle_time

    @abc.abstractmethod
    def run(self):
        pass

    def get_queue_finished(self):
        return self.queue_finished

    def get_time(self):
        return self.time

    def get_idle_time(self):
        return self.idle_time

    def add_queue_finished(self, queue):
        self.queue_finished += queue

    def set_processes(self, procesess):
        self.processes = procesess

    def read_csv(self, file_path: str):

        with open(file_path, 'r') as f:
            data = f.read().split()

            for i in range(1, len(data)):
                d = data[i].split(',')
                attr = list(map(int, d))
                self.processes.append(Process(*attr))


    def generate_output(self):

        length = 10
        title = (length + len(self.label) + length)*"=" + "\n" + length*" " + self.label + "\n" + (length + len(self.label) + length)*"=" + "\n\n"
        print(title)
        
        self.processes.sort(key = lambda p : p.id)

        space = 18
        th1 = "Process ID"
        th2 = "Response Time"
        th3 = "Turnaround Time"
        th4 = "Waiting Time"

        table_rows = []
        table_rows.append((space*4)*"=")
        table_headers = "".join([string + (space-len(string))*" " for string in [th1, th2, th3, th4]])

        table_rows.append(table_headers)

        for p in self.processes:
            row = "".join([str(string) + (space-len(string))*" " for string in map(str, [p.id, p.response_time, p.turnaround_time, p.waiting_time])])
            table_rows.append(row)
        
        table_rows.append((space*4)*"=")
        av_rt = sum([p.response_time for p in self.processes]) / self.no_processes
        av_tt = sum([p.turnaround_time for p in self.processes]) / self.no_processes
        av_wt = sum([p.waiting_time for p in self.processes]) / self.no_processes

        last_row = ["Average:", str(av_rt)[:10], str(av_tt)[:10], str(av_wt)[:10]]
        table_last_row = "".join([str(element) + (space-len(element))*" " for element in last_row])
        table_rows.append(table_last_row)
        table_rows.append("\n\n")
        print("\n".join(table_rows))

        print("Total Time:", self.time)
        print("Idle Time:", self.idle_time)
        print("Burst Time:", self.burst_time)
        print("CPU Utilization:", self.cpu_utilization)
        print("Throughput:", self.throughput)