# Operating Systems - CSE Department

## Final Project

The goal in this project is to implement some CPU time scheduling algorithms.

## File Processes

Input of the program is a CSV file including: `process_id`, `arrival_time`, `cpu_time1`, `io_time`, `cpu_time2`

## Algorithms implementation

Four algorithms implemented in this project:

1. First Come, First Serve(FCFS)

2. Round Robin(RR), with time quantum(5ms)

3. Shortest Job First(SFJ)

4. Multilevel Feedback Queue(MLFQ):

    First queue: RR Time Quantum 8 ms

    Second queue: RR with Time Quantum 16 ms

    Third queue: FCFS


## Processes

For every process, some informations should be genereted and shown in output including: `Response Time`, `Waiting Time`, `Turnaround Time`, `Start and Stop Time`

## Final Algorithm Resulsts

After executing every algorithm, some parameters need to be shown inlcuding: `Total Time and Idle Time`, `Average Waiting Time`, `Average Response Time`, `Average Turnaround Time`, `CPU Utilization`, `Throughput`


