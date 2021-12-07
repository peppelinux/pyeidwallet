python eID Wallet
-----------------

Python PoC to get a proof of features of a eid digital wallet

stack
-----

- [hyperledger/aries-cloudagent-python](https://github.com/hyperledger/aries-cloudagent-python)


poc
---

````
import asyncio
from pyediwallet.wallet import MyWallet

_PRIV_KEY_BASE58 = "5D6Pa8dSwApdnfg7EZR8WnGfvLDCZPZGsZ5Y1ELL9VDj"
_PUB_KEY_BASE58 = "oqpWYKaZD9M1Kbe94BVXpr8WTdFBNZyKv48cziTiQUeuhm7sBhCABMyYG4kcMrseC68YTFFgyhiNeBKjzdKk9MiRWuLv5H4FFujQsQK2KTAtzU8qTBiZqBHMmnLF4PL7Ytu"

mw = MyWallet(
    priv_key = _PRIV_KEY_BASE58,
    pub_key = _PUB_KEY_BASE58
)
````

setup
-----

````
pip install pyeidwallet
````


authors
-------

Giuseppe De Marco
