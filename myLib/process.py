class Process:

    def __init__(self, id, arrival_time, cpu_time1, io_time, cpu_time2):
        self.id = id
        self.arrival_time = arrival_time
        self.cpu_time1 = cpu_time1
        self.io_time = io_time
        self.cpu_time2 = cpu_time2
        self.burst_time = cpu_time1 + cpu_time2

        self.start_time = -1
        self.stop_time = 0

    @property
    def remaining_time(self):
        return self.cpu_time1 + self.cpu_time2

    @property
    def turnaround_time(self):
        return self.stop_time - self.arrival_time

    @property
    def waiting_time(self):
        return self.turnaround_time - self.burst_time
    
    @property
    def response_time(self):
        return self.start_time - self.arrival_time

    def __lt__(self, other):
        return self.arrival_time < other.arrival_time

    def __str__(self):
        ID = "Process ID: " + str(self.id)
        arrival_time = "\tarrival_time: " + str(self.arrival_time)
        cpu_time1 = "\tcpu time 1: " + str(self.cpu_time1)
        io_time = "\tIO time: " + str(self.io_time)
        cpu_time2 = "\tcpu time 2: " + str(self.cpu_time2)

        return "\n".join([ID, arrival_time, cpu_time1, io_time, cpu_time2, "\n"])