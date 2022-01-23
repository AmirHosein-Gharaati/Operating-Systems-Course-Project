from myLib.algorithm import Algorithm

class SJF(Algorithm):

    def __init__(self, label="Shortest Job First", processes=[]) -> None:
        super().__init__(label, processes)

    
    def run(self):
        
        self.processes.sort()

        while len(self.queue_finished) < self.no_processes:

            # init
            for i in range(self.init_starting_index, self.no_processes):
                if self.processes[i].arrival_time <= self.time:
                    self.queue_ready.append(self.processes[i])
                    self.init_starting_index += 1

            # put ready to running
            if len(self.queue_ready) > 0:

                minn, index = 10**6, 0
                for i in range(len(self.queue_ready)):
                    if self.queue_ready[i].burst_time < minn:
                        minn = self.queue_ready[i].burst_time
                        index = i

                if len(self.queue_running) == 0:
                    self.queue_running.append(self.queue_ready[index])
                    self.queue_ready.pop(index)
                else:

                    if self.queue_running[0].burst_time > minn:
                        p = self.queue_running.pop(0)
                        self.queue_running.append(self.queue_ready[index])
                        self.queue_ready.pop(index)
                        self.queue_ready.append(p)

            # IO
            io_index = 0
            while io_index < len(self.queue_io):
                if self.queue_io[io_index].io_time == 1:
                    self.queue_io[io_index].io_time = 0
                    self.queue_ready.append(self.queue_io[io_index])
                    self.queue_io.pop(io_index)

                else:
                    self.queue_io[io_index].io_time -= 1
                    io_index += 1

            # idle
            if len(self.queue_running) == 0:
                self.idle_time += 1

            # running state
            else:

                # response time
                if self.queue_running[0].start_time == -1:
                    self.queue_running[0].start_time = self.time
                
                if self.queue_running[0].cpu_time1 > 1:
                    self.queue_running[0].cpu_time1 -= 1

                elif self.queue_running[0].cpu_time1 == 1:
                    self.queue_running[0].cpu_time1 = 0
                    self.queue_io.append(self.queue_running[0])
                    self.queue_running.pop(0)

                elif self.queue_running[0].cpu_time2 > 1:
                    self.queue_running[0].cpu_time2 -= 1

                elif self.queue_running[0].cpu_time2 == 1:
                    self.queue_running[0].cpu_time2 = 0
                    self.queue_running[0].stop_time = self.time

                    self.queue_finished.append(self.queue_running[0])
                    self.queue_running.pop(0)

            self.time += 1