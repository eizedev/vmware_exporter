# vmware_exporter

VMware vCenter Exporter for Prometheus.

Get VMware vCenter information:

- Basic VM and Host metrics
- Current number of active snapshots
- Datastore size and other stuff
- Snapshot Unix timestamp creation date

## Badges

![Docker Stars](https://img.shields.io/docker/stars/pryorda/vmware_exporter.svg)
![Docker Pulls](https://img.shields.io/docker/pulls/pryorda/vmware_exporter.svg)
![Docker Automated](https://img.shields.io/docker/automated/pryorda/vmware_exporter.svg)
![Docker Size](https://img.shields.io/docker/image-size/pryorda/vmware_exporter)
![Docker Version](https://img.shields.io/docker/v/pryorda/vmware_exporter)

[![Join the chat at https://gitter.im/vmware_exporter/community](https://badges.gitter.im/vmware_exporter/community.svg)](https://gitter.im/vmware_exporter/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

## Usage

> Requires Python >= 3.8

- Install with `$ python setup.py install` or via pip `$ pip install vmware_exporter`. The docker command below is preferred.
- Create `config.yml` based on the configuration section. Some variables can be passed as environment variables
- Run `$ vmware_exporter -c /path/to/your/config`
- Go to [http://localhost:9272/metrics?vsphere_host=vcenter.company.com](http://localhost:9272/metrics?vsphere_host=vcenter.company.com) to see metrics

Alternatively, if you don't wish to install the package, run it using `$ vmware_exporter/vmware_exporter.py` or use the following docker command:

```shell
docker run -it --rm  -p 9272:9272 -e VSPHERE_USER=${VSPHERE_USERNAME} -e VSPHERE_PASSWORD=${VSPHERE_PASSWORD} -e VSPHERE_HOST=${VSPHERE_HOST} -e VSPHERE_IGNORE_SSL=True -e VSPHERE_SPECS_SIZE=2000 --name vmware_exporter pryorda/vmware_exporter
```

When using containers combined with `--env-file` flag, please use capital letters to set bolleans, for example:

```shell
$ podman run -it --rm -p 9272:9272 --name vmware_exporter --env-file config.env pryorda/vmware_exporter
$ cat config.env
VSPHERE_USER=administrator@vsphere.my.domain.com
VSPHERE_PASSWORD=Secure-Pass
VSPHERE_HOST=192.168.0.1
VSPHERE_IGNORE_SSL=TRUE
VSPHERE_SPECS_SIZE=2000
```

### Configuration and limiting data collection

Only provide a configuration file if enviroment variables are not used. If you do plan to use a configuration file, be sure to override the container entrypoint or add -c config.yml to the command arguments.

If you want to limit the scope of the metrics gathered, you can update the subsystem under `collect_only` in the config section, e.g. under `default`, or by using the environment variables:

```yaml
    collect_only:
        vms: False
        vmguests: True
        datastores: True
        hosts: True
        snapshots: True
        resourcepools: False
```

This would only connect datastores and hosts.

You can have multiple sections for different hosts and the configuration would look like:

```yaml
default:
    vsphere_host: "vcenter"
    vsphere_user: "user"
    vsphere_password: "password"
    ignore_ssl: False
    specs_size: 5000
    fetch_custom_attributes: True
    fetch_tags: True
    fetch_alarms: True
    #exporter_metrics: True
    collect_only:
        vms: True
        vmguests: True
        datastores: True
        hosts: True
        snapshots: True
        resourcepools: False

esx:
    vsphere_host: vc.example2.com
    vsphere_user: 'root'
    vsphere_password: 'password'
    ignore_ssl: True
    specs_size: 5000
    fetch_custom_attributes: True
    fetch_tags: True
    fetch_alarms: True
    #exporter_metrics: True
    collect_only:
        vms: False
        vmguests: True
        datastores: False
        hosts: True
        snapshots: True
        resourcepools: False

limited:
    vsphere_host: slowvc.example.com
    vsphere_user: 'administrator@vsphere.local'
    vsphere_password: 'password'
    ignore_ssl: True
    specs_size: 5000
    fetch_custom_attributes: True
    fetch_tags: True
    fetch_alarms: False
    #exporter_metrics: True
    collect_only:
        vms: False
        vmguests: False
        datastores: True
        hosts: False
        snapshots: False
        resourcepools: False
```

With optional limit to specific custom attributes:

```yaml
default:
    vsphere_host: "vcenter"
    vsphere_user: "user"
    vsphere_password: "password"
    ignore_ssl: False
    specs_size: 5000
    fetch_custom_attributes: True
    custom_attributes_allowed:
    - configurationId
    fetch_tags: True
    fetch_alarms: True
    #exporter_metrics: True
    collect_only:
        vms: True
        vmguests: True
        datastores: True
        hosts: True
        snapshots: True
        resourcepools: False
```

Switching sections can be done by adding ?section=limited to the URL.

#### Monitoring the exporter own metrics

The exporter exposes metrics about its own behavior as [recommended](https://prometheus.io/docs/instrumenting/writing_clientlibs/#exposition) by Prometheus.

Those metrics are available in the `/metrics` page. By default, those metrics are only exposed in the 'default' section (no need to collect it multiple times). This behavior can be controlled using the `VSPHERE_EXPORTER_METRICS` variable or using `exporter_metrics` in the configuration file.

The metrics about the vmware_exporter process are only available on Linux (see [prometheus/client_python](https://github.com/prometheus/client_python#process-collector)).

#### Environment Variables

| Variable                          | Precedence             | Defaults | Description                                                             |
| --------------------------------- | ---------------------- | -------- | ----------------------------------------------------------------------- |
| `VSPHERE_HOST`                    | config, env, get_param | n/a      | vsphere server to connect to                                            |
| `VSPHERE_USER`                    | config, env            | n/a      | User for connecting to vsphere                                          |
| `VSPHERE_PASSWORD`                | config, env            | n/a      | Password for connecting to vsphere                                      |
| `VSPHERE_SPECS_SIZE`              | config, env            | 5000     | Size of specs list for query stats function                             |
| `VSPHERE_IGNORE_SSL`              | config, env            | False    | Ignore the ssl cert on the connection to vsphere host                   |
| `VSPHERE_FETCH_CUSTOM_ATTRIBUTES` | config, env            | False    | Set to true to collect objects custom attributes as metric labels       |
| `VSPHERE_FETCH_TAGS`              | config, env            | False    | Set to true to collect objects tags as metric labels                    |
| `VSPHERE_FETCH_ALARMS`            | config, env            | False    | Fetch objects triggered alarms, and in case of hosts hdw alarms as well |
| `VSPHERE_EXPORTER_METRICS`        | config, env            | True     | Set fo false to disable exposing the exporter metric in section default |
| `VSPHERE_COLLECT_HOSTS`           | config, env            | True     | Set to false to disable collection of host metrics                      |
| `VSPHERE_COLLECT_DATASTORES`      | config, env            | True     | Set to false to disable collection of datastore metrics                 |
| `VSPHERE_COLLECT_VMS`             | config, env            | True     | Set to false to disable collection of virtual machine metrics           |
| `VSPHERE_COLLECT_VMGUESTS`        | config, env            | True     | Set to false to disable collection of virtual machine guest metrics     |
| `VSPHERE_COLLECT_SNAPSHOTS`       | config, env            | True     | Set to false to disable collection of snapshot metrics                  |
| `VSPHERE_COLLECT_RESOURCEPOOLS`   | config, env            | True     | Set to false to disable collection of resourcepool metrics              |

You can create new sections as well, with very similar variables. For example, to create a `limited` section you can set:

| Variable                                  | Precedence             | Defaults | Description                                                               |
| ----------------------------------------- | ---------------------- | -------- | ------------------------------------------------------------------------- |
| `VSPHERE_LIMITED_HOST`                    | config, env, get_param | n/a      | vsphere server to connect to                                              |
| `VSPHERE_LIMITED_USER`                    | config, env            | n/a      | User for connecting to vsphere                                            |
| `VSPHERE_LIMITED_PASSWORD`                | config, env            | n/a      | Password for connecting to vsphere                                        |
| `VSPHERE_LIMITED_SPECS_SIZE`              | config, env            | 5000     | Size of specs list for query stats function                               |
| `VSPHERE_LIMITED_IGNORE_SSL`              | config, env            | False    | Ignore the ssl cert on the connection to vsphere host                     |
| `VSPHERE_LIMITED_FETCH_CUSTOM_ATTRIBUTES` | config, env            | False    | Set to true to collect objects custom attributes as metric labels         |
| `VSPHERE_LIMITED_FETCH_TAGS`              | config, env            | False    | Set to true to collect objects tags as metric labels                      |
| `VSPHERE_LIMITED_FETCH_ALARMS`            | config, env            | False    | Fetch objects triggered alarms, and in case of hosts hdw alarms as well   |
| `VSPHERE_LIMITED_EXPORTER_METRICS`        | config, env            | *        | Expose exporter metrics ( * Enabled only in section 'default' by default) |
| `VSPHERE_LIMITED_COLLECT_HOSTS`           | config, env            | True     | Set to false to disable collection of host metrics                        |
| `VSPHERE_LIMITED_COLLECT_DATASTORES`      | config, env            | True     | Set to false to disable collection of datastore metrics                   |
| `VSPHERE_LIMITED_COLLECT_VMS`             | config, env            | True     | Set to false to disable collection of virtual machine metrics             |
| `VSPHERE_LIMITED_COLLECT_VMGUESTS`        | config, env            | True     | Set to false to disable collection of virtual machine guest metrics       |
| `VSPHERE_LIMITED_COLLECT_SNAPSHOTS`       | config, env            | True     | Set to false to disable collection of snapshot metrics                    |
| `VSPHERE_COLLECT_RESOURCEPOOLS`           | config, env            | True     | Set to false to disable collection of resourcepool metrics                |

You need to set at least `VSPHERE_SECTIONNAME_USER` for the section to be detected.

### Prometheus configuration

You can use the following parameters in the Prometheus configuration file. The `params` section is used to manage multiple login/passwords.

```yaml
  - job_name: 'vmware_vcenter'
    metrics_path: '/metrics'
    static_configs:
      - targets:
        - 'vcenter.company.com'
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: localhost:9272

  - job_name: 'vmware_esx'
    metrics_path: '/metrics'
    file_sd_configs:
      - files:
        - /etc/prometheus/esx.yml
    params:
      section: [esx]
    relabel_configs:
      - source_labels: [__address__]
        target_label: __param_target
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: localhost:9272

# Example of Multiple vCenter usage per #23

- job_name: vmware_export
    metrics_path: /metrics
    static_configs:
    - targets:
      - vcenter01
      - vcenter02
      - vcenter03
    relabel_configs:
    - source_labels: [__address__]
      target_label: __param_target
    - source_labels: [__param_target]
      target_label: instance
    - target_label: __address__
      replacement: exporter_ip:9272
```

## Current Status

- vCenter and vSphere 6.0/6.5 have been tested.
- VM information, Snapshot, Host and Datastore basic information is exported, i.e:

```yaml
# HELP vmware_snapshots VMware current number of existing snapshots
# TYPE vmware_snapshot_count gauge
vmware_snapshot_timestamp_seconds{vm_name="My Super Virtual Machine"} 2.0
# HELP vmware_snapshot_timestamp_seconds VMware Snapshot creation time in seconds
# TYPE vmware_snapshot_timestamp_seconds gauge
vmware_snapshot_age{vm_name="My Super Virtual Machine",vm_snapshot_name="Very old snaphot"} 1478146956.96092
vmware_snapshot_age{vm_name="My Super Virtual Machine",vm_snapshot_name="Old snapshot"} 1478470046.975632

# HELP vmware_datastore_capacity_size VMware Datastore capacity in bytes
# TYPE vmware_datastore_capacity_size gauge
vmware_datastore_capacity_size{ds_name="ESX1-LOCAL"} 67377299456.0
# HELP vmware_datastore_freespace_size VMware Datastore freespace in bytes
# TYPE vmware_datastore_freespace_size gauge
vmware_datastore_freespace_size{ds_name="ESX1-LOCAL"} 66349694976.0
# HELP vmware_datastore_uncommited_size VMware Datastore uncommitted in bytes
# TYPE vmware_datastore_uncommited_size gauge
vmware_datastore_uncommited_size{ds_name="ESX1-LOCAL"} 0.0
# HELP vmware_datastore_provisoned_size VMware Datastore provisoned in bytes
# TYPE vmware_datastore_provisoned_size gauge
vmware_datastore_provisoned_size{ds_name="ESX1-LOCAL"} 1027604480.0
# HELP vmware_datastore_hosts VMware Hosts number using this datastore
# TYPE vmware_datastore_hosts gauge
vmware_datastore_hosts{ds_name="ESX1-LOCAL"} 1.0
# HELP vmware_datastore_vms VMware Virtual Machines number using this datastore
# TYPE vmware_datastore_vms gauge
vmware_datastore_vms{ds_name="ESX1-LOCAL"} 0.0

# HELP vmware_host_power_state VMware Host Power state (On / Off)
# TYPE vmware_host_power_state gauge
vmware_host_power_state{host_name="esx1.company.com"} 1.0
# HELP vmware_host_cpu_usage VMware Host CPU usage in MHz
# TYPE vmware_host_cpu_usage gauge
vmware_host_cpu_usage{host_name="esx1.company.com"} 2959.0
# HELP vmware_host_cpu_max VMware Host CPU max availability in MHz
# TYPE vmware_host_cpu_max gauge
vmware_host_cpu_max{host_name="esx1.company.com"} 28728.0
# HELP vmware_host_memory_usage VMware Host Memory usage in Mbytes
# TYPE vmware_host_memory_usage gauge
vmware_host_memory_usage{host_name="esx1.company.com"} 107164.0
# HELP vmware_host_memory_max VMware Host Memory Max availability in Mbytes
# TYPE vmware_host_memory_max gauge
vmware_host_memory_max{host_name="esx1.company.com"} 131059.01953125
```

## References

The VMware exporter uses theses libraries:

- [pyVmomi](https://github.com/vmware/pyvmomi) for VMware connection
- Prometheus [client_python](https://github.com/prometheus/client_python) for Prometheus supervision
- [Twisted](http://twistedmatrix.com/trac/) for HTTP server

The initial code is mainly inspired by:

- [https://www.robustperception.io/writing-a-jenkins-exporter-in-python](https://www.robustperception.io/writing-a-jenkins-exporter-in-python/)
- [https://github.com/vmware/pyvmomi-community-samples](https://github.com/vmware/pyvmomi-community-samples)
- [https://github.com/jbidinger/pyvmomi-tools](https://github.com/jbidinger/pyvmomi-tools)

Forked from [rverchere/vmware_exporter](https://github.com/rverchere/vmware_exporter). I removed the fork so that I could do searching and everything.

## Maintainer

Daniel Pryor [pryorda](https://github.com/pryorda)

## License

See LICENSE file

[![Known Vulnerabilities](https://snyk.io/test/github/rmontenegroo/vmware_exporter/badge.svg?targetFile=requirements.txt)](https://snyk.io/test/github/rmontenegroo/vmware_exporter?targetFile=requirements.txt)
