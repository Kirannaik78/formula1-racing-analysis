import pulumi
from pulumi_azure_native import containerservice
import pulumi_kubernetes as k8s
from typing import TypedDict
from pulumi import Output

class AksComponentArgs(TypedDict):
    """
    Input arguments for the Aks cluster Component.
    """

    resource_group_name: pulumi.Input[str]
    aks_subnet_id: pulumi.Input[str]
    location: pulumi.Input[str]
    prefix: pulumi.Input[str]
    kubernetes_version: pulumi.Input[str]
    dns_prefix: pulumi.Input[str]


class AksComponent(pulumi.ComponentResource):
    """
    Provisions a private AKS cluster and creates the Kubernetes Provider.
    """

    def __init__(self, name: str, args: AksComponentArgs, opts: pulumi.ResourceOptions = None):
        super().__init__("custom:infra:AksComponent", name, args, opts)

        self.cluster = containerservice.ManagedCluster(
            f"{name}-aks",
            resource_group_name=args['resource_group_name'],
            location=args['location'],
            api_server_access_profile=containerservice.ManagedClusterAPIServerAccessProfileArgs(
                enable_private_cluster=False,
            ),
            network_profile=containerservice.ContainerServiceNetworkProfileArgs(
                network_plugin='azure',
                service_cidr="10.20.0.0/16",
                dns_service_ip="10.20.0.10",
            ),
            agent_pool_profiles=[
                containerservice.ManagedClusterAgentPoolProfileArgs(
                    name='systempool',
                    count=3,
                    vm_size="Standard_D2s_v3",
                    os_type="Linux",
                    mode="System",
                    vnet_subnet_id=args["aks_subnet_id"]
                )
            ],
            dns_prefix=args['dns_prefix'],
            identity=containerservice.ManagedClusterIdentityArgs(type='SystemAssigned'),
            opts=pulumi.ResourceOptions(parent=self)
        )

        creds = Output.all(args['resource_group_name'], self.cluster.name).apply(
            lambda args: containerservice.list_managed_cluster_user_credentials(
                resource_group_name=args[0],
                resource_name=args[1],
            )
        )

        self.kubeconfig = creds.kubeconfig[0].value.apply(
            lambda enc: str(enc).encode('base64').decode('utf8')
        )

        self.k8s_provider = k8s.Provider(
            f'{name}-k8s-provider',
            kubeconfig=self.kubeconfig,
            opts=pulumi.ResourceOptions(depends_on=[self.cluster, self]),
        )

        self.register_outputs({
            'aks_cluster_name': self.cluster.name,
            'kubeconfig': pulumi.Output.secret(self.kubeconfig),
            'k8s_provider': self.k8s_provider
        })