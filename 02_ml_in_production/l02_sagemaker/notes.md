# Building a Model using SageMaker

## General Instances

SageMaker instances are a bit different than regular instances.

1. m1.t2.medium - really just for running notes and devving
2. m1.m4.xlarge - training and batching XGBOOST models, deploy all models to test
3. m1.p2.xlarge - train and batch transform, GPU accelerated Pytorch models, finals only

## AWS Service Utilization Quotas

Each quota is region-specific.

There are three ways to view quotes:

* Service Endpoints and Quotas
* Services Quotas console
* AWS CLI commands
  * list-service-quotas
  * list-aws-default-service-quotas

And three ways to increase quotas

* Amazon Service Quotas service, log directly into the Service Quotas console
* Using AWS Support Center - creating a manual support case
  * https://aws.amazon.com/console
  * AWS Support Center → Create case
  * Service limit increase
  * Case details → Sagemaker
  * Request 1 → Appropriate region, Resource Type → SageMaker training, Limit → ml.m4.xlarge instances, New limit value → 1
* AWS CLI commands
  * request-service-quota-increase

**Of Note: Currently, Amazon Service Quotas does not support SageMaker service.**

### Recommendations for SageMaker services

1. For `ml.m4.xlarge`- The default quota would be any number in the range [0 - 20]. Students can expect an error - *'ResourceLimitExceeded'*, when executing the notebook in the concept ***Boston Housing Problem - Training The Model\***, later in this lesson. In such a case only, the student must request a limit increase for `ml.m4.xlarge`. 
2. For `ml.p2.xlarge` - The default quota would be either 0 or 1, therefore it is alright to go ahead and request an increase anytime.

## Setting Up a Notebook Instance

This will be the primary way that we're going to interact with a notebook.

It's also important to realize that these notebooks need to be into the **Stop** state when not in use, or you will be charged. Data will stay as long as the instance is not **Deleted**.

```bash
https://console.aws.amazon.com
```

SageMaker dashboard → Notebook Instances → Create notebook instance

Start with `ml.t2.medium`

### Create an IAM role

Defaults permissions are fine, to save on cost make sure **S3 buckets** are set to **None**. A name will be automatically provisioned, if none is provided.

### Maneuvering the Instance

Once the Notebook instance has been created, go to `Open Jupyter` under `Actions` will open a new tab, that lets you experiment with the code.

### Importing Git Code

On the right side under `Files` go to `New`, and choose `Terminal` on the drop-down menu.

```bash
cd SageMaker
git clone https://github.com/udacity/sagemaker-deployment.git
exit
```

Once the directory has been copied, it should show up automatically in the main Jupyter instance.