from pathlib import Path

import pytest
import yaml

from brownie import compile_source

PACKAGE_VERSION = yaml.safe_load(
    (Path(__file__).parents[3] / "ethpm-config.yaml").read_text()
)["version"]


VAULT_SOURCE_CODE = (Path(__file__).parents[3] / "contracts/Vault.vy").read_text()


def patch_vault_version(version):
    source = VAULT_SOURCE_CODE.replace(PACKAGE_VERSION, version)
    return compile_source(source).Vyper


@pytest.fixture
def create_token(gov, Token):
    def create_token():
        return Token.deploy({"from": gov})

    yield create_token


@pytest.fixture
def create_vault(gov):
    def create_vault(token, version=PACKAGE_VERSION):
        vault = patch_vault_version(version).deploy({"from": gov})
        vault.initialize(
            token, gov, f"Yearn {token.name()} Vault", f"yv{token.symbol()}"
        )
        return vault

    yield create_vault


@pytest.fixture
def registry(gov, Registry):
    yield Registry.deploy({"from": gov})
