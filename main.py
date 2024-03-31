
import sys
import copy

class Process:
    def __init__(self, arrival_time, computation_time):
        self.arrival_time = arrival_time
        self.computation_time = computation_time
        self.start_time = 0
        self.end_time = 0
        self.turn_around_time = 0
        self.waiting_time = 0
        self.remaining_time = computation_time

def FCFS(process_list, num_of_processes):
    process_list = sorted(process_list, key=lambda x: x.arrival_time)
    
    # Initialize variables
    time = process_list[0].arrival_time if process_list else 0
    total_turnaround = 0
    
    for i in range(num_of_processes):
        # Guard against index out of range errors
        if i >= len(process_list):
            break

        process = process_list[i]
        if process.computation_time > 0:  # Only process if computation time > 0
            if time < process.arrival_time:
                time = process.arrival_time

            process.start_time = time
            process.end_time = process.start_time + process.computation_time
            process.turn_around = process.end_time - process.arrival_time
            total_turnaround += process.turn_around
            time = process.end_time
           
    avg = total_turnaround / num_of_processes
    print(f'FCFS: mean turnaround: {avg:.2f}')

#LCFS(NP)
def LCFS_NP(process_list, num_of_processes):
    process_list = sorted(process_list, key=lambda p: p.arrival_time)  

    process_stack = []
    total_turnaround_time = 0
    time = 0

    for process in process_list:
        # If the current time is before the arrival time of the process and the stack is empty,
        # skip to this process arrival time and do the process
        if time < process.arrival_time and not process_stack:
            time = process.arrival_time + process.computation_time
            total_turnaround_time += process.computation_time
            continue

        # If the current time is at or after the arrival time of the process, add the process to the stack
        if time >= process.arrival_time:
            process_stack.append(process)
            continue

        while process_stack and time < process.arrival_time:
            current_process = process_stack.pop()
            current_process.waiting_time = time - current_process.arrival_time
            current_process.turn_around_time = current_process.waiting_time + current_process.computation_time
            total_turnaround_time += current_process.turn_around_time
            time += current_process.computation_time

        # Add the process to the stack
        process_stack.append(process)

    # while there are processes on the stack, pop them off and finish executing them
    while process_stack:
        current_process = process_stack.pop()
        current_process.waiting_time = time - current_process.arrival_time
        current_process.turn_around_time = current_process.waiting_time + current_process.computation_time
        total_turnaround_time += current_process.turn_around_time
        time += current_process.computation_time

    avg = total_turnaround_time / num_of_processes
    print(f'LCFS(NP): mean turnaround: {avg:.2f}')  

#LCFS(P)
def LCFS_P(process_list, num_of_processes):
    process_list = sorted(process_list, key=lambda p: p.arrival_time)  
    
    process_stack = []
    time = 0
    total_turnaround_time = 0

    for i, process in enumerate(process_list):
        # if this is the last element in the list, process it and break out of the loop
        if i == len(process_list) - 1:
            time = process.arrival_time + process.computation_time
            process.turn_around_time = process.computation_time
            total_turnaround_time += process.turn_around_time
            break

        # if the next process arrives after the current process has finished executing,
        # The process is executed without interruption
        if process_list[i + 1].arrival_time - process.arrival_time >= process.computation_time:
            time = process.arrival_time + process.computation_time
            process.turn_around_time = process.computation_time
            total_turnaround_time += process.turn_around_time

        # otherwise, preempt the current process and push it onto the stack
        else:
            time = process_list[i + 1].arrival_time
            process.turn_around_time += process_list[i + 1].arrival_time - process.arrival_time
            process.computation_time -= process.turn_around_time
            process_stack.append(process)

    # while there are processes on the stack, pop them off and finish executing them
    while process_stack:
        current_process = process_stack.pop()  # pop the next process off the stack
        # calculate the waiting time for the process
        current_process.waiting_time = time - current_process.arrival_time - current_process.turn_around_time
        # update the turn-around time for the process
        current_process.turn_around_time += current_process.waiting_time + current_process.computation_time
        total_turnaround_time += current_process.turn_around_time  # update the total turn-around time
        time += current_process.computation_time  # update the current time

    avg = total_turnaround_time / num_of_processes
    print(f'LCFS(P): mean turnaround = {avg:.2f}')  

#RR(2)
def RR(process_list, num_of_processes):
    process_list = sorted(process_list, key=lambda p: p.arrival_time)  

    time_slice = 2
    time = 0
    total_turnaround_time = 0
    process_queue = []

    while True:
        all_completed = True
        # check if any new processes have arrived and add them to the process queue
        for process in process_list:
            if time == process.arrival_time and process.computation_time > 0:
                process_queue.append(process)
            if process.computation_time > 0:  # check if any processes have remaining computation time
                all_completed = False
        if all_completed:  # if all processes have completed, exit the loop
            break

        if process_queue:
            current_process = process_queue.pop(0)  # remove the first process from the queue
            # process has more computation time remaining than the time quantum
            if current_process.computation_time > time_slice:
                current_process.computation_time -= time_slice
                total_turnaround_time += len(process_queue) * time_slice + time_slice

                # check if any new processes have arrived during the time quantum
                for i in range(time + 1, time + time_slice + 1, 1):
                    for process in process_list:
                        if i == process.arrival_time and process.computation_time > 0:
                            process_queue.append(process)  # add the process to the queue
                            total_turnaround_time += time + time_slice - i
                process_queue.append(current_process)  # add the process back to the queue
                time += time_slice + 1

            # process has less or equal computation time remaining than the time quantum
            else:
                cpu_time = current_process.computation_time
                current_process.computation_time = 0
                total_turnaround_time += len(process_queue) * cpu_time + cpu_time

                # check if any new processes have arrived during the time quantum
                for i in range(time + 1, time + cpu_time + 1, 1):
                    for process in process_list:
                        if i == process.arrival_time and process.computation_time > 0:
                            process_queue.append(process)  # add the process to the queue
                            total_turnaround_time += time + cpu_time - i
                time += cpu_time + 1
        else:
            time += 1

    avg = total_turnaround_time / num_of_processes

    print(f'RR: mean turnaround = {avg:.2f}') 

def SJF(process_list, num_of_processes):
    # Exclude processes with 0 computation time for scheduling
    scheduling_process_list = [p for p in process_list if p.computation_time > 0]
    
    completed_processes = 0
    time = 0  # Start time from 0 to handle processes arriving at time 0
    total_turnaround_time = 0

    for process in scheduling_process_list:
        process.remaining_time = process.computation_time

    while completed_processes < len(scheduling_process_list):
        ready_processes = [p for p in scheduling_process_list if p.arrival_time <= time and p.remaining_time > 0]

        if ready_processes:
            ready_processes.sort(key=lambda x: x.computation_time)
            current_process = ready_processes[0]
            current_process.remaining_time -= 1
            if current_process.remaining_time == 0:
                completed_processes += 1
                current_process.end_time = time + 1
                current_process.turn_around_time = current_process.end_time - current_process.arrival_time
                total_turnaround_time += current_process.turn_around_time
        time += 1

    # Calculate average turnaround time including all processes, even those with computation time 0
    avg = total_turnaround_time / num_of_processes
    print(f'SJF: mean turnaround = {avg:.2f}')


path = str(sys.argv[1])  # Get the filename path from the command line argument
filename = open(path, 'r')  # Open the filename
process_list = []  # Initialize an empty list to store the processes

num_of_processes = int(filename.readline().strip())  # Read the number of processes from the first line

# Iterate over the rest of the lines in the filename
for line in filename:
    arrival_time, computation_time = line.strip().split(',')  # Split the line on the comma

    # Convert the values to integers
    arrival_time = int(arrival_time)
    computation_time = int(computation_time)

    # If the computation time is not 0, create a Process object and add it to the list
    if computation_time != 0:
        process_list.append(Process(arrival_time=arrival_time, computation_time=computation_time))

filename.close()  

process_list1 = copy.deepcopy(process_list)
process_list2 = copy.deepcopy(process_list)
process_list3 = copy.deepcopy(process_list)
process_list4 = copy.deepcopy(process_list)
process_list5 = copy.deepcopy(process_list)


FCFS(process_list1, num_of_processes)
LCFS_NP(process_list2, num_of_processes)
LCFS_P(process_list3, num_of_processes)
RR(process_list4, num_of_processes)
SJF(process_list5, num_of_processes)

