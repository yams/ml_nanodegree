# Modeling

## ① Characteristics of Modeling

In machine learning, a **hyperparameter** is a parameter whose value cannot be estimated from the data.

* Specifically, a **hyperparameter** is *not directly* learned through the estimators. Therefore, the value must be **set** by the model developer.
* Thus, hyperparameter tuning for optimization is an important part of model training.
* Often, cloud platform machine learning services provide methods that allow for **automatic hyperparameter** tuning, for use with model training.

If the machine learning platform fails to offer an *automatic* **hyperparameter** option, one option is to use methods from scikit-learn in Python to help, and set those in the application.

## ② Characteristics of Deployment, in regards to the Model

* Model Versioning
  * Besides saving the **model version** as a part of a model's metadata in a database, the *deployment platform* should allow one to indicate a deployed **model's version**.
  * This makes it easier to maintain, monitor, and update the *deployed model*.
* Model Monitoring
  * Once a model is deployed, you will want to make certain it continues to meet it's performance metrics; otherwise, the application may need to be updated with a *better* performing model.
  * Deployment needs to ensure that we can easily **monitor** our deployed models.
* Model Updating (Simple)
  * If a deployed model is *failing* to meet it's performance metrics, it's likely we will need to **update** the model.
  * Deployment needs to allow us to easily **update** our models.
* Model Routing (Complicated)
  * If there's been a fundamental change in the data that's being input into the model for predictions, we'll want to collect this input data  to be used to **update** the model.
  * The deployment platform should support **routing** differing proportions of user requests to the deployed models; to allow *comparison* of performance between the deployed model variants.
  * This enables us to **compare model performance** between different versions **and** variants.
* Predictions (On-Demand)
  * May also be called online, real-time, or synchronous predictions.
  * **Expectations**: a *low latency* of response to each prediction request, but allows for possibility *high variability* in request volume.
  * Predictions are returned in the response from the request. Often these requests and responses are done through an API using JSON or XML formatted strings.
  * Each prediction request from the user can contain *one* **or** *many* requests for predictions. Noting that *many* is limited based upon the *size* of the data sent as the request. **Common cloud platforms on-demand prediction limits range from 1.5 to 5 Megabytes**.
  * **On-demand predictions are commonly used to provide customers, users, or employees with real-time, online responses based upon a deployed model.** Think: immediate response that a user wants to see.
* Predictions (Batch)
  * May also be called asynchronous, or batch-based predictions.
  * **Expectations**: *high volume* of requests, with more periodic submission, indicating *latency* is not an issue
  * Each batch request will point to specifically formatted data file of requests and will return the predictions to a file. Cloud services **require** these files to be *stored* in the cloud provider's cloud.
  * Cloud services typically have *limits* on how much data they can process with each batch request, based upon limits they impose on the *size of file* you can store in their cloud storage service. For example, *Amazon's SageMaker* limits batch predictions requests to the size limit they enforce on an object in their S3 storage service.
  * **Batch predictions are commonly used to help make business decisions.** Think: A business has a complex model to predict customer satisfaction across a number of products, and they need those estimates weekly.