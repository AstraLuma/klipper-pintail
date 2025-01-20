# Installation

1. Clone to `~/pintail`
2. Make a venv in `~/pintail-env` and install `requirements.txt` to it
3. Edit `pintail.service` and copy to `/etc/systemd/system`
4. `systemctl daemon-reload` & `systemctl enable pintail` & `systemctl start pintail`
5. Add `pintail` to `~/printer_data/moonraker.asvc`
6. Copy the `moonraker.conf` fragment to your `moonraker.conf`
7. Reload moonraker

TODO: Automate with moonraker update