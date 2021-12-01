# Usage

Dependencies are:
 - terraformpy
 - pydantic

Do a "mock" render of the terraform files

```python
from qhub_tf.deploy import deploy
deploy()
```

Then do the actual deployment

```shell
cd /tmp/infrastructure/
terraform init
terraform plan
```
