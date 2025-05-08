#!/usr/bin/env python3

# PyreGuard © 2025 by gothickitty93 is licensed under CC BY-NC-SA 4.0

import wx
import subprocess

# Set the WireGuard configuration file here
WG_CONF_FILE = '/specify/your/directory/and/file.conf'

def run_command(command):
    try:
        result = subprocess.run(['pkexec', 'sh', '-c', command], check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8'), None
    except subprocess.CalledProcessError as e:
        return None, e.stderr.decode('utf-8')

class PyreGuardFrame(wx.Frame):
    def __init__(self, parent, title):
        super(PyreGuardFrame, self).__init__(parent, title=title, size=(350, 250))
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        btn_start = wx.Button(panel, label='Start WireGuard')
        btn_stop = wx.Button(panel, label='Stop WireGuard')
        btn_status = wx.Button(panel, label='Check Status')
        btn_exit = wx.Button(panel, label='Exit')

        vbox.Add(btn_start, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(btn_stop, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(btn_status, flag=wx.EXPAND | wx.ALL, border=10)
        vbox.Add(btn_exit, flag=wx.EXPAND | wx.ALL, border=10)

        panel.SetSizer(vbox)

        btn_start.Bind(wx.EVT_BUTTON, self.on_start)
        btn_stop.Bind(wx.EVT_BUTTON, self.on_stop)
        btn_status.Bind(wx.EVT_BUTTON, self.on_status)
        btn_exit.Bind(wx.EVT_BUTTON, self.on_exit)

        self.Centre()
        self.Show()

    def on_start(self, event):
        output, error = run_command(f'wg-quick up {WG_CONF_FILE}')
        if error:
            wx.MessageBox(f'Failed to bring up WireGuard:\n{error}', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox(f'WireGuard started successfully:\n{output}', 'Success', wx.OK | wx.ICON_INFORMATION)

    def on_stop(self, event):
        output, error = run_command(f'wg-quick down {WG_CONF_FILE}')
        if error:
            wx.MessageBox(f'Failed to bring down WireGuard:\n{error}', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox(f'WireGuard stopped successfully:\n{output}', 'Success', wx.OK | wx.ICON_INFORMATION)

    def on_status(self, event):
        output, error = run_command('wg')
        if error:
            wx.MessageBox(f'Failed to check status:\n{error}', 'Error', wx.OK | wx.ICON_ERROR)
        else:
            if output:
                wx.MessageBox(output, 'WireGuard Status', wx.OK | wx.ICON_INFORMATION)
            else:
                wx.MessageBox('No active WireGuard interface.', 'WireGuard Status', wx.OK | wx.ICON_INFORMATION)

    def on_exit(self, event):
        self.Close()

if __name__ == '__main__':
    app = wx.App(False)
    frame = PyreGuardFrame(None, 'PyreGuard 25.5.8')
    app.MainLoop()
