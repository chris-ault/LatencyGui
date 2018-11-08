#!/usr/bin/env python
import PySimpleGUI27 as sg
import subprocess
import shlex
import sys
import os

def run_command(command):
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            if 'time' in output:
                return output.strip().split('time=')[1].split('TTL')[0].rstrip()
    rc = process.poll()
    return rc


try:
    # python 2.x
    import Tkinter as tk
except ImportError:
    # python 3.x
    import tkinter as tk


class Example(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.text = tk.Text(self, height=6, width=40)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=self.vsb.set)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)

        self.add_timestamp()

    def add_timestamp(self):
        ip = sys.argv[1]
        self.text.insert("end", str(run_command("ping " + ip)) + "\n")
        self.text.see("end")
        self.after(1000, self.add_timestamp)

if __name__ == "__main__":
    root =tk.Tk()
    root.title("Latency")
    #root.resizable(0,0)
    root.geometry("100x50")
    #root.overrideredirect(1)
    frame = Example(root)
    frame.pack(fill="both", expand=True)
    root.mainloop()
