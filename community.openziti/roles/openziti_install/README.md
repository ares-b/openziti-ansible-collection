# OpenZiti Install
This role installs and configures OpenZiti components.

## Usage

### Sudo Password
Some tasks needs to be executed with sudo privileges, when using this role, make sure you have a safe way of storing your sudo passwords.
For example, you could use `ansible-vault` and update your hosts file with the key-value `ansible_become_pass="{{ my_host_become_pass }}"`.

### Example hosts
```
---
all:
  children:
    dev_network:
      hosts:
        host_one:
          ansible_host: XXX.XX.XXX.XXX
          ansible_ssh_user: XXXXX
          ansible_become_pass="{{ host_one_become_pass }}"
          openziti_components:
            - ziti-controller
            - ziti-router
            - ziti-tunnel
            - ziti
            - ziti-edge-tunnel
        host_two:
          ansible_host: XXX.XX.XXX.XXX
          ansible_ssh_user: XXXXX
          ansible_become_pass="{{ host_two_become_pass }}"
          openziti_components:
            - ziti_console
```
### Role variables you should care about

 <table>
  <tr>
    <th>Variable</th>
    <th>Default value</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>openziti_core_version</td>
    <td>latest</td>
    <td>OpenZiti core binaries version </td>
  </tr>
  <tr>
    <td>openziti_edge_tunnel_version</td>
    <td>latest</td>
    <td>OpenZiti edge tunnel binaries version </td>
  </tr>
  <tr>
    <td>openziti_console_version</td>
    <td>master</td>
    <td>OpenZiti Console branch name</td>
  </tr>
  <tr>
    <td>openziti_remote_path</td>
    <td>/opt/openziti</td>
    <td>Host's directory where to store OpenZiti components</td>
  </tr>
  <tr>
    <td>openziti_cache_downloads_dir</td>
    <td>/tmp/openziti_downloads</td>
    <td>Directory where to store OpenZiti Downloads on cache server</td>
  </tr>
  <tr>
    <td>openziti_cache_releases_dir</td>
    <td>/tmp/openziti_releases</td>5 Allee Saint Exupery 92390 Villeneuve La Garenne
    <td>Directory where to store OpenZiti components on cache server</td>
  </tr>
  <tr>
    <td>openziti_controller_dir</td>
    <td>"{{ openziti_cache_releases_dir }}/remote_install"</td>
    <td>Directory where to store ansible components on ansible controller before pushing to remote</td>
  </tr>
</table> 

