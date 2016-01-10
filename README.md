# randtool - a secure random number generator "swiss army knife"
0.0.0-ALPHA (Do not use yet, in development) - 9 January 2016

`randtool` is a command line program to generate secure random data, and then transform the data in various ways. One important feature of `randtool` is that it can create deterministic ("seeded") output that can be recreated later if you have the parameters. Of course, the program can also output non-parametrized, non-deterministic ("random") data, that change between invocations.

### Security Warning

`randtool` can be used in dangerous ways if you are not careful. Please only use this program if you know what you are doing. :-)

## Install

    pip install {argon2,pycrypto,scrypt} # virtualenv recommended

## Sources and Transformers

`randtool` uses so called *sources* and *transformers* to solve problems. A source is a way of creating bulk random data. A transformer takes this bulk data and transforms it before outputting.

The **random** source: `randtool` uses `/dev/urandom` as the non-deterministic randomness source. This source is specified using the `--random/-r` option.

The **seeded** source: By default, `randtool` uses AES in Counter mode initailized by Argon2i as the parametrized, deterministic randomness source. This source can be specified using the `--seed/-s` option, to initialize the random number generator using the specified string.

The **password-protected** source: If `-p/--password` is given, `randtool` will query for a password and use that together with a salt to seed the random number generator, similar to above.

The most basic transformer, the "nop" transformer, doesn't transform the data at all, it just outputs a byte string from the random source.

    $ randtool -r -n16
	<16 bytes printed>

The `-H/--hex` transformer will output the data as a hex string (this is not a very useful transformer, except for illustration purposes). Notice the behavior of the random source compared to the seeded source:

    $ randtool -r -n16 --hex
    58ddf4d157e9a7bd42929a3a9845a8db
    $ randtool -r -n16 --hex
    9734d4d43c2d82911a791aa837f65ba8
	
    $ randtool --seed=foo -n16 --hex
    c1dc7a7aae61eff1abed96a3d038ec13
    $ randtool --seed=foo -n16 --hex
    c1dc7a7aae61eff1abed96a3d038ec13
	
    $ randtool -p -n16 --hex
    Password:
    1a4a5c80aab1db7f0acdb4d90ad7b44b

## Usage

### The XOR Transformer

`randtool` can be used to encrypt/decrypt files using the XOR transformer, as specified by the `--xor/-x` option. This is best used together with the **password-protected** source. The encryption/decryption can be either done in-place or written to a new file.

### The Integer Transformer

Create 5 integers in the range [0, 100):

    $ mkrand --seed=abc -I0-100 -n5
    64
    91
    83
    95
    80

Roll a dice:

    $ randtool -r -I1-7 -n1
    6

### The Choice Transformer

Select from a set of choices:

    $ randtool -r -C 'Ardbeg 10' 'Tomintoul 14' 'Glen Scotia 18'
    Tomintoul 14

### The Password Recipe

The password-protected source together with the nop transformer and the `--salt` option can bse used to derive domain specific passwords from a "master" password:

    $ randtool -p --salt=reddit -n15 | base64
    Password:
    kBzBMW4yTS4MddGiyHBa

## About and License

`randtool` is written by Björn Edström in 2016. See LICENSE for details.
