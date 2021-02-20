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

# General Notebook Outline with Boston Housing Example

Typically, when using a notebook instance with SageMaker, we will proceed through the following steps.

1. Download or otherwise retrieve the data.
2. Process / Prepare the data.
3. Upload the processed data to S3.
4. Train a chosen model.
5. Test the trained model (typically using a batch transform job).
6. Deploy the trained model.
7. Use the deployed model.

### Setup, Download Data

The initial dataset we're going to look at is `Housing Data for Boston, MA`, and we're going to try to predict a house value using a variety of datasets.

```bash
https://www.cs.toronto.edu/~delve/data/boston/bostonDetail.html
```

This has been preloaded onto the Jupyter notebook, from the `github.com/udacity/sagemaker-deployment.git` repository.

```python
# Make sure we use SageMaker 1.x for the lesson
!pip install sagemaker==1.72.0

# Normal Python Imports

%matplotlib inline

import os

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from sklearn.datasets import load_boston
import sklearn.model_selection

# SageMaker Imports (New!)

import sagemaker
from sagemaker import get_execution_role
from sagemaker.amazon.amazon_estimator import get_image_uri
from sagemaker.predictor import csv_serializer

# Initialize a session for us to interact with (New!)
session = sagemaker.Session()

# Obtain IAM role from AWS Console (New!)
role = get_execution_role()

# Download the data (New!)
boston = load_boston
```