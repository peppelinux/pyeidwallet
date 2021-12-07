from aries_cloudagent.vc.ld_proofs import (
    DocumentVerificationResult,
    WalletKeyPair,
    AssertionProofPurpose,
    verify,
    sign,
    derive,
    BbsBlsSignature2020,
    BbsBlsSignatureProof2020
)

from aries_cloudagent.config.injection_context import InjectionContext
from aries_cloudagent.core.in_memory import InMemoryProfile
from aries_cloudagent.wallet.key_type import KeyType
from aries_cloudagent.wallet.util import b58_to_bytes
from aries_cloudagent.wallet.in_memory import InMemoryWallet

from aries_cloudagent.vc.tests.document_loader import custom_document_loader
from aries_cloudagent.vc.tests.data import (
    BBS_PARTIAL_PROOF_NESTED_VC_MATTR,
    BBS_VC_MATTR,
    BBS_NESTED_VC_MATTR,
    BBS_VC_REVEAL_DOCUMENT_MATTR,
    BBS_PARTIAL_PROOF_VC_MATTR,
    BBS_PROOF_NESTED_VC_MATTR,
    BBS_PROOF_VC_MATTR,
    BBS_SIGNED_NESTED_VC_MATTR,
    BBS_SIGNED_VC_MATTR,
    BBS_NESTED_VC_REVEAL_DOCUMENT_MATTR,
    BBS_NESTED_VC_FULL_REVEAL_DOCUMENT_MATTR,
)


class MyWallet:
    
    def __init__(self, priv_key:str = None, pub_key:str = None, **kwargs):
        self.priv_key = priv_key
        self.pub_key = pub_key
        
        for k,v in kwargs.items():
            setattr(self, k, v)
        
        self.profile = InMemoryProfile(
            context=InjectionContext(
                enforce_typing=False, settings=getattr(self, 'settings', None)
            ),
            name=InMemoryProfile.TEST_PROFILE_NAME, # stupid test-profile name
        )
        
        self.wallet = InMemoryWallet(self.profile)
        self.profile.keys[self.pub_key] = {
            # dummy seed
            "seed": "seed",
            "secret": b58_to_bytes(self.priv_key),
            "verkey": self.pub_key,
            "metadata": {},
            "key_type": KeyType.BLS12381G2,
        }

        for i in ('pub_key', 'priv_key'):
            if not getattr(self, i, None):
                raise Exception(f"{i} is a needed arg")
    
    def get_suites(
            self, 
            vmeth:str = "did:example:489398593#test",
            key_type:str = KeyType.BLS12381G2,
            pub_key:str = None
    ) -> dict:

        if key_type == KeyType.BLS12381G2:
            signature_issuer_suite = BbsBlsSignature2020(
                verification_method=vmeth,
                key_pair=WalletKeyPair(
                    wallet=self.wallet,
                    key_type=key_type,
                    public_key_base58=pub_key or self.pub_key
                )
            )
            signature_suite = BbsBlsSignature2020(
                key_pair=WalletKeyPair(wallet=self.wallet, key_type=key_type),
            )
            proof_suite = BbsBlsSignatureProof2020(
                key_pair=WalletKeyPair(wallet=self.wallet, key_type=key_type)
            )
        else:
            raise NotImplementedError(f"Unknow keytype {key_type}")
        
        return type('SignVerSuite', (), {
            "signature_issuer_suite": signature_issuer_suite,
            "signature_suite": signature_suite,
            "proof_suite": proof_suite
        })
    
    async def sign(self, jdoc:dict, reveal_doc = None) -> dict:
        suites = self.get_suites()
        _data = dict(
            document=jdoc,
            suite=suites.signature_issuer_suite,
            purpose=AssertionProofPurpose(),
            document_loader=custom_document_loader
        )
        result = await sign(**_data)
        return result
    
    async def derive(self, jdoc:dict, reveal_doc) -> dict:
        suites = self.get_suites()
        _data = dict(
            document=jdoc,
            suite=suites.proof_suite,
            reveal_document=reveal_doc,
            document_loader=custom_document_loader
        )
        result = await derive(**_data)
        return result

    async def verify(self, jdoc:dict) -> dict:
        suites = self.get_suites()
        
        _sign_tmap = {
            'BbsBlsSignature2020': suites.signature_suite,
            'BbsBlsSignatureProof2020': suites.proof_suite,
        }
        _suites = [_sign_tmap[jdoc['proof']['type']]]
        _data = dict(
            document=jdoc,
            suites=_suites,
            purpose=AssertionProofPurpose(),
            document_loader=custom_document_loader
        )
        result = await verify(**_data)
        return result
        
if __name__ == '__main__':
    import asyncio
    import json

    _PRIV_KEY_BASE58 = "5D6Pa8dSwApdnfg7EZR8WnGfvLDCZPZGsZ5Y1ELL9VDj"
    _PUB_KEY_BASE58 = "oqpWYKaZD9M1Kbe94BVXpr8WTdFBNZyKv48cziTiQUeuhm7sBhCABMyYG4kcMrseC68YTFFgyhiNeBKjzdKk9MiRWuLv5H4FFujQsQK2KTAtzU8qTBiZqBHMmnLF4PL7Ytu"

    mw = MyWallet(
        priv_key = _PRIV_KEY_BASE58,
        pub_key = _PUB_KEY_BASE58
    )
    
    _actions = {
        'to_be_signed': 'sign',
        'to_be_verified': 'verify',
        'to_be_derived': 'derive'
    }
    
    _docs = {
        'to_be_signed': (
            BBS_VC_MATTR, 
            BBS_NESTED_VC_MATTR, 
            
        ),
        'to_be_verified': (
            BBS_SIGNED_VC_MATTR,
            BBS_SIGNED_NESTED_VC_MATTR,
            BBS_PROOF_VC_MATTR,
            BBS_PARTIAL_PROOF_VC_MATTR,
            BBS_PROOF_NESTED_VC_MATTR,
            BBS_PARTIAL_PROOF_NESTED_VC_MATTR
        ),
        'to_be_derived': (
            (BBS_SIGNED_VC_MATTR, BBS_VC_REVEAL_DOCUMENT_MATTR),
            (BBS_SIGNED_NESTED_VC_MATTR, BBS_NESTED_VC_FULL_REVEAL_DOCUMENT_MATTR),
            (BBS_SIGNED_NESTED_VC_MATTR, BBS_NESTED_VC_REVEAL_DOCUMENT_MATTR)
        )
    }
    # signature examples
    for k,v in _docs.items():
        print(f"{'#'* 25} {k.replace('_', ' ').title()} {'#'* 25}")
        _meth = getattr(mw, _actions[k])
        for _doc in v:
            print(f"given this doc: \n{json.dumps(_doc, indent=2)}")
            
            if isinstance(_doc, dict):
                result = asyncio.run(_meth(jdoc = _doc))
            elif isinstance(_doc, tuple):
                result = asyncio.run(_meth(jdoc = _doc[0], reveal_doc = _doc[1]))
            else:
                raise ValueError(f"{_doc} is an invalid type for this loop!")
                
            if isinstance(result, DocumentVerificationResult):
                if result.errors:
                    # TODO: this exception must be specialized
                    raise Exception(f"Verification raises errors: {result.errors}")
                # verify returns an object
                print("Signature verification OK")
            
            else:
                print(f"resulting: \n{json.dumps(result, indent=2)}")
            print('\n')
    
