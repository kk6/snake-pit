# -*- coding: utf-8 -*-
"""Distributions"""

from __future__ import absolute_import, division, print_function, unicode_literals

import distlib.database

from .exceptions import DistributionNotFound


distlib.database.METADATA_FILENAME = 'metadata.json'


class DistFinder(object):

    def __init__(self, white_list=()):
        self.dist_path = distlib.database.DistributionPath()
        self.white_list = white_list

    def get_installed_distributions(self):
        """Return installed distributions.

        :return: Installed distributions.
        :rtype: generator

        """
        return self.dist_path.get_distributions()

    def get_distribution(self, name):
        """Return distribution.

        :param name: Distribution name.
        :return: A distribution.

        """
        return self.dist_path.get_distribution(name)

    def get_requires_recursively(self, dists, dist):
        """Return required distributions recursively.

        :param dists: Installed distributions
        :param dist: A distribution.
        :rtype: list

        """
        dependencies = [dist]
        required_dists = distlib.database.get_required_dists(dists, dist)
        for required_dist in required_dists:
            dependencies.extend(self.get_requires_recursively(dists, required_dist))
        return dependencies

    def get_dependencies(self, name):
        """Return all dependency distributions.

        :param name: Distribution name.
        :return: All dependency distributions.
        :rtype: list

        """
        dists = list(self.get_installed_distributions())
        dist = self.get_distribution(name)
        if not dist:
            raise DistributionNotFound("Distribution not found: {}".format(name))
        return self.get_requires_recursively(dists, dist)

    def get_deletable_dist_set(self, name):
        """Return deletable distributions by set.

        :param name: Distribution name.
        :return: Deletable distribution name set.
        :rtype: set

        """
        #
        # FIXME: Despite the deletable package, there is not picked up the case.
        # If you remove specify multiple packages, no package only they are
        # dependent has been determined to be deleted .
        #
        dists = list(self.get_installed_distributions())
        uninstall_candidates = self.get_dependencies(name)
        remaining_dist_set = {d.key for d in dists} - {d.key for d in uninstall_candidates}
        cannot_delete_dists = []
        for non_required in remaining_dist_set:
            cannot_delete_dists.extend(self.get_dependencies(non_required))
        deletable_dist_set = {d.key for d in uninstall_candidates} - {d.key for d in cannot_delete_dists}
        deletable_dist_set.add(name)
        return deletable_dist_set.difference(self.white_list)

    def choose_installed(self, names):
        """Return a set of installed distributions.

        :param names: Distribution names.
        :return: Installed distribution names.
        :rtype: set

        """
        return set(names) & {d.key for d in self.get_installed_distributions()}

    def choose_not_installed(self, names):
        """Return a set of not installed distributions.

        :param names: Distribution names.
        :return: Not installed distribution names.
        :rtype: set

        """
        return set(names) - {d.key for d in self.get_installed_distributions()}
