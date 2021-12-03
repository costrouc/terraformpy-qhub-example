from qhub_tf.version import __version__
from qhub_tf import schema


def render_config(
    project_name: str,
    qhub_domain: str,
    cloud_provider: str,
    ci_provider: str,
    repository: str,
    auth_provider: str,
    namespace: str = "dev",
    terraform_state=None,
    kubernetes_version=None,
    ssl_cert_email=None,
):
    jupyterhub_theme_config = {
        "hub_title": f"QHub - { project_name }",
        "welcome": f"""Welcome to { qhub_domain }. It is maintained by <a href="http://quansight.com">Quansight staff</a>. The hub's configuration is stored in a github repository based on <a href="https://github.com/Quansight/qhub/">https://github.com/Quansight/qhub/</a>. To provide feedback and report any technical problems, please use the <a href="https://github.com/Quansight/qhub/issues">github issue tracker</a>."""
    }

    qhub_config_config = {
        "project_name": project_name,
        "namespace": namespace,
        "provider": cloud_provider,
        "qhub_version": __version__,
        "domain": qhub_domain,
    }

    if cloud_provider == "do":
        qhub_config_config['digital_ocean'] = schema.DigitalOceanProvider()
        jupyterhub_theme_config["hub_subtitle"] = "Autoscaling Compute Environment on DO"
    elif cloud_provider == "gcp":
        qhub_config_config['google_cloud_platform'] = schema.GoogleCloudPlatformProvider()
        jupyterhub_theme_config["hub_subtitle"] = "Autoscaling Compute Environment on GCP"
    elif cloud_provider == "azure":
        qhub_config_config['azure'] = schema.AzureProvider()
        jupyterhub_theme_config["hub_subtitle"] = "Autoscaling Compute Environment on Azure"
    elif cloud_provider == "aws":
        qhub_config_config['amazon_web_services'] = schema.AmazonWebServicesProvider()
        jupyterhub_theme_config["hub_subtitle"] = "Autoscaling Compute Environment on AWS"
    elif cloud_provider == "local":
        qhub_config_config["local"] = schema.LocalProvider()
        jupyterhub_theme_config["hub_subtitle"] = "Autoscaling Compute Environment"

    jupyterhub_theme = schema.Theme()
    jupyterhub_theme.jupyterhub.update(jupyterhub_theme_config)

    return schema.QHubConfig(
        **qhub_config_config,
        ci_cd=schema.CICD(),
        terraform_state=schema.TerraformState(),
        certificate=schema.Certificate(),
        cdsdashboards=schema.CDSDashboards(),
        security=schema.Security(
            authentication=schema.PasswordAuthentication()),
        default_images=schema.DefaultImages(),
        theme=jupyterhub_theme,
        profiles=schema.Profiles(),
        monitoring=schema.Monitoring(),
    )
