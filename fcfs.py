from myLib.algorithm import Algorithm

class FCFS(Algorithm):

    def __init__(self, label="FCFS", processes=[], one_time=False) -> None:
        super().__init__(label, processes)

        self.fake_arrival_time = dict()
        self.idle_times = []
        self.one_time = one_time

    def set_fake_arrival_time(self, times):
        self.fake_arrival_time = times

    def get_all_idle_times(self):
        return self.idle_times
    
    def run(self):

        self.processes.sort()
        
        while len(self.queue_finished) < self.no_processes:
            
            # init put to ready queue
            if self.one_time:
                for key, value in self.fake_arrival_time.items():
                    p_id = key
                    arrival_time = value

                    if arrival_time == self.time:
                        
                        for p in self.processes:
                            if p.id == p_id:
                                self.queue_ready.append(p)

            else:         
                # for i in range(self.init_starting_index, len(self.processes)):
                #     if self.processes[i].arrival_time <= self.time:
                #         self.queue_running.append(self.processes[i])
                #         self.init_starting_index += 1

                for i in range(self.init_starting_index, self.no_processes):
                    if self.processes[i].arrival_time <= self.time:
                        self.queue_ready.append(self.processes[i])
                        self.init_starting_index += 1

            # put ready to running
            if len(self.queue_running) == 0 and len(self.queue_ready) > 0:
                self.queue_running.append(self.queue_ready[0])
                self.queue_ready.pop(0)

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
                self.idle_times.append(f'{self.time}-{self.time}')
                self.idle_time += 1

            # take from running to IO or finish
            # NOTE: there is actually just one process in the running state
            for i in range(len(self.queue_running)):
                if self.queue_running[i].start_time == -1:
                    self.queue_running[i].start_time = self.time
                
                if self.queue_running[i].cpu_time1 == 1 and self.queue_running[i].io_time > 0:
                    self.queue_running[i].cpu_time1 = 0
                    self.queue_io.append(self.queue_running[i])
                    self.queue_running.pop(i)

                elif self.queue_running[i].cpu_time1 > 1:
                    self.queue_running[i].cpu_time1 -= 1

                elif self.queue_running[i].cpu_time2 == 1 and self.queue_running[i].io_time == 0 :
                    self.queue_running[i].cpu_time2 = 0
                    self.queue_running[i].stop_time = self.time + 1
                    p = self.queue_running.pop(i)
                    self.queue_finished.append(p)
                    
                elif self.queue_running[i].cpu_time2 > 1:
                    self.queue_running[i].cpu_time2 -= 1
            
            self.time += 1