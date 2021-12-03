import enum
import typing
from abc import ABC
import random

import pydantic
from pydantic import validator, root_validator

from qhub_tf.version import __version__


class CertificateEnum(str, enum.Enum):
    letsencrypt = "lets-encrypt"
    selfsigned = "self-signed"
    existing = "existing"


class TerraformStateEnum(str, enum.Enum):
    remote = "remote"
    local = "local"
    existing = "existing"


class ProviderEnum(str, enum.Enum):
    local = "local"
    do = "do"
    aws = "aws"
    gcp = "gcp"
    azure = "azure"


class CiEnum(str, enum.Enum):
    github_actions = "github-actions"
    gitlab_ci = "gitlab-ci"
    none = "none"


class AuthenticationEnum(str, enum.Enum):
    password = "password"
    github = "GitHub"
    auth0 = "Auth0"
    custom = "custom"


class Base(pydantic.BaseModel):
    ...

    class Config:
        extra = "forbid"


# ============== CI/CD =============


class CICD(Base):
    type: CiEnum = CiEnum.none
    branch: str = "main"
    before_script: typing.Optional[typing.List[str]]
    after_script: typing.Optional[typing.List[str]]


# ======== Generic Helm Extensions ========
class HelmExtension(Base):
    name: str
    repository: str
    chart: str
    version: str
    overrides: typing.Optional[typing.Dict]


# ============== Monitoring =============


class Monitoring(Base):
    enabled: bool = True


# ============== ClearML =============


class ClearML(Base):
    enabled: bool
    enable_forward_auth: typing.Optional[bool]


# ============== Prefect =============


class Prefect(Base):
    enabled: bool
    image: typing.Optional[str]
    overrides: typing.Optional[typing.Dict]


# ============= Terraform ===============


class TerraformState(Base):
    type: TerraformStateEnum = TerraformStateEnum.remote
    backend: typing.Optional[str]
    config: typing.Optional[typing.Dict[str, str]]


class TerraformModules(Base):
    # No longer used, so ignored, but could still be in qhub-config.yaml
    repository: str
    rev: str


# ============ Certificate =============


class Certificate(Base):
    type: CertificateEnum = CertificateEnum.selfsigned
    # existing
    secret_name: typing.Optional[str]
    # lets-encrypt
    acme_email: typing.Optional[str]
    acme_server: typing.Optional[str]


# ========== Default Images ==============


class DefaultImages(Base):
    jupyterhub: str = f"quansight/qhub-jupyterhub:v{__version__}"
    jupyterlab: str = f"quansight/qhub-jupyterlab:v{__version__}"
    dask_worker: str = f"quansight/qhub-dask-worker:v{__version__}"
    dask_gateway: str = f"quansight/qhub-dask-gateway:v{__version__}"
    conda_store: str = f"quansight/qhub-conda-store:v{__version__}"


# =========== Authentication ==============


class GitHubConfig(Base):
    client_id: str
    client_secret: str


class Auth0Config(Base):
    client_id: str
    client_secret: str
    auth0_subdomain: str


class PasswordAuthentication(Base):
    type: AuthenticationEnum = AuthenticationEnum.password


class Auth0Authentication(Base):
    type: AuthenticationEnum = AuthenticationEnum.auth0
    config: Auth0Config


class GitHubAuthentication(Base):
    type: AuthenticationEnum = AuthenticationEnum.github
    config: GitHubConfig


# =========== Users and Groups =============


class User(Base):
    password: typing.Optional[str]
    primary_group: typing.Optional[str]
    secondary_groups: typing.Optional[typing.List[str]]


class Group(Base):
    gid: typing.Optional[int]


# ================= Keycloak ==================


class Keycloak(Base):
    initial_root_password: typing.Optional[str]
    overrides: typing.Optional[typing.Dict]


# ============== Security ================


class Security(Base):
    authentication: typing.Union[
        PasswordAuthentication,
        Auth0Authentication,
        GitHubAuthentication,
    ]
    users: typing.Optional[typing.Dict[str, typing.Union[User, None]]]
    groups: typing.Optional[
        typing.Dict[str, typing.Union[Group, None]]
    ]  # If gid is omitted, no attributes in Group means it appears as None
    keycloak: typing.Optional[Keycloak]


# ================ Providers ===============


class KeyValueDict(Base):
    key: str
    value: str


class NodeSelector(Base):
    general: KeyValueDict
    user: KeyValueDict
    worker: KeyValueDict


class NodeGroup(Base):
    instance: str
    min_nodes: int
    max_nodes: int
    gpu: typing.Optional[bool] = False

    class Config:
        extra = "allow"


class DigitalOceanProvider(Base):
    region: str = "nyc3"
    kubernetes_version: str = "1.21.5-do.0"
    # Digital Ocean image slugs are listed here https://slugs.do-api.dev/
    node_groups: typing.Dict[str, NodeGroup] = {
        "general": NodeGroup(instance="g-4vcpu-16gb", min_nodes=1, max_nodes=1),
        "user": NodeGroup(instance="g-2vcpu-8gb", min_nodes=1, max_nodes=5),
        "worker": NodeGroup(instance="g-2vcpu-8gb", min_nodes=1, max_nodes=5),
    }


class GoogleCloudPlatformProvider(Base):
    region: str = "us-central1"
    availability_zones: typing.Optional[typing.List[str]] = [
        "us-central1-a",
    ]
    kubernetes_version: str = "1.18.16-gke.502"
    node_groups: typing.Dict[str, NodeGroup] = {
        "general": NodeGroup(instance="n1-standard-4", min_nodes=1, max_nodes=1),
        "user": NodeGroup(instance="n1-standard-2", min_nodes=0, max_nodes=5),
        "worker": NodeGroup(instance="n1-standard-2", min_nodes=0, max_nodes=5),
    }


class AzureProvider(Base):
    region: str = "Central US"
    kubernetes_version: str = "1.21"
    node_groups: typing.Dict[str, NodeGroup] = {
        "general": NodeGroup(instance="Standard_D4_v3", min_nodes=1, max_nodes=1),
        "user": NodeGroup(instance="Standard_D2_v2", min_nodes=0, max_nodes=5),
        "worker": NodeGroup(instance="Standard_D2_v2", min_nodes=0, max_nodes=5),
    }
    storage_account_postfix: str = "".join(
        random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8)
    )


class AmazonWebServicesProvider(Base):
    region: str = "us-west-2"
    availability_zones: typing.Optional[typing.List[str]] = [
        "us-west-2-den-1a",
        "us-west-2-las-1a"
    ]
    kubernetes_version: str = "1.18"
    node_groups: typing.Dict[str, NodeGroup] = {
        "general": NodeGroup(instance="m5.xlarge", min_nodes=1, max_nodes=1),
        "user": NodeGroup(instance="m5.large", min_nodes=1, max_nodes=5),
        "worker": NodeGroup(instance="m5.large", min_nodes=1, max_nodes=5),
    }


class LocalProvider(Base):
    kube_context: typing.Optional[str]
    node_selectors: typing.Dict[str, KeyValueDict] = {
        "general": {
            "key": "kubernetes.io/os",
            "value": "linux",
        },
        "user": {
            "key": "kubernetes.io/os",
            "value": "linux",
        },
        "worker": {
            "key": "kubernetes.io/os",
            "value": "linux",
        },
    }


# ================= Theme ==================


class Theme(Base):
    jupyterhub: typing.Dict[str, typing.Union[str, list]] = {
        "hub_title": None,
        "hub_subtitle": None,
        "welcome": None,
        "logo": "/hub/custom/images/jupyter_qhub_logo.svg",
        "primary_color": "#4f4173",
        "secondary_color": "#957da6",
        "accent_color": "#32C574",
        "text_color": "#111111",
        "h1_color": "#652e8e",
        "h2_color": "#652e8e",
    }


# ================== Profiles ==================


class KubeSpawner(Base):
    cpu_limit: int
    cpu_guarantee: int
    mem_limit: str
    mem_guarantee: str
    image: str

    class Config:
        extra = "allow"


class JupyterLabProfile(Base):
    display_name: str
    description: str
    default: typing.Optional[bool]
    users: typing.Optional[typing.List[str]]
    groups: typing.Optional[typing.List[str]]
    kubespawner_override: typing.Optional[KubeSpawner]


class DaskWorkerProfile(Base):
    worker_cores_limit: int
    worker_cores: int
    worker_memory_limit: str
    worker_memory: str
    image: str

    class Config:
        extra = "allow"


class Profiles(Base):
    jupyterlab: typing.List[JupyterLabProfile] = [
        JupyterLabProfile(
            display_name="Small Instance",
            description="Stable environment with 1 cpu / 4 GB ram",
            default=True,
            kubespawner_override={
                "cpu_limit": 1,
                "cpu_guarantee": 0.75,
                "mem_limit": "4G",
                "mem_guarantee": "2.5G",
                "image": f"quansight/qhub-jupyterlab:v{__version__}",
            },
        ),
        JupyterLabProfile(
            display_name="Medium Instance",
            description="Stable environment with 2 cpu / 8 GB ram",
            default=True,
            kubespawner_override={
                "cpu_limit": 2,
                "cpu_guarantee": 1.5,
                "mem_limit": "8G",
                "mem_guarantee": "5G",
                "image": f"quansight/qhub-jupyterlab:v{__version__}",
            },
        ),
    ]
    dask_worker: typing.Dict[str, DaskWorkerProfile] = {
        "Small Worker": DaskWorkerProfile(
            worker_cores_limit=1,
            worker_cores=0.75,
            worker_memory_limit="4G",
            worker_memory="2.5G",
            worker_threads=1,
            image=f"quansight/qhub-dask-worker:v{__version__}",
        ),
        "Medium Worker": DaskWorkerProfile(
            worker_cores_limit=2,
            worker_cores=1.5,
            worker_memory_limit="8G",
            worker_memory="5G",
            worker_threads=2,
            image=f"quansight/qhub-dask-worker:v{__version__}",
        )
    }

    @validator("jupyterlab", pre=True)
    def check_default(cls, v, values):
        """Check if only one default value is present"""
        default = [attrs["default"] for attrs in v if "default" in attrs]
        if default.count(True) > 1:
            raise TypeError(
                "Multiple default Jupyterlab profiles may cause unexpected problems."
            )
        return v


