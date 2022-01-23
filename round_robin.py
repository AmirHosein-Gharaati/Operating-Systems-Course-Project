from myLib.algorithm import Algorithm

class RoundRobin(Algorithm):

    def __init__(self, time_quantum, label="Round Robin", one_time=False,  processes=[]) -> None:
        super().__init__(label, processes)

        self.time_quantum = time_quantum
        self.queue_not_finished = []
        self.fake_arrival_time = dict()
        self.one_time = one_time
        self.idle_times = []

    def get_all_idle_times(self):
        return self.idle_times

    def get_fake_arrival_time(self):
        return self.fake_arrival_time

    def get_queue_not_finished(self):
        return self.queue_not_finished

    def set_fake_arrival_time(self, times):
        self.fake_arrival_time = times

    def add_fake_arrival(self, id, time):
        self.fake_arrival_time[id] = time

    def run(self):

        self.processes.sort()

        while(len(self.queue_finished) + len(self.queue_not_finished) < self.no_processes):
    
            # init
            if self.one_time and self.fake_arrival_time:
                for p_id in self.fake_arrival_time:
                    arrival_time = self.fake_arrival_time[p_id]
                    
                    if arrival_time == self.time:
                        
                        for p in self.processes:
                            if p.id == p_id:
                                self.queue_running.append(p)

            else:         
                for i in range(self.init_starting_index, len(self.processes)):
                    if self.processes[i].arrival_time <= self.time:
                        self.queue_running.append(self.processes[i])
                        self.init_starting_index += 1

            index_io = 0
            io_progress_time = 1
            flag_io = False

            # running state
            if len(self.queue_running):

                # response time
                if self.queue_running[0].start_time == -1:
                    self.queue_running[0].start_time = self.time

                # cpu time1
                if self.queue_running[0].cpu_time1 >= 1:

                    # cpu time finish
                    if self.queue_running[0].cpu_time1 <= self.time_quantum:
                        self.time += self.queue_running[0].cpu_time1
                        io_progress_time = self.queue_running[0].cpu_time1

                        self.queue_running[0].cpu_time1 = 0
                        self.queue_io.append(self.queue_running[0])
                        flag_io = True
                        self.queue_running.pop(0)
                    
                    else:
                        self.time += self.time_quantum
                        io_progress_time = self.time_quantum

                        self.queue_running[0].cpu_time1 -= self.time_quantum

                        # one time queue
                        if self.one_time:
                            p = self.queue_running.pop(0)
                            self.add_fake_arrival(id=p.id, time=self.time)
                            self.queue_not_finished.append(p)

                        else:
                            self.queue_running.append(self.queue_running[0])
                            self.queue_running.pop(0)

                # cpu time2
                elif self.queue_running[0].io_time == 0 and self.queue_running[0].cpu_time2 >= 1:

                    # cpu time finish
                    if self.queue_running[0].cpu_time2 <= self.time_quantum:
                        self.time += self.queue_running[0].cpu_time2
                        io_progress_time = self.queue_running[0].cpu_time2

                        self.queue_running[0].cpu_time2 = 0
                        self.queue_running[0].stop_time = self.time + self.queue_running[0].cpu_time2
                        self.queue_finished.append(self.queue_running[0])
                        self.queue_running.pop(0)
                    
                    else:
                        self.time += self.time_quantum
                        io_progress_time = self.time_quantum

                        self.queue_running[0].cpu_time2 -= self.time_quantum

                        # one time queue
                        if self.one_time:
                            p = self.queue_running.pop(0)
                            self.add_fake_arrival(id=p.id, time=self.time)
                            self.queue_not_finished.append(p)
                        else:
                            self.queue_running.append(self.queue_running[0])
                            self.queue_running.pop(0)
            else:
                for i in range(self.time, self.time + io_progress_time):
                    self.idle_times.append(f'{i}-{i+1}')
                
                self.time += io_progress_time
                self.idle_time += io_progress_time



            # IO state

            # last element shouldn't be processed for io if flag_io has been set
            end = len(self.queue_io)-1 if flag_io else len(self.queue_io)

            while index_io < end:

                if self.queue_io[index_io].io_time <= io_progress_time:
                    self.queue_io[index_io].io_time = 0
                    self.queue_running.append(self.queue_io[index_io])
                    self.queue_io.pop(index_io)
                else:
                    self.queue_io[index_io].io_time -= io_progress_time
                    index_io += 1

                end = len(self.queue_io)-1 if flag_io else len(self.queue_io)
                
        