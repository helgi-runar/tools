import csv
import datetime
import time

import psutil
import pynvml

# Initialize NVML for GPU monitoring
pynvml.nvmlInit()


def get_gpu_info():
    try:
        device_count = pynvml.nvmlDeviceGetCount()
        gpu_usage = []
        gpu_memory = []

        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
            memory = pynvml.nvmlDeviceGetMemoryInfo(handle)

            gpu_usage.append(utilization.gpu)  # GPU usage in %
            gpu_memory.append(memory.used / (1024**2))  # GPU memory used in MB

        return sum(gpu_usage) / len(gpu_usage), sum(gpu_memory) / len(gpu_memory) if gpu_usage else (0, 0)
    except Exception as e:
        print(f"GPU monitoring error: {e}")
        return 0, 0


# File to store the logs
log_file = "resource_usage_log.csv"

# Write header to the log file
with open(log_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "CPU_Usage(%)", "RAM_Usage(MB)", "GPU_Usage(%)", "GPU_Memory(MB)"])

# Start monitoring
print("Logging system resources... Press Ctrl+C to stop.")
try:
    while True:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().used / (1024**2)  # Convert to MB
        gpu_usage, gpu_memory = get_gpu_info()

        # Write data to CSV
        with open(log_file, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, cpu_usage, ram_usage, gpu_usage, gpu_memory])

        time.sleep(1)  # Adjust sampling interval as needed
except KeyboardInterrupt:
    print("Logging stopped.")
finally:
    pynvml.nvmlShutdown()
