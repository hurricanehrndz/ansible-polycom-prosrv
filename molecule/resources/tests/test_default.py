import os

import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_polycom_ftp_home(host):
    f = host.file('/home/polycom')

    assert f.exists
    assert f.user == 'polycom'
    assert f.mode == 0o555


@pytest.mark.parametrize("dir_name", [
    "LOGS",
    "OVERRIDES",
    "CONTACTS",
    "LICENCE",
    "PROFILES",
    "CALLLISTS",
    "COREDUMPS",
    "CAMERAPRESETS"
])
def test_polycom_ftp_dirs(host, dir_name):
    d = host.file(f'/home/polycom/{dir_name}')

    assert d.exists
    assert d.is_directory
    assert d.mode == 0o755
    assert d.user == 'polycom'


@pytest.mark.parametrize("dir_name", [
    "FIRMWARE-VVX/5.9.6.rts38",
    "FIRMWARE-TRIO/5.9.1.10906.AB"
])
def test_polycom_fw_dirs(host, dir_name):
    d = host.file(f'/home/polycom/{dir_name}')

    assert d.exists
    assert d.is_directory
    assert d.mode == 0o755
    assert d.user == 'root'


@pytest.mark.parametrize("firmware", [
    "FIRMWARE-VVX/5.9.6.rts38/sip.ver",
    "FIRMWARE-TRIO/5.9.1.10906.AB/sip.ver"
])
def test_polycom_fw(host, firmware):
    f = host.file(f'/home/polycom/{firmware}')

    assert f.exists
    assert f.user == 'root'
    assert f.mode == 0o644


@pytest.mark.parametrize("config", [
    "shared.cfg",
    "000000000000.cfg"
])
def test_polycom_configs(host, config):
    f = host.file(f'/home/polycom/{config}')

    assert f.exists
    assert f.user == 'root'
    assert f.mode == 0o444
