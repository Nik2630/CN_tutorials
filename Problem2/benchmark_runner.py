import subprocess
import re
import matplotlib.pyplot as plt
import sys

def run_benchmarks():
    client_counts = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    execution_times = []

    print("Running benchmarks...")

    for num_clients in client_counts:
        command = ["bash", "start.sh", "client.py", str(num_clients)]
        try:
            process_output = subprocess.run(command, capture_output=True, text=True, check=True)
            output_text = process_output.stdout

            # Extract execution time using regex
            match = re.search(r"Total execution time: (\d+\.\d+) seconds", output_text)
            if match:
                execution_time = float(match.group(1))
                execution_times.append(execution_time)
                print(f"Benchmark for {num_clients} clients completed. Execution time: {execution_time:.2f} seconds")
            else:
                execution_times.append(None) # or some error value
                print(f"Error: Could not extract execution time for {num_clients} clients.")

        except subprocess.CalledProcessError as e:
            execution_times.append(None) # or some error value
            print(f"Error running benchmark for {num_clients} clients:")
            print(e.stderr)
        except FileNotFoundError:
            execution_times.append(None)
            print("Error: start.sh or client.py not found. Make sure they are in the same directory as this script.")
            return None, None # Exit if start.sh is not found

    return client_counts, execution_times

def print_table(client_counts, execution_times, server_type):
    print(f"\nBenchmark Results for Server Type {server_type}:")
    print("-" * 30)
    print("{:<15} {:<15}".format("Clients", "Execution Time (s)"))
    print("-" * 30)
    for i in range(len(client_counts)):
        time_str = "{:.2f}".format(execution_times[i]) if execution_times[i] is not None else "Error"
        print("{:<15} {:<15}".format(client_counts[i], time_str))
    print("-" * 30)

def plot_benchmark_graph(client_counts, execution_times, server_type):
    if not client_counts or not execution_times:
        print("No data to plot.")
        return

    plt.figure(figsize=(10, 6))
    plt.plot(client_counts, execution_times, marker='o', linestyle='-')
    plt.xlabel('Number of Concurrent Clients')
    plt.ylabel('Execution Time (Latency) in seconds')
    plt.title(f'Client Benchmark Performance - Server Type {server_type}')
    plt.xticks(client_counts)
    plt.ylim(0, 320)  
    plt.grid(True)
    plt.savefig(f'client_benchmark_plot_server{server_type}.png')
    plt.show()
    print(f"Benchmark plot saved as client_benchmark_plot_server{server_type}.png")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python benchmark_runner.py <server_type>")
        print("server_type must be 1, 2, or 3")
        sys.exit(1)

    server_type = int(sys.argv[1])
    if server_type not in [1, 2, 3]:
        print("Error: server_type must be 1, 2, or 3")
        sys.exit(1)

    clients, times = run_benchmarks()
    if clients and times:
        print_table(clients, times, server_type)
        plot_benchmark_graph(clients, times, server_type)
    else:
        print("Benchmark execution failed or start.sh script not found. Please check errors above.")