# Copyright 2012 Cloudbase Solutions Srl
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import sys

from oslo_config import cfg

from cloudbaseinit import init
from cloudbaseinit.utils import log as logging

CONF = cfg.CONF


def main():
    CONF(sys.argv[1:])
    logging.setup('cloudbaseinit')

    init.InitManager().configure_host()


if __name__ == "__main__":
    main()
