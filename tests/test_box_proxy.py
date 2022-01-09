from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import (
    network,
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    BoxV2,
)


def test_proxy_delegates_call():
    acc = get_account()
    box = Box.deploy({"from": acc})
    proxy_admin = ProxyAdmin.deploy({"from": acc})
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": acc},
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    assert proxy_box.retrieve() == 0
    proxy_box.store(69, {"from": acc})
    assert proxy_box.retrieve() == 69
