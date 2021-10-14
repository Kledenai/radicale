from ldap3 import Server, Connection, ALL
from radicale import rights
from radicale.storage import sanitize_path

name = "radicale-rights-ldap"


class Rights(rights.BaseRights):
    def __init__(self, configuration, logger):
        super().__init__(configuration, logger)
        self.server = Server(self.configuration.get("rights", "ldap_url"))
        self.base = self.configuration.get("rights", "user_base")
        self.group_base = self.configuration.get("rights", "group_base")
        self.user_attribute = self.configuration.get("rights", "user_attribute")
        self.group_attribute = self.configuration.get("rights", "group_attribute")
        self.group_prefix = self.configuration.get(
            "rights", "group_prefix", fallback=None
        )
        self.filter = self.configuration.get(
            "rights", "ldap_filter", fallback="(objectClass=*)"
        )
        self.scope = self.configuration.get("rights", "ldap_scope", fallback="SUBTREE")
        binddn = self.configuration.get("rights", "ldap_binddn")
        password = self.configuration.get("rights", "ldap_password")
        self.connection = Connection(self.server, binddn, password)
        self.bind()

    def bind(self):
        try:
            self.connection.rebind()
        except Exception as e:
            raise RuntimeError(
                "LDAP rights plugn failed to connect to LDAP server: {}".format(e.args)
            )

    def user_in_group(self, user, group):
        if not self.connection.bound:
            self.bind()
        user_filter = self.user_attribute + "=" + user
        if self.group_prefix is not None:
            group = self.group_prefix + group
        group_filter = "(memberOf={}={},{})".format(
            self.group_attribute, group, self.group_base
        )
        query = "(& ({}) {} {})".format(user_filter, group_filter, self.filter)
        if self.connection.search(self.base, query, search_scope=self.scope):
            return True
        else:
            return False

    def authorized(self, user, path, permissions):
        self.logger.debug(
            "User %r is trying to access path %r. Permissions: %r",
            user,
            path,
            permissions,
        )
        # everybody can access the root collection
        if path == "/":
            self.logger.debug("Accessing root path. Access granted.")
            return True
        user = user or ""
        sane_path = sanitize_path(path)
        sane_path = sane_path.lstrip("/")
        pathowner, subpath = sane_path.split("/", maxsplit=1)
        if user == pathowner:
            self.logger.debug("User %r is pathowner. Access granted.", user)
            return True
        else:
            # Check if pathowner is group of user
            in_group = self.user_in_group(user, pathowner)
            if in_group:
                self.logger.debug(
                    "User %r is in pathowner group %r. Access granted.", user, pathowner
                )
            else:
                self.logger.debug(
                    "Access to path %r is not granted to user %r.", pathowner, user
                )
            return in_group