# ================ Environment ================


class CondaEnvironment(Base):
    name: str
    channels: typing.Optional[typing.List[str]]
    dependencies: typing.List[typing.Union[str, typing.Dict[str, typing.List[str]]]]


# =============== CDSDashboards ==============


class CDSDashboards(Base):
    enabled: bool = True
    cds_hide_user_named_servers: typing.Optional[bool] = True
    cds_hide_user_dashboard_servers: typing.Optional[bool] = True


# =============== Extensions = = ==============


class QHubExtensionEnv(Base):
    code: str


class QHubExtension(Base):
    name: str
    image: str
    urlslug: str
    private: bool = False
    oauth2client: bool = False
    envs: typing.Optional[typing.List[QHubExtensionEnv]]
    logout: typing.Optional[str]


# ======== External Container Registry ========

# This allows the user to set a private AWS ECR as a replacement for
# Docker Hub for some images - those where you provide the full path
# to the image on the ECR.
# extcr_account and extcr_region are the AWS account number and region
# of the ECR respectively. access_key_id and secret_access_key are
# AWS access keys that should have read access to the ECR.


class ExtContainerReg(Base):
    enabled: bool
    access_key_id: typing.Optional[str]
    secret_access_key: typing.Optional[str]
    extcr_account: typing.Optional[str]
    extcr_region: typing.Optional[str]

    @root_validator
    def enabled_must_have_fields(cls, values):
        if values["enabled"]:
            for fldname in (
                "access_key_id",
                "secret_access_key",
                "extcr_account",
                "extcr_region",
            ):
                if (
                    fldname not in values
                    or values[fldname] is None
                    or values[fldname].strip() == ""
                ):
                    raise ValueError(
                        f"external_container_reg must contain a non-blank {fldname} when enabled is true"
                    )
        return values


# ============ QHub Config ============
class QHubConfig(Base):
    project_name: str
    namespace: str = "dev"
    provider: ProviderEnum
    qhub_version: str = __version__
    ci_cd: typing.Optional[CICD]
    domain: str
    terraform_state: typing.Optional[TerraformState]
    certificate: Certificate
    helm_extensions: typing.Optional[typing.List[HelmExtension]] = []
    prefect: typing.Optional[Prefect]
    cdsdashboards: CDSDashboards
    security: Security
    external_container_reg: typing.Optional[ExtContainerReg]
    default_images: DefaultImages
    storage: typing.Dict[str, str] = {
        "conda_store": "60Gi",
        "shared_filesystem": "100Gi"
    }
    local: typing.Optional[LocalProvider]
    google_cloud_platform: typing.Optional[GoogleCloudPlatformProvider]
    amazon_web_services: typing.Optional[AmazonWebServicesProvider]
    azure: typing.Optional[AzureProvider]
    digital_ocean: typing.Optional[DigitalOceanProvider]
    theme: Theme
    profiles: Profiles
    environments: typing.Dict[str, CondaEnvironment] = {
        "environment-dask.yaml": CondaEnvironment(
            name="dask",
            channels=["conda-forge"],
            dependencies=[
                "python",
                "ipykernel",
                "ipywidgets",
                "qhub-dask ==0.3.13",
                "python-graphviz",
                "numpy",
                "numba",
                "pandas",
            ],
        ),
        "environment-dashboard.yaml": CondaEnvironment(
            name="dashboard",
            channels=["conda-forge"],
            dependencies=[
                "python==3.9.7",
                "ipykernel==6.4.1",
                "ipywidgets==7.6.5",
                "qhub-dask==0.3.13",
                "param==1.11.1",
                "python-graphviz==0.17",
                "matplotlib==3.4.3",
                "panel==0.12.4",
                "voila==0.2.16",
                "streamlit==1.0.0",
                "dash==2.0.0",
                "cdsdashboards-singleuser==0.6.0",
            ],
        )
    }
    monitoring: typing.Optional[Monitoring]
    clearml: typing.Optional[ClearML]
    extensions: typing.Optional[typing.List[QHubExtension]]

    @validator("qhub_version", pre=True, always=True)
    def check_default(cls, v):
        """
        Always called even if qhub_version is not supplied at all (so defaults to ''). That way we can give a more helpful error message.
        """
        if v != __version__:
            if v == "":
                v = "not supplied"
            raise ValueError(
                f"qhub_version in the config file must equal {__version__} to be processed by this version of qhub (your value is {v})."
                " Install a different version of qhub or run qhub upgrade to ensure your config file is compatible."
            )
        return v
