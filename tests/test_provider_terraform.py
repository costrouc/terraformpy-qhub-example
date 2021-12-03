import tempfile
import os
import json

from qhub_tf.provider import terraform


def _write_terraform_test(directory):
    with open(os.path.join(directory, "example.tf"), "w") as f:
        f.write(
            """
resource "local_file" "main" {
    content     = "Hello, World!"
    filename    = "example.txt"
}

output "output_test" {
  description = "description of output"
  value = "test"
}
"""
        )


def test_terraform_version():
    assert terraform.version() == terraform.TERRAFORM_VERSION


def test_terraform_init_apply_output_destroy(tmpdir):
    """Difficult to split into separate unit tests"""
    _write_terraform_test(tmpdir)
    terraform.init(tmpdir)
    assert {".terraform.lock.hcl", ".terraform", "example.tf"} == set(
        os.listdir(tmpdir)
    )
    terraform.validate(tmpdir)
    terraform.apply(tmpdir)
    assert {
        "example.txt",
        "terraform.tfstate",
        ".terraform.lock.hcl",
        ".terraform",
        "example.tf",
    } == set(os.listdir(tmpdir))
    output = json.loads(terraform.output(tmpdir))
    assert output["output_test"]["value"] == "test"
    terraform.destroy(tmpdir)
    assert {
        "terraform.tfstate.backup",
        "terraform.tfstate",
        ".terraform.lock.hcl",
        ".terraform",
        "example.tf",
    } == set(os.listdir(tmpdir))
