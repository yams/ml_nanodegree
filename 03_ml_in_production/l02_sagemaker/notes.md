

# Building a Model using SageMaker

## General Instances

SageMaker instances are a bit different than regular instances.

1. m1.t2.medium - really just for running notes and devving
2. m1.m4.xlarge - training and batching XGBOOST models, deploy all models to test
3. m1.p2.xlarge - train and batch transform, GPU accelerated Pytorch models, finals only

## SageMaker (Overwritten) Definitions

These terms are not SageMaker specific, but their meaning is slightly adjusted in the SageMaker context.

- **Session** - the SageMaker [session]((https://sagemaker.readthedocs.io/en/latest/session.html)) is a special *object* that pre-instantiates necessary things for our usage, such as S3 and some machine learning models. The `upload_data` , `train`, `tune`, and `create_model` functions are all integral to our usage of Sagemaker.
- **Role** - Sometimes called the *execution role*, this is the IAM role that you created when you created your notebook  instance. The role basically defines how data that your notebook uses/creates will be stored. You can even try printing out the role with `print(role)` to see the details of this creation.

## A Note on S3 Buckets

In these instances, we'll be using S3 buckets for data storage.

> S3, or Simple Storage Service, is a virtual storage solution that is mostly meant for data to be  written to few times and read from many times. This is, in some sense,  the main workhorse for data storage and transfer when using Amazon  services. These are similar to file folders that contain data *and* metadata about that data, such as the data size, date of upload, author, and so on.

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

# Prepare and Split the data (New!)
X_bos_pd = pd.DataFrame(boston.data, columns=boston.feature_names)
Y_bos_pd = pd.DataFrame(boston.target)

# We split the dataset into 2/3 training and 1/3 testing sets.
X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(X_bos_pd, Y_bos_pd, test_size=0.33)

# Then we split the training set further into 2/3 training and 1/3 validation sets.
X_train, X_val, Y_train, Y_val = sklearn.model_selection.train_test_split(X_train, Y_train, test_size=0.33)

# Save data locally, to prepare for S3 later (New!)
data_dir = '../data/boston'
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
    
# pandas saves our test, train and validation data to csv files. 
# No header information or index per built-in Amazon algorithm spec. Train and
# validation data assumes first entry in each row is the target variable.
X_test.to_csv(os.path.join(data_dir, 'test.csv'), header=False, index=False)

pd.concat([Y_val, X_val], axis=1).to_csv(os.path.join(data_dir, 'validation.csv'), header=False, index=False)
pd.concat([Y_train, X_train], axis=1).to_csv(os.path.join(data_dir, 'train.csv'), header=False, index=False)

# SageMaker Session Library contains S3 connections. Custom prefix is best practice (gets converted to an S3 folder), to avoid namespace collision.
prefix = 'boston-xgboost-HL'

test_location = session.upload_data(os.path.join(data_dir, 'test.csv'), key_prefix=prefix)
val_location = session.upload_data(os.path.join(data_dir, 'validation.csv'), key_prefix=prefix)
train_location = session.upload_data(os.path.join(data_dir, 'train.csv'), key_prefix=prefix)

```

### Train the XGBoost model

We'll use the SageMaker API for this as opposed to a python built-in API. Code is slightly easier to read, at the cost of some flexibility.

we need to provide the location of a container which contains the training code. Since we are using a built in algorithm this container is provided by Amazon. However, the full name of the container is a bit lengthy and depends on the region that we are operating in. Fortunately, SageMaker  provides a useful utility method called `get_image_uri` that constructs the image name for us.

To use the `get_image_uri` method we need to provide it  with our current region, which can be obtained from the session object,  and the name of the algorithm we wish to use. In this notebook we will  be using XGBoost however you could try another algorithm if you wish.  The list of built in algorithms can be found in the list of [Common Parameters](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-algo-docker-registry-paths.html). 

```python
# Construct the image name for the training container, which will contain the estimator
container = get_image_uri(session.boto_region_name, 'xgboost')

# Construct the estimator object, putting it into a container with IAM perms
xgb = sagemaker.estimator.Estimator(container,
                                    role,     
                                    train_instance_count=1, # number of instances to use for training (can be multiple)
                                    train_instance_type='ml.m4.xlarge',                                 															output_path='s3://{}/{}/output'.format(session.default_bucket(), prefix),                   
                                    sagemaker_session=session)

# Before asking SageMaker to train, set model specific hyperparameters. 
# Reference: https://docs.aws.amazon.com/sagemaker/latest/dg/xgboost_hyperparameters.html
xgb.set_hyperparameters(max_depth=5,
                        eta=0.2,
                        gamma=4,
                        min_child_weight=6,
                        subsample=0.8,
                        objective='reg:linear',
                        early_stopping_rounds=10,
                        num_round=200)

# Now, train and fit. content_type needs to match specific dataset.
s3_input_train = sagemaker.s3_input(s3_data=train_location, content_type='csv')
s3_input_validation = sagemaker.s3_input(s3_data=val_location, content_type='csv')

xgb.fit({'train': s3_input_train, 'validation': s3_input_validation})

# Test by initaiting a "transformer", which we will also use to confirm overfitting
xgb_transformer = xgb.transformer(instance_count = 1, instance_type = 'ml.m4.xlarge')

# Initiate the transform job.
xgb_transformer.transform(test_location, content_type='text/csv', split_type='Line')

# Since it's background initiatied, let's just pause while AWS finishes.
xgb_transformer.wait()

# Output is automatically stored in S3, so let's copy locally, and ingest the data.
!aws s3 cp --recursive $xgb_transformer.output_path $data_dir
Y_pred = pd.read_csv(os.path.join(data_dir, 'test.csv.out'), header=None)

# Graph the results.
plt.scatter(Y_test, Y_pred)
plt.xlabel("Median Price")
plt.ylabel("Predicted Price")
plt.title("Median Price vs Predicted Price")

# Cleanup, because our free instance is kinda size-limited.
!rm $data_dir/*
!rmdir $data_dir
```