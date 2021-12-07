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

##### Sign a verifiable credential

<details>
  <summary>doc</summary>

````python
doc = {
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://w3id.org/citizenship/v1",
    "https://w3id.org/security/bbs/v1"
  ],
  "id": "https://issuer.oidp.uscis.gov/credentials/83627465",
  "type": [
    "VerifiableCredential",
    "PermanentResidentCard"
  ],
  "issuer": "did:example:489398593",
  "identifier": "83627465",
  "name": "Permanent Resident Card",
  "description": "Government of Example Permanent Resident Card.",
  "issuanceDate": "2019-12-03T12:19:52Z",
  "expirationDate": "2029-12-03T12:19:52Z",
  "credentialSubject": {
    "id": "did:example:b34ca6cd37bbf23",
    "type": [
      "PermanentResident",
      "Person"
    ],
    "givenName": "JOHN",
    "familyName": "SMITH",
    "gender": "Male",
    "image": "data:image/png;base64,iVBORw0KGgokJggg==",
    "residentSince": "2015-01-01",
    "lprCategory": "C09",
    "lprNumber": "999-999-999",
    "commuterClassification": "C1",
    "birthCountry": "Bahamas",
    "birthDate": "1958-07-17"
  }
}

result = asyncio.run(mw.sign(jdoc = doc))
````
</details>



#### Verify a signature

<details>
  <summary>doc</summary>

````python
doc = {
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://w3id.org/citizenship/v1",
    "https://w3id.org/security/bbs/v1"
  ],
  "id": "https://issuer.oidp.uscis.gov/credentials/83627465",
  "type": [
    "VerifiableCredential",
    "PermanentResidentCard"
  ],
  "issuer": "did:example:489398593",
  "identifier": "83627465",
  "name": "Permanent Resident Card",
  "description": "Government of Example Permanent Resident Card.",
  "issuanceDate": "2019-12-03T12:19:52Z",
  "expirationDate": "2029-12-03T12:19:52Z",
  "credentialSubject": {
    "id": "did:example:b34ca6cd37bbf23",
    "type": [
      "PermanentResident",
      "Person"
    ],
    "givenName": "JOHN",
    "familyName": "SMITH",
    "gender": "Male",
    "image": "data:image/png;base64,iVBORw0KGgokJggg==",
    "residentSince": "2015-01-01",
    "lprCategory": "C09",
    "lprNumber": "999-999-999",
    "commuterClassification": "C1",
    "birthCountry": "Bahamas",
    "birthDate": "1958-07-17"
  },
  "proof": {
    "type": "BbsBlsSignature2020",
    "created": "2020-10-16T23:59:31Z",
    "proofPurpose": "assertionMethod",
    "proofValue": "kAkloZSlK79ARnlx54tPqmQyy6G7/36xU/LZgrdVmCqqI9M0muKLxkaHNsgVDBBvYp85VT3uouLFSXPMr7Stjgq62+OCunba7bNdGfhM/FUsx9zpfRtw7jeE182CN1cZakOoSVsQz61c16zQikXM3w==",
    "verificationMethod": "did:example:489398593#test"
  }
}
````
</details>

````
result = asyncio.run(mw.verify(jdoc = doc))
````

#### Derivation

<details>
  <summary>doc</summary>

````python
doc = [
  {
    "@context": [
      "https://www.w3.org/2018/credentials/v1",
      "https://w3id.org/citizenship/v1",
      "https://w3id.org/security/bbs/v1"
    ],
    "id": "https://issuer.oidp.uscis.gov/credentials/83627465",
    "type": [
      "VerifiableCredential",
      "PermanentResidentCard"
    ],
    "issuer": "did:example:489398593",
    "identifier": "83627465",
    "name": "Permanent Resident Card",
    "description": "Government of Example Permanent Resident Card.",
    "issuanceDate": "2019-12-03T12:19:52Z",
    "expirationDate": "2029-12-03T12:19:52Z",
    "credentialSubject": {
      "id": "did:example:b34ca6cd37bbf23",
      "type": [
        "PermanentResident",
        "Person"
      ],
      "givenName": "JOHN",
      "familyName": "SMITH",
      "gender": "Male",
      "image": "data:image/png;base64,iVBORw0KGgokJggg==",
      "residentSince": "2015-01-01",
      "lprCategory": "C09",
      "lprNumber": "999-999-999",
      "commuterClassification": "C1",
      "birthCountry": "Bahamas",
      "birthDate": "1958-07-17"
    },
    "proof": {
      "type": "BbsBlsSignature2020",
      "created": "2020-10-16T23:59:31Z",
      "proofPurpose": "assertionMethod",
      "proofValue": "kAkloZSlK79ARnlx54tPqmQyy6G7/36xU/LZgrdVmCqqI9M0muKLxkaHNsgVDBBvYp85VT3uouLFSXPMr7Stjgq62+OCunba7bNdGfhM/FUsx9zpfRtw7jeE182CN1cZakOoSVsQz61c16zQikXM3w==",
      "verificationMethod": "did:example:489398593#test"
    }
  },
  {
    "@context": [
      "https://www.w3.org/2018/credentials/v1",
      "https://w3id.org/citizenship/v1",
      "https://w3id.org/security/bbs/v1"
    ],
    "id": "https://issuer.oidp.uscis.gov/credentials/83627465",
    "type": [
      "VerifiableCredential",
      "PermanentResidentCard"
    ],
    "@explicit": true,
    "issuer": "did:example:489398593",
    "identifier": "83627465",
    "name": "Permanent Resident Card",
    "description": "Government of Example Permanent Resident Card.",
    "issuanceDate": "2019-12-03T12:19:52Z",
    "expirationDate": "2029-12-03T12:19:52Z",
    "credentialSubject": {
      "id": "did:example:b34ca6cd37bbf23",
      "type": [
        "PermanentResident",
        "Person"
      ],
      "@explicit": true,
      "givenName": "JOHN",
      "familyName": "SMITH",
      "gender": "Male"
    }
  }
]
````
</details>

