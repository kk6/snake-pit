# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import, unicode_literals

import click


class AliasedGroup(click.Group):

    def _get_matched_commands(self, ctx, cmd):
        return [x for x in self.list_commands(ctx) if x.startswith(cmd)]

    def _get_command(self, ctx, cmd_name):
        return click.Group.get_command(self, ctx, cmd_name)

    def get_command(self, ctx, cmd_name):
        """Get command by aliased command name"""

        cmd = self._get_command(ctx, cmd_name)
        if cmd is not None:
            return cmd
        matches = self._get_matched_commands(ctx, cmd_name)
        if not matches:
            return None
        elif len(matches) == 1:
            return self._get_command(ctx, matches[0])
        ctx.fail('Too many matches: {}'.format(', '.join(sorted(matches))))
