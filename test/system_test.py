# -*- coding: utf-8 -*-
# Copyright (C) 2016 by Björn Edström <be@bjrn.se>
# See LICENSE for details.

import unittest
import subprocess


def run(cmd):
    out, err = subprocess.Popen(
        cmd, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE).communicate()
    return (out, err)


class SystemTest(unittest.TestCase):
    def test_random_source(self):
        out, err = run(['randtool', '-r', '-n', '16'])
        self.assertEquals(16, len(out))
        self.assertEquals('', err)

        out2, err = run(['randtool', '-r', '-n', '16'])
        self.assertEquals(16, len(out2))
        self.assertEquals('', err)

        self.assertTrue(out != out2)

    def test_seeded_source(self):
        out, err = run(['randtool', '-s', 'foo', '-n', '16'])
        self.assertEquals(16, len(out))
        self.assertEquals('', err)

        out2, err = run(['randtool', '-s', 'foo', '-n', '16'])
        self.assertEquals(16, len(out2))
        self.assertEquals('', err)

        self.assertTrue(out == out2)

    def test_seeded_source_kat(self):
        out, err = run(['randtool', '-s', 'foo', '-n', '20'])
        self.assertEquals(b'yh1m\xd1r\xe4m\xc0\xc8\xe8\x1dz\x98%\xa9\x94\xf7g\xa0', out)
        self.assertEquals('', err)

    def test_password_source(self):
        raise NotImplementedError('fixme')

    def test_xor(self):
        plaintext = b'foo bar test abcdef 1234567'
        with file('/tmp/randtool.xortest', 'w') as fobj:
            fobj.write(plaintext)
        out, err = run(['randtool', '-s', 'foo', '-n', '5', '--xor', '/tmp/randtool.xortest', '-o', '/tmp/randtool.xortest.enc'])
        self.assertTrue(not err)
        self.assertTrue(not out)

        with file('/tmp/randtool.xortest.enc', 'r') as fobj:
            ciphertext = fobj.read()

        out, err = run(['randtool', '-s', 'foo', '-n', '5', '--xor', '/tmp/randtool.xortest.enc'])

        self.assertEquals(plaintext, out)

    def test_xor_inplace(self):
        plaintext = b'foo bar test abcdef 1234567'
        with file('/tmp/randtool.xortest', 'w') as fobj:
            fobj.write(plaintext)
        out, err = run(['randtool', '-s', 'foo', '--xor', '/tmp/randtool.xortest', '-o', 'inplace'])
        self.assertTrue(not err)
        self.assertTrue(not out)

        with file('/tmp/randtool.xortest', 'r') as fobj:
            ciphertext = fobj.read()

        self.assertTrue(plaintext != ciphertext)

        out, err = run(['randtool', '-s', 'foo', '--xor', '/tmp/randtool.xortest', '-o', 'inplace'])
        self.assertTrue(not err)
        self.assertTrue(not out)

        with file('/tmp/randtool.xortest', 'r') as fobj:
            plaintext2 = fobj.read()

        self.assertEquals(plaintext, plaintext2)


if __name__ == '__main__':
    unittest.main()
