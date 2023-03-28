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
import nova.conf
from nova import utils
from nova.virt.libvirt.volume import volume as libvirt_volume
from os_brick import initiator
from os_brick.initiator import connector
from oslo_log import log as logging


LOG = logging.getLogger(__name__)
CONF = nova.conf.CONF


class LibvirtLocalVolumeDriver(libvirt_volume.LibvirtVolumeDriver):
    """Class for volumes backed by local file."""

    def __init__(self, host):
        super(LibvirtLocalVolumeDriver, self).__init__(host)

        self.connector = connector.InitiatorConnector.factory(
            initiator.LOCAL, utils.get_root_helper())

    def connect_volume(self, connection_info, instance):
        """Attach the volume to instance_name."""
        LOG.debug("Calling os-brick to attach local Volume", instance=instance)
        device_info = self.connector.connect_volume(connection_info['data'])
        LOG.debug("Attached local volume %s", device_info, instance=instance)

        connection_info['data']['device_path'] = device_info['path']

    def disconnect_volume(self, connection_info, instance, force=False):
        """Detach the volume from instance_name."""
        LOG.debug("calling os-brick to detach local Volume", instance=instance)
        self.connector.disconnect_volume(connection_info['data'], None, force=force)
        LOG.debug("Disconnected local Volume", instance=instance)

    def extend_volume(self, connection_info, instance, requested_size):
        """Extend the volume."""
        LOG.debug("calling os-brick to extend local Volume", instance=instance)
        new_size = self.connector.extend_volume(connection_info['data'])
        LOG.debug("Extend local Volume: new_size=%s",
                  new_size, instance=instance)
        return new_size
