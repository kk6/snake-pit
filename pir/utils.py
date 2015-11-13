# -*- coding: utf-8 -*-
import pip


def get_installed_package_set():
    return {p.key for p in pip.get_installed_distributions()}


def classify_installed_or_not(packages):
    installed = get_installed_package_set()
    will_install = set(packages) - installed
    need_upgrade = set(packages) & installed
    return will_install, need_upgrade