````
result = asyncio.derive(mw.verify(jdoc = doc[0], reveal_doc = doc[1]))
````

<details>
  <summary>Result of derivation</summary>

````python
{
  "@context": [
    "https://www.w3.org/2018/credentials/v1",
    "https://w3id.org/citizenship/v1",
    "https://w3id.org/security/bbs/v1"
  ],
  "id": "https://issuer.oidp.uscis.gov/credentials/83627465",
  "type": [
    "PermanentResidentCard",
    "VerifiableCredential"
  ],
  "description": "Government of Example Permanent Resident Card.",
  "identifier": "83627465",
  "name": "Permanent Resident Card",
  "credentialSubject": {
    "id": "did:example:b34ca6cd37bbf23",
    "type": [
      "Person",
      "PermanentResident"
    ],
    "familyName": "SMITH",
    "gender": "Male",
    "givenName": "JOHN"
  },
  "expirationDate": "2029-12-03T12:19:52Z",
  "issuanceDate": "2019-12-03T12:19:52Z",
  "issuer": "did:example:489398593",
  "proof": {
    "type": "BbsBlsSignatureProof2020",
    "nonce": "FaR1EJ0C580Eet7U8WAaMjYW3b8e/8k5j1wcvYip9i6Hi6EepB5Qr5CeoasCNfmS+/A=",
    "proofValue": "ABkB/wbvkJBC7TokHbS41THvK3mfjFfWd8VHuXoaenZ/xlleUOE7IJGtkGBe7Sdc5J/vD/Zyid+jvDS6hvSKyPccZP5bu/CctSA/Pq15Nm2EeI25KgENn9ePmR9Y11pMUJyXZivMrvI/rD49Q6FgHCQImwhSudGwjPRJYXM5Yo0ay6ovo/0ONfH7DB/FxQfHNdoh/hmhAAAAdLK7ZoIKJBpxUbVegQ+KXPrwxJtZVs1kq3uYq5xbIWSmU1uIdaPIenoPp7ec0D2MvQAAAAIofW9lTpXdP4fRJf1TqvKILwCRlZh+JgJoXEc2E8wJmF2O0kZCd5g5LM376UdM8kAiFr4D6/Z1QPSEK/SFrhh6kBQeGrldWL9m9Wagnpvkt0E/WZ5xv3gdmQt8Hq0J8NsH+ChBm5Nbva4n3O6zxeCnAAAACTHEoId6WsjjwPdOHQYshLKg2ttg23MS2iIFd4U3323HUrrHs10QaKbQIccXCUV8xmIlgWIHpYaYq9CCOVDuIq9Iuo5fe25ZOY5GceeJ7LhhLOvG6ZGFtRMOU81uUEc46iRNUrxoQUh9f/UyCF/QxFwnx7Z0PNYoooVgV6iTfZv8N26DT0SJDQNWCxGZ7VaqeD5QNQC9D/zeGo27FD99g44jQ2AuUrZyhJVIAA/xNsrO3TEKNWxcQWzTsRYuQKtUGEsdyrmE6xMMBbrN1vuibRO2oecAzdWzP6V2ZjTfK7v4IiFr1l+MYsftEQHtwR0Ahf9mUdnyWdCakRpEI2DM2xgcKz8T/f8WGBjhxShcg2sVtJENRloWPYRjCFsERIK/Ow==",
    "verificationMethod": "did:example:489398593#test",
    "proofPurpose": "assertionMethod",
    "created": "2020-10-16T23:59:31Z"
  }
}
````
</details>


setup
-----

````
pip install pyeidwallet
````

references
----------

- [BBS+ Signatures 2020](https://w3c-ccg.github.io/ldp-bbs2020/)
- [Verifiable Credentials Implementation Guidelines 1.0](https://w3c.github.io/vc-imp-guide/#zero-knowledge-proofs)

authors
-------

Giuseppe De Marco
