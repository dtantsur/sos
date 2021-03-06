# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from sos.plugins import Plugin, RedHatPlugin, DebianPlugin, UbuntuPlugin


class Apache(Plugin):
    """Apache http daemon
    """
    plugin_name = "apache"
    profiles = ('webserver', 'openshift')

    option_list = [
        ("log", "gathers all apache logs", "slow", False)
    ]

    def setup(self):
        # collect list of installed modules
        self.add_cmd_output(["apachectl -M"])


class RedHatApache(Apache, RedHatPlugin):
    files = (
        '/etc/httpd/conf/httpd.conf',
        '/etc/httpd22/conf/httpd.conf',
        '/etc/httpd24/conf/httpd.conf'
    )

    def setup(self):
        super(RedHatApache, self).setup()

        self.add_copy_spec([
            "/etc/httpd/conf/httpd.conf",
            "/etc/httpd/conf.d/*.conf",
            "/etc/httpd/conf.modules.d/*.conf",
            # JBoss Enterprise Web Server 2.x
            "/etc/httpd22/conf/httpd.conf",
            "/etc/httpd22/conf.d/*.conf",
            # Red Hat JBoss Web Server 3.x
            "/etc/httpd24/conf/httpd.conf",
            "/etc/httpd24/conf.d/*.conf",
            "/etc/httpd24/conf.modules.d/*.conf",
        ])

        self.add_forbidden_path("/etc/httpd/conf/password.conf")

        # determine how much logs to collect
        self.limit = None if self.get_option("all_logs") else 5

        # collect only the current log set by default
        self.add_copy_spec("/var/log/httpd/access_log", self.limit)
        self.add_copy_spec("/var/log/httpd/error_log", self.limit)
        self.add_copy_spec("/var/log/httpd/ssl_access_log", self.limit)
        self.add_copy_spec("/var/log/httpd/ssl_error_log", self.limit)
        # JBoss Enterprise Web Server 2.x
        self.add_copy_spec("/var/log/httpd22/access_log", self.limit)
        self.add_copy_spec("/var/log/httpd22/error_log", self.limit)
        self.add_copy_spec("/var/log/httpd22/ssl_access_log", self.limit)
        self.add_copy_spec("/var/log/httpd22/ssl_error_log", self.limit)
        # Red Hat JBoss Web Server 3.x
        self.add_copy_spec("/var/log/httpd24/access_log", self.limit)
        self.add_copy_spec("/var/log/httpd24/error_log", self.limit)
        self.add_copy_spec("/var/log/httpd24/ssl_access_log", self.limit)
        self.add_copy_spec("/var/log/httpd24/ssl_error_log", self.limit)
        if self.get_option("log") or self.get_option("all_logs"):
            self.add_copy_spec([
                "/var/log/httpd/*",
                # JBoss Enterprise Web Server 2.x
                "/var/log/httpd22/*",
                # Red Hat JBoss Web Server 3.x
                "/var/log/httpd24/*"
            ])


class DebianApache(Apache, DebianPlugin, UbuntuPlugin):
    files = ('/etc/apache2/apache2.conf',)

    def setup(self):
        super(DebianApache, self).setup()
        self.add_copy_spec([
            "/etc/apache2/*",
            "/etc/default/apache2"
        ])

        # determine how much logs to collect
        self.limit = None if self.get_option("all_logs") else 15

        # collect only the current log set by default
        self.add_copy_spec("/var/log/apache2/access_log", self.limit)
        self.add_copy_spec("/var/log/apache2/error_log", self.limit)
        if self.get_option("log") or self.get_option("all_logs"):
            self.add_copy_spec("/var/log/apache2/*")

# vim: set et ts=4 sw=4 :
