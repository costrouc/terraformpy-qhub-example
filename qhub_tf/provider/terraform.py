import io
import logging
import os
import platform
import re
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from typing import List


TERRAFORM_VERSION = "1.0.5"


class TerraformException(Exception):
    pass


def run_subprocess(args: List[str], prefix: str = None, streaming: bool=False, **kwargs):
    if prefix:
        line_prefix = f"[{prefix}]: "
    else:
        line_prefix

    print(line_prefix + "$ " + " ".join(args))

    if "shell" in kwargs:
        args = " ".join(args)

    process = subprocess.Popen(
        args,
        **kwargs,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
    )
    if streaming:
        for line in process.stdout.readlines():
            print(line_prefix + line, end="")
    return process.wait()


def run_terraform_subprocess(args: List[str], streaming: bool = True, **kwargs):
    terraform_path = download_terraform_binary()
    if run_subprocess([terraform_path] + args, streaming=streaming, prefix="terraform", **kwargs):
        raise TerraformException("Terraform returned an error")


def download_terraform_binary(version=TERRAFORM_VERSION):
    os_mapping = {
        "linux": "linux",
        "win32": "windows",
        "darwin": "darwin",
        "freebsd": "freebsd",
        "openbsd": "openbsd",
        "solaris": "solaris",
    }

    architecture_mapping = {
        "x86_64": "amd64",
        "i386": "386",
        "armv7l": "arm",
        "aarch64": "arm64",
    }

    download_url = f"https://releases.hashicorp.com/terraform/{version}/terraform_{version}_{os_mapping[sys.platform]}_{architecture_mapping[platform.machine()]}.zip"
    filename_directory = os.path.join(tempfile.gettempdir(), "terraform", version)
    filename_path = os.path.join(filename_directory, "terraform")

    if not os.path.isfile(filename_path):
        with urllib.request.urlopen(download_url) as f:
            bytes_io = io.BytesIO(f.read())
        download_file = zipfile.ZipFile(bytes_io)
        download_file.extract("terraform", filename_directory)

    os.chmod(filename_path, 0o555)
    return filename_path


def version():
    terraform_path = download_terraform_binary()
    command = [terraform_path, "--version"]
    version_output = subprocess.check_output(command, encoding='utf-8')
    return re.search(r"(\d+)\.(\d+).(\d+)", version_output).group(0)


def init(directory=None):
    run_terraform_subprocess(["init", "-no-color"], cwd=directory)


def validate(directory=None):
    run_terraform_subprocess(["validate", "-no-color"], cwd=directory)


def plan(directory=None):
    command = ["plan", "-no-color"]
    run_terraform_subprocess(command, cwd=directory)


def apply(directory=None, targets=None):
    targets = targets or []
    command = ["apply", "-auto-approve", "-no-color"] + ["-target=" + _ for _ in targets]
    run_terraform_subprocess(command, cwd=directory)


def output(directory=None):
    terraform_path = download_terraform_binary()
    return subprocess.check_output(
        [terraform_path, "output", "-json"], cwd=directory
    ).decode("utf8")[:-1]


def destroy(directory=None):
    command = ["destroy", "-auto-approve", "-no-color"]
    run_terraform_subprocess(command, cwd=directory)
