# -----------------------------------------------------------------------------
# Copyright (c) 2014--, The Qiita Development Team.
#
# Distributed under the terms of the BSD 3-clause License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------

from unittest import TestCase, main
from os import getcwd

from qp_target_gene.util import system_call


class UtilTests(TestCase):
    def test_system_call(self):
        obs_out, obs_err, obs_val = system_call("pwd")
        self.assertEqual(obs_out, "%s\n" % getcwd())
        self.assertEqual(obs_err, "")
        self.assertEqual(obs_val, 0)

    def test_system_call_error(self):
        obs_out, obs_err, obs_val = system_call("IHopeThisCommandDoesNotExist")
        self.assertEqual(obs_out, "")
        self.assertTrue("not found" in obs_err)
        self.assertEqual(obs_val, 127)


if __name__ == '__main__':
    main()
