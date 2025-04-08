#!/usr/bin/env python3

#PyreGuard by gothickitty93
import subprocess
import tkinter as tk
from tkinter import messagebox
import os

# Set the WireGuard configuration file here
WG_CONF_FILE = '/specify/your/directory/and/file.conf'

def run_command(command):
    try:
        result = subprocess.run(['pkexec', 'sh', '-c', command], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8'), None
    except subprocess.CalledProcessError as e:
        return None, e.stderr.decode('utf-8')

def start_wg():
    output, error = run_command(f'wg-quick up {WG_CONF_FILE}')
    if error:
        messagebox.showerror('Error', f'Failed to bring up WireGuard:\n{error}')
    else:
        messagebox.showinfo('Success', f'WireGuard started successfully:\n{output}')

def stop_wg():
    output, error = run_command(f'wg-quick down {WG_CONF_FILE}')
    if error:
        messagebox.showerror('Error', f'Failed to bring down WireGuard:\n{error}')
    else:
        messagebox.showinfo('Success', f'WireGuard stopped successfully:\n{output}')

def check_status():
    output, error = run_command('wg')
    if error:
        messagebox.showerror('Error', f'Failed to check status:\n{error}')
    else:
        if output:
            messagebox.showinfo('WireGuard Status', output)
        else:
            messagebox.showinfo('WireGuard Status', 'No active WireGuard interface.')

# Create GUI window
root = tk.Tk()
root.title('WireGuard GUI')
root.geometry('300x200')

# Add buttons
btn_start = tk.Button(root, text='Start WireGuard', command=start_wg)
btn_start.pack(pady=10)

btn_stop = tk.Button(root, text='Stop WireGuard', command=stop_wg)
btn_stop.pack(pady=10)

btn_status = tk.Button(root, text='Check Status', command=check_status)
btn_status.pack(pady=10)

btn_exit = tk.Button(root, text='Exit', command=root.quit)
btn_exit.pack(pady=10)

# Run the GUI
root.mainloop()
