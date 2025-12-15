import pulumi
from pulumi_azure_native import network
from typing import TypedDict
from dataclasses import dataclass

@dataclass(frozen=True)
class NetworkComponentArgs(TypedDict):
    """
    Input arguments for the Network Component.
    """
    resource_group_name: pulumi.Input[str]
    vnet_cidr: pulumi.Input[str]
    aks_subnet_cidr: pulumi.Input[str]
    location: pulumi.Input[str]
    prefix: pulumi.Input[str]


class NetworkComponent(pulumi.ComponentResource):
    """
    A reusable component to provision a complete Azure Vnet with subnet.
    """

    def __init__(self, name, args: NetworkComponentArgs, opts=None):
        super().__init__('custom:infra:NetworkComponent', name, args, opts)

        self.vnet = network.VirtualNetwork(
            f"{name}-vnet",
            resource_group_name=args['resource_group_name'],
            address_space=network.AddressSpaceArgs(
                address_prefixes=[args['vnet_cidr']]
            ),
            opts=pulumi.ResourceOptions(parent=self)
        )
        self.nat_public_ip = network.PublicIPAddress(
            f"{name}-nat-pip",
            resource_group_name=args['resource_group_name'],
            public_ip_allocation_method="Static",
            sku=network.PublicIPAddressSkuArgs(name='Standard'),
            opts=pulumi.ResourceOptions(parent=self)
        )
        self.nat_gateway = network.NatGateway(
            f"{name}-nat-gw",
            resource_group_name=args['resource_group_name'],
            location=args['location'],
            sku=network.NatGatewaySkuArgs(name="Standard"),
            public_ip_addresses=[network.SubResourceArgs(id=self.nat_public_ip.id)],
            opts=pulumi.ResourceOptions(parent=self)
        )

        self.aks_subnet = network.Subnet(
            f"{name}-aks-snet",
            resource_group_name=args['resource_group_name'],
            virtual_network_name = self.vnet.name,
            subnet_name = 'aks-subnet',
            address_prefix=args['aks_subnet_cidr'],
            private_endpoint_network_policies="Disabled",
            private_link_service_network_policies="Disabled",
            nat_gateway=network.SubResourceArgs(id=self.nat_gateway.id),
            opts=pulumi.ResourceOptions(parent=self.vnet),
            
        )

        self.register_outputs({
            "vnet_name": self.vnet.name,
            "aks_subnet_id": self.aks_subnet.id,
            "nat_egress_id":self.nat_public_ip.ip_address,
        })

