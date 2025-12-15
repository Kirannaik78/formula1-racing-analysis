import pulumi
from pulumi_azure_native import resources
from components.network.network_component import NetworkComponentArgs, NetworkComponent

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