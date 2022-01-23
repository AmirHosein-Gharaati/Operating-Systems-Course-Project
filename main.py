from fcfs import FCFS
from round_robin import RoundRobin
from sjf import SJF
from mlfq import MLFQ


if __name__ == '__main__':

    menu = "Please enter your algorithm:\n 1.FCFS\n 2.Round Robin\n 3.SJF\n 4.MLFQ\n"

    print(menu)

    choice = input()

    if choice == "1":
        p = FCFS(label="FCFS")
        p.read_csv('proces_inputs.csv')
        p.run()
        p.generate_output()

    elif choice == "2":
        p = RoundRobin(time_quantum=16)
        p.read_csv('proces_inputs.csv')
        p.run()
        p.generate_output()

    elif choice == "3":
        p = SJF()
        p.read_csv('proces_inputs.csv')
        p.run()
        p.generate_output()

    elif choice == "4":
        p = MLFQ(label="MLFQ")
        p.read_csv('proces_inputs.csv')
        p.run()
        p.generate_output()