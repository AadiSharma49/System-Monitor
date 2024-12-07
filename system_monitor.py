import psutil
import tkinter as tk
from ttkbootstrap import Style
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from collections import deque

# Initialize deque for live graph data
cpu_data = deque([0] * 50, maxlen=50)
memory_data = deque([0] * 50, maxlen=50)
disk_data = deque([0] * 50, maxlen=50)
gpu_data = deque([0] * 50, maxlen=50)

# Function to update system stats
def update_stats():
    # CPU
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_label.config(text=f"CPU Usage: {cpu_percent}%")
    cpu_data.append(cpu_percent)
    cpu_line.set_ydata(cpu_data)

    # Memory
    memory = psutil.virtual_memory()
    memory_label.config(text=f"Memory Usage: {memory.percent}% ({memory.used / (1024**3):.2f} GB of {memory.total / (1024**3):.2f} GB)")
    memory_data.append(memory.percent)
    memory_line.set_ydata(memory_data)

    # Disk
    disk = psutil.disk_usage('/')
    disk_label.config(text=f"Disk Usage: {disk.percent}% ({disk.used / (1024**3):.2f} GB of {disk.total / (1024**3):.2f} GB)")
    disk_data.append(disk.percent)
    disk_line.set_ydata(disk_data)

    # GPU (Optional if applicable, needs third-party tools like GPUtil)
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]
            gpu_label.config(text=f"GPU Usage: {gpu.load * 100:.2f}% (Memory: {gpu.memoryUsed}MB/{gpu.memoryTotal}MB)")
            gpu_data.append(gpu.load * 100)
        else:
            gpu_label.config(text="GPU Monitoring: No GPUs detected.")
    except ImportError:
        gpu_label.config(text="GPU Monitoring: No GPU processing available.")
        gpu_data.append(0)

    gpu_line.set_ydata(gpu_data)

    # Update network I/O
    net = psutil.net_io_counters()
    network_label.config(text=f"Network I/O: Sent {net.bytes_sent / (1024**2):.2f} MB, Received {net.bytes_recv / (1024**2):.2f} MB")

    # Refresh graphs
    graph_canvas.draw()

    # Schedule next update
    root.after(1000, update_stats)  # Update every 1 second

# Create the GUI
style = Style(theme="darkly")
root = style.master
root.title("System Monitor")
root.geometry("1200x800")
root.attributes('-fullscreen', True)  # Fullscreen mode

# Header
header = ttk.Label(root, text="Real-Time System Monitor", font=("Helvetica", 24, "bold"))
header.pack(pady=20)

# Labels for stats
cpu_label = ttk.Label(root, text="CPU Usage: Loading...", font=("Helvetica", 16))
cpu_label.pack(pady=10)

memory_label = ttk.Label(root, text="Memory Usage: Loading...", font=("Helvetica", 16))
memory_label.pack(pady=10)

disk_label = ttk.Label(root, text="Disk Usage: Loading...", font=("Helvetica", 16))
disk_label.pack(pady=10)

gpu_label = ttk.Label(root, text="GPU Usage: Loading...", font=("Helvetica", 16))
gpu_label.pack(pady=10)

network_label = ttk.Label(root, text="Network I/O: Loading...", font=("Helvetica", 16))
network_label.pack(pady=10)

# Create a Matplotlib figure for graphs
fig, ax = plt.subplots(4, 1, figsize=(8, 6), dpi=100)
fig.tight_layout(pad=3.0)

# CPU graph
cpu_line, = ax[0].plot(cpu_data, label="CPU Usage", color="red")
ax[0].set_title("CPU Usage (%)")
ax[0].set_ylim(0, 100)

# Memory graph
memory_line, = ax[1].plot(memory_data, label="Memory Usage", color="blue")
ax[1].set_title("Memory Usage (%)")
ax[1].set_ylim(0, 100)

# Disk graph
disk_line, = ax[2].plot(disk_data, label="Disk Usage", color="green")
ax[2].set_title("Disk Usage (%)")
ax[2].set_ylim(0, 100)

# GPU graph
gpu_line, = ax[3].plot(gpu_data, label="GPU Usage", color="purple")
ax[3].set_title("GPU Usage (%)")
ax[3].set_ylim(0, 100)

# Embed Matplotlib figure in Tkinter
graph_canvas = FigureCanvasTkAgg(fig, root)
graph_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Exit button with cursor pointer
exit_button = ttk.Button(root, text="Exit", command=root.destroy, cursor="hand2")
exit_button.pack(pady=20)

# Start updating stats
update_stats()

# Run the application
root.mainloop()
