# Dev Shell for kubernetes tasks

A simple container that has some tooling to carry out kubernetes tasks in a shell.  This
is useful because a remote shell (e.g. a desktop connected via VPN) can have problems like
lack of bandwidth or lack of naming. Conveniently having a simply unix like (remote login)
shell can be sufficient for the task.

Also, common tasks should have common tools (like ping, etc) and these are also built
into the container.

## Use in comibination with a helm chart

The helm chart found in [dev-shell-chart](https://github.com/helxplatform/dev-shell-chart)
is a useful way to deploy as it contains some convenient mapping and environment definitions.
