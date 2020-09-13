# Machine Learning Workflow

All providers have a bit of their own spin on the Machine Learning Workflow.

[Amazon Web Services](https://aws.amazon.com/) (AWS) → [Machine Learning Workflow](https://docs.aws.amazon.com/sagemaker/latest/dg/how-it-works-mlconcepts.html)
[Google Cloud Platform](https://cloud.google.com/) (GCP) → [Machine Learning Workflow](https://cloud.google.com/ml-engine/docs/tensorflow/ml-solutions-overview)
[Microsoft Azure](https://azure.microsoft.com/en-us/) (Azure) → [Machine Learning Workflow](https://docs.microsoft.com/en-us/azure/machine-learning/service/overview-what-is-azure-ml)

## ① Explore and Process Data

### Step 1: Retrieve the Data

Relatively easy when provided for us, but automation should be done here if we're obtaining information from a remote data source.

### Step 2: Clean & Explore the Data

Also includes getting rid of any outliers.

### Step 3: Prepare/Transform

Transform and normalize (if necessary) to prepare it for training.

Data should be split here into **training**, **validation**, and **test** datasets. 
	**Training** set is used to train our model. 
	**Validation** is used for model tuning and selection. 
	**Test** is used after training for evaluation of hte model.

## ② Modeling

Focuses on developing the model that's deployed to production.

### Step 1: Develop & Train the Model

Finally! Pretty self explanatory.

### Step 2: Validate & Evaluate the Model

Tune the model using **validation** set. Also, will select the model if we've compared it against multiple models in the training dataset, here.

## ③ Deployment

While less likely used for personal or academic use, this one is heavily used in the workplace. For usage in the workplace, currently existing infrastructure that supports part of the workflow may exist, or extremely sensitive data vulnerable to the security risks of cloud computing may not want to be migrated. Whether those concerns are security based, operationally based, or considered in terms of compliance or legal concerns.

### Step 1: Deploy to Production

As the name implies, we're going to need a model provided to those responsible for deployment. In our case, we're going to assume that the machine learning model we will be deploying was developed in Python.

#### Paths to Deployment

1. **Python model is recoded into the programming language of the production environment.**

   Least common. Normally involves recoding the model into Java or C++. Rarely used anymore because it simply doubles the time it takes to recode, test, and validate the model that provides the *same* prediction quality as the original. (Oof, imagine the double bugs.)

2. **Model is coded in Predictive Model Markup Language (PMML) or Portable Format Analytics (PFA), then ported.**

   Two complimentary standards that *simplify* moving predictive models to deployment in a production enviroment. That Data Mining Group developed both PMML and PFA to provide vendor-neutral executable model specifications for certain predictive models used by data mining and machine learning. Certain analytic software allows for the direct import of PMML including but *not limited to* IBM SPSS, R, Apache Spark, Teradata Warehouse Miner, etc.

3. **Python model is converted into a format that can be used in the production environment. (Most common.)**

   Use libraries and methods that convert the model into production-ready code. the *most* popular libraries include PyTorch, TensorFlow, and SciKit-Learn. Some even have methods that will convert Python into an intermediate format, such as [ONNX](https://onnx.ai/), or [Open Neural Network Exchange](https://onnx.ai/) format. These intermediate formats are then converted into software native to the production environment.

   * Probably the easiest and fastest way to move a Python model to deployment.
   * Typically how it's done in the workplace today.
   * Technologies like containers, endpoints, and APIs (Application Programming Interfaces) also help to ease the work required for deploying a model into the production environment.

### Step 2: Monitor and Update the Deployed Model

Model should be rebuilt and can be deployed as a new version of the application, which they can download the updated application. User data that's been captured by our application can also be cycled back into our new data and help improve our application!

Services include direct applications, databases, virtual machines, and other services, such as SageMaker, for Machine Learning!