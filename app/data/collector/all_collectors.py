from app.data.collector.cpu import CPUCollector
from app.data.collector.disk import DiskCollector
from app.data.collector.network import NetworkCollector
from app.data.collector.system_command import run_shell, collect_top, collect_vmstat, collect_pidstat, \
                                                                     collect_free, collect_df, collect_iostat, collect_ethtool
from app.data.collector.log_reader import collect_system_log, collect_kernel_log, collect_app_log

class AllCollectors:
    def __init__(self):
        self.network_collector = NetworkCollector()
        self.disk_collector = DiskCollector()
        self.cpu_collector = CPUCollector()

    def collect_network(self):
        return self.network_collector.collect()

    def top_network(self, n=5):
        return self.network_collector.top(n)

    def recent_network(self, n=5):
        return self.network_collector.recent(n)

    def collect_disk(self):
        return self.disk_collector.collect()

    def top_disk(self, n=5, path='/'):
        return self.disk_collector.top(n, path)

    def recent_disk(self, n=5, path='/'):
        return self.disk_collector.recent(n, path)

    def collect_cpu(self):
        return self.cpu_collector.collect()

    def top_cpu(self, n=5):
        return self.cpu_collector.top(n)

    def recent_cpu(self, n=5):
        return self.cpu_collector.recent(n)

    def run_shell_command(self, command):
        return run_shell(command)

    def collect_top_info(self):
        return collect_top()

    def collect_vmstat_info(self):
        return collect_vmstat()

    def collect_pidstat_info(self):
        return collect_pidstat()

    def collect_free_info(self):
        return collect_free()

    def collect_df_info(self):
        return collect_df()

    def collect_iostat_info(self):
        return collect_iostat()

    def collect_ethtool_info(self, interface="eth0"):
        return collect_ethtool(interface)

    def collect_system_logs(self, lines=100):
        return collect_system_log(lines)

    def collect_kernel_logs(self, lines=100):
        return collect_kernel_log(lines)

    def collect_app_logs(self, path, lines=100):
        return collect_app_log(path, lines)