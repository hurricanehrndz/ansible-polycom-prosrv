# hurricanehrndz.polycom-prosrv

[![Build Status](https://img.shields.io/travis/hurricanehrndz/ansible-polycom-prosrv/master.svg?style=for-the-badge&logo=travis)](https://travis-ci.org/hurricanehrndz/ansible-polycom-prosrv)
[![Galaxy](http://img.shields.io/badge/galaxy-hurricanehrndz.polycom--prosrv-blue.svg?style=for-the-badge&logo=ansible)](https://galaxy.ansible.com/hurricanehrndz/polycom_prosrv)
[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg?style=for-the-badge)](https://raw.githubusercontent.com/hurricanehrndz/ansible-rustup/master/LICENSE)

`hurricanehrndz.polycom-prosrv` is an Ansible role which:

- installs vsftp
- configures vsftp for polycom provisiong
- xml validation of configs
- secures vsftp
- grants acccess to lone ftp user
- creates provisiong directory structure
- downloads UC software for VVX and TRIO phones

In summary, this role configures a vsftp instance for provisioing polycom VVX
and TRIO phones. Please feel free to submit pull requests to add aditional
features. The current set of features are sufficient for my needs.

## Upcoming features

- Logo branding
- FTPS - letsecnrypt
- nginx - logo serving
- RHEL support

## Requirements

- Ansible >= 2.4
- [vsftpd-role](requirements.yml)

## Installation

Using `ansible-galaxy`:

```shell
ansible-galaxy install hurricanehrndz.polycom-prosrv
```

Using `requirements.yml`:

```yaml
- src: hurricanehrndz.polycom-prosrv
```

Using `git`:

```shell
git clone https://github.com/hurricanehrndz/ansible-polycom-prosrv.git hurricanehrndz.polycom-prosrv
```

## Role Variables

All variables meant to be overridden are stored in the
[defaults/main.yml](defaults/main.yml) file. A list and short description of
these variables can also be found in the table below.

| Name                          | Types/Values   | Description                                                                                  |
| ----------------------------- | -------------- | -------------------------------------------------------------------------------------------  |
| `polycom_vvx_uc_software`     | string         | Url to latest vvx 'split' firware zip.                                                       |
| `polycom_trio_uc_software`    | string         | Url  to latest trio firmware zip.                                                            |
| `polycom_exchnage_integration`| boolean        | Enable Exchange integration                                                                  |
| `polycom_exchnage_url`        | string         | Exchange web services URL for org                                                            |
| `polycom_exchnage_reminder`   | boolean        | Enable calendar reminders                                                                    |
| `polycom_enable_btoe`         | boolean        | Enable Better Together Over Ethernet feature                                                 |
| `polycom_set_admin_pass`      | boolean        | Set admin phone password                                                                     |
| `polycom_admin_pass`          | string         | Set admin phone password to value. '456'                                                     |
| `polycom_enable_lync_updates` | boolean        | Enable Update from SfB Servers                                                               |
| `polycom_enable_http`         | boolean        | Enable phone's web interface over https                                                      |
| `polycom_web_port`            | interger       | HTTPS port web interface listens on                                                          |
| `polycom_ftp_user`            | string         | Username for accessing provisioning server                                                   |
| `polycom_ftp_name`            | string         | User identity for acessing provisioning server                                               |
| `polycom_ftp_pass`            | string         | [user password, hashed and salted](https://bit.ly/2PD9Vgr). Default is 'polycom456'          |
| `polycom_prov_add_opts`       | hash           | additional opt for sane defaults on FTP service set by role                                  |
| `polycom_phone_creds`         | hash           | SfB Phone credentials for Single-Sign-In, see [example](molecule/default/vars/test-vars.yml) |

## Dependencies

- [vsftpd-role](/requirements.yml)

## Example Playbook

```yaml
- hosts: servers
  pre_tasks:
    - name: Update repo cache
      action: >
        {{ ansible_pkg_mgr }} update_cache=ye
  tasks:
    - name: Setup polycom provisioning
      include_role:
        name: hurricanehrndz.polycom-prosrv
      vars:
        # FTP server
        polycom_prosrv_addy: "prosrv.contoso.com"
        polycom_prosrv_add_opts:
          pasv_addr_resolve: YES
        polycom_phone_creds:
          - polycom_phone_mac: "0004ffffffff"
            polycom_phone_user: "roomphone"
            polycom_phone_pass: "secret"
            polycom_phone_domain: "contoso.com"
```

```yaml
- hosts: servers
  pre_tasks:
    - name: Update repo cache
      action: >
        {{ ansible_pkg_mgr }} update_cache=ye
  tasks:
    - name: Setup polycom provisioning
      include_role:
        name: hurricanehrndz.polycom-prosrv
      vars:
        # implicit FTPS server
        polycom_prosrv_addy: "prosrv.contoso.com"
        polycom_prosrv_add_opts:
          # certs must exist, create using another role
          rsa_cert_file: /etc/letsencrypt/live/prosrv.contoso.com/cert.pem
          rsa_private_key_file: /etc/letsencrypt/live/prosrv.contoso.com/privkey.pem

          listen_port: 990
          pasv_addr_resolve: YES
          ssl_enable: YES
          implicit_ssl: YES
          allow_anon_ssl: NO
          force_local_data_ssl: YES
          force_local_logins_ssl: YES
          ssl_tlsv1: YES
          ssl_sslv2: NO
          ssl_sslv3: NO
          # Polycom need to reuse
          require_ssl_reuse: NO
          ssl_ciphers: HIGH
        polycom_phone_creds:
          - polycom_phone_mac: "0004ffffffff"
            polycom_phone_user: "roomphone"
            polycom_phone_pass: "secret"
            polycom_phone_domain: "contoso.com"

```

## License

[MIT](LICENSE)

## Author Information

[Carlos Hernandez aka HurricaneHrndz](https://github.com/hurricanehrndz)

### Sources

- [Optimising the Polycom VVX for Lync/SfB](https://greiginsydney.com/optimising-the-polycom-vvx-for-lync/)
- [https://greiginsydney.com/polycom-vvx-firmware-v5-now-with-btoe/](https://greiginsydney.com/polycom-vvx-firmware-v5-now-with-btoe/)
- [Device Updates with Skype for Business Online](http://blog.schertz.name/2016/07/device-updates-with-skype-for-business-online/)
- [Master config for Polycom VVX & Trio device families](https://github.com/greiginsydney/000000000000.cfg/)
- [Updating Polycom VVX Phones](https://blog.schertz.name/2013/10/updating-polycom-vvx-phones/)
- [SfB - Polycom Docs](https://support.polycom.com/content/dam/polycom-support/products/voice/business-media-phones/downloads/previous-versions/archived-documents/en/uc-software-lync-deploy-guide-5-5-1.pdf)
