# Show this help
@help:
    just --list

# Push and run a command
run *CMD:
    rsync -av --delete ./ ender.local:pintail/
    ssh ender.local -t cd pintail \; {{CMD}}

# Push and run a python script
@py *CMD:
    just run ~/pintail-env/bin/python3 {{CMD}}

# Sync and open a repl
repl:
    rsync -av --delete ./ ender.local:pintail/
    ssh ender.local -t cd pintail \; ~/pintail-env/bin/python3

# Stop service for development
stop:
    ssh ender.local -t sudo systemctl stop pintail

# Start service when development is done
start:
    ssh ender.local -t sudo systemctl start pintail
    