# -*- coding: utf-8 -*-
"""Distributions"""

from __future__ import absolute_import, division, print_function, unicode_literals

import distlib.database
import pip

from .exceptions import DistributionNotFound


distlib.database.METADATA_FILENAME = 'metadata.json'


def get_installed_package_set():
    """Return installed packages.

    :return: Installed packages.
    :rtype: set

    """
    return {p.key for p in pip.get_installed_distributions()}


class DistFinder(object):

    def __init__(self):
        self.dist_path = distlib.database.DistributionPath()

    def get_installed_distributions(self):
        return self.dist_path.get_distributions()

    def get_distribution(self, name):
        return self.dist_path.get_distribution(name)

    def get_required_dists_recursively(self, dists, dist):
        """Return required distributions recursively.

        :param dists: Installed distributions
        :param dist: A distribution.

        """
        dependencies = [dist]
        required_dists = distlib.database.get_required_dists(dists, dist)
        for required_dist in required_dists:
            dependencies.extend(self.get_required_dists_recursively(dists, required_dist))
        return dependencies

    def get_dependencies(self, name):
        dists = list(self.get_installed_distributions())
        dist = self.get_distribution(name)
        if not dist:
            raise DistributionNotFound("Distribution not found: {}".format(name))
        return self.get_required_dists_recursively(dists, dist)


def classify_installed_or_not(packages):
    """Classify packages installed or not.

    :param packages: Passed packages by user.
    :return: Install candidates and installed packages.
    :rtype: tuple

    """
    installed = get_installed_package_set()
    will_install = set(packages) - installed
    need_upgrade = set(packages) & installed
    return will_install, need_upgrade
