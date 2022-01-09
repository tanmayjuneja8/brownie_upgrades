from scripts.helpful_scripts import get_account, encode_function_data, upgrade
from brownie import (
    network,
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    BoxV2,
)


def main():
    acc = get_account()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy({"from": acc}, publish_source=True)

    # proxy starts

    proxy_admin = ProxyAdmin.deploy({"from": acc}, publish_source=True)
    #  initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": acc, "gas_limit": 1000000},
        publish_source=True,
    )
    print(f"Proxy deployed to {proxy}. You can now upgrade to V2.")
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, {"from": acc})
    print(proxy_box.retrieve())

    # BoxV2 deploy and upgrade
    boxV2 = BoxV2.deploy({"from": acc}, publish_source=True)
    # upgrade
    upgrade_transaction = upgrade(
        acc,
        proxy,
        boxV2.address,
        proxy_admin_contract=proxy_admin,
    )
    upgrade_transaction.wait(1)
    print("Proxy has been upgraded!")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.increment({"from": acc})
    print(proxy_box.retrieve())
