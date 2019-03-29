from cloudbaseinit.osutils import factory as osutils_factory
from cloudbaseinit.plugins.common import base
from cloudbaseinit.openstack.common import log as logging

import re
import subprocess
import time

LOG = logging.getLogger(__name__)

class EnlargeRoot(base.BasePlugin):
    def _call_shell(self, cmd):
        return subprocess.check_call(cmd, stderr=subprocess.STDOUT, shell=True)

    def _call_shell_output(self, cmd):
        return subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)

    def execute(self, service, shared_data):
        rootdisk = 'vtbd0'

        # We might have swap before the root partition
        gpart_output = self._call_shell_output('gpart show -p ' + rootdisk)
        regex = rootdisk + r'p(?P<part>[0-9]+)\s+freebsd-(?P<fs>(u|z)fs)'
        match = re.search(regex, gpart_output)
        partition = match.group('part')
        filesystem = match.group('fs')

        self._call_shell('gpart recover ' + rootdisk)
        self._call_shell('sysctl kern.geom.debugflags=16')
        self._call_shell('gpart resize -i ' + partition + ' ' + rootdisk)

        if filesystem == 'ufs':
            # Get the gptid value as: gptid/83ff5607-b603-11e8-b952-4fd92016f579
            gptid = self._call_shell_output('/sbin/glabel status | awk \'/' + rootdisk + 'p' + partition + '/ {print $1 }\'')
            for i in range(1,7):
                try:
                    self._call_shell('growfs -y /dev/' + gptid)
                    break
                except subprocess.CalledProcessError:
                    print 'Error growing the root disk. Retrying ... ' + str(i) +'/6'
                    time.sleep(1)
                    continue
            # just to claim the pfsense menu console
            self._call_shell('exec /etc/rc.initial')
        elif filesystem == 'zfs':
            self._call_shell('zpool set autoexpand=on zroot')
            self._call_shell('zpool online -e zroot ' + rootdisk + 'p' + partition)
        return (base.PLUGIN_EXECUTION_DONE, False)
