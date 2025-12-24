import pulumi
from pulumi_azure_native import resources
from components.network.network_component import NetworkComponentArgs, NetworkComponent
from components.aks.aks_component import AksComponentArgs, AksComponent


kafka_config = pulumi.Config("kafka-config")
config = pulumi.Config('azure')


resource_group = resources.ResourceGroup(
    f"{config.get('prefix')}-rg",
    resource_group_name=f"{config.get('prefix')}-rg",
    location=config.get('location')
)

network_args = NetworkComponentArgs(
    resource_group_name = resource_group.name,
    vnet_cidr = config.get('vnet'),
    aks_subnet_cidr = kafka_config.get('subnet_cidr'),
    location= config.get('location'),
    prefix = kafka_config.get('prefix'),
)

network_infra = NetworkComponent(
    f'{kafka_config.get('prefix')}-net',
    network_args,
    opts=pulumi.ResourceOptions(depends_on=[resource_group])
)

# 3. Provision AKS Cluster

aks_args = AksComponentArgs(
    resource_group_name=resource_group.name,
    aks_subnet_id=network_infra.aks_subnet.id,
    location=config.get('location'),
    prefix=kafka_config.get('prefix'),
    kubernetes_version=kafka_config.get('kubernetes_version'),
    dns_prefix=kafka_config.get('prefix')
)

aks_infra = AksComponent(
    f"{kafka_config.get('prefix')}-cluster",
    aks_args,
    opts=pulumi.ResourceOptions(depends_on=[network_infra])
)

pulumi.export("resource_group_name", resource_group.name)
pulumi.export("vnet_name", network_infra.vnet.name)
pulumi.export("aks_subnet_id", network_infra.aks_subnet.id)
