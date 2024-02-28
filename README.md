# Dev Shell for kubernetes tasks

A simple container that has some tooling to carry out kubernetes tasks in a shell.  This
is useful because a remote shell (e.g. a desktop connected via VPN) can have problems like
lack of bandwidth or lack of naming. Conveniently having a simple unix like (remote login)
shell can be sufficient for the task.

The OS used is Ubuntu 22.04. Also, common tasks should have common tools (like ping, etc) and these are also built
into the container. Here's a full list of what's installed:

    apt-utils: Additional utilities for apt package manager.
    curl: Downloads files from the internet.
    net-tools: Basic networking utilities.
    iputils-ping: Specifically provides the ping command.
    telnet: Network troubleshooting tool.
    git: Version control system.
    gcc: GNU C compiler.
    vim: Text editor.
    python3-dev: Development libraries for Python 3.
    python3-pip: Package manager for Python 3.
    python-is-python3: Checks if the current Python version is Python 3.

## Use in comibination with a helm chart

The helm chart found in [dev-shell-chart](https://github.com/helxplatform/dev-shell-chart)
is a useful way to deploy as it contains some convenient mapping and environment definitions.
