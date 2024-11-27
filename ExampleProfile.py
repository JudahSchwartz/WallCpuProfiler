import sys
import time

stack = []
# Dictionary to hold accumulated times for each function
accumulated_times = {}

# Global variables to track start times
start_time = None
cpu_start_time = None

def profiler(frame, event, arg):
    global start_time, cpu_start_time

    # Get the function name
    function_name = frame.f_code.co_name

    if event == 'call':

        time_tup = (time.time(), time.process_time())
        stack.append(time_tup)

    elif event == 'return':
        # When the function returns, calculate the time spent
        time_tup = stack.pop()
        start_time, cpu_start_time =time_tup
        wall_clock_time = time.time() - start_time
        cpu_time = time.process_time() - cpu_start_time

        # Add accumulated times to the dictionary
        if function_name not in accumulated_times:
            accumulated_times[function_name] = {'wall_clock': 0, 'cpu': 0}

        accumulated_times[function_name]['wall_clock'] += wall_clock_time
        accumulated_times[function_name]['cpu'] += cpu_time

    return profiler



# Example usage:
def example_function():
    time.sleep(2)  # Simulate some work
    nested_function()


def nested_function():
    time.sleep(3)  # Simulate some nested work


sys.setprofile(profiler)

# Call the decorated function
example_function()


sys.setprofile(None)
# Print accumulated times after execution

print("Accumulated Times:")
for func, times in accumulated_times.items():
    print(f"{func}: Wall Clock Time = {times['wall_clock']:.4f} seconds, CPU Time = {times['cpu']:.4f} seconds")
