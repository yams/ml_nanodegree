# Section 2: Deployment

We'll be deploying our model using [Amazon's SageMaker](https://aws.amazon.com/sagemaker/).

## Problem Introduction: 

We'll be predicting the median value of home in Boston Masachusetts, using a provided dataset. Features:We're using Avg. number of rooms, and medium value (in USD). Ultimate goal is to also deploy this out to a smartphone application that we've developed.

## 1. What's the *machine learning workflow*?

## 2. How does ***deployment\*** fit into the *machine learning workflow*?

## 3. What is *cloud computing*?

## 4. Why would we use *cloud computing* for ***deploying\*** machine learning models?

## 5. Why isn't deployment a part of many machine learning curriculums?

## 6. What does it mean for a model to be ***deployed\***?

## 7. What are the *essential* characteristics associated with the code of *deployed models*?

## 8. What are *different* cloud computing platforms we might use to ***deploy\*** our machine learning models?

At the end of this lesson, you'll understand the broader idea of ***machine learning deployment\***. Then Sean will be guiding you through using [SageMaker](https://aws.amazon.com/sagemaker/) to *deploy* your own machine learning models. This is a lot to cover, but by the end you will have a general idea of *all* the concepts related to *deploying machine learning models* into real world *production systems*.

## 9. Production Environments

The Application takes data input from users. Then, submits that data to our model. Afterwards, it's our model that uses the data, and outputs **predictions**.

The environment itself is the computation system that hosts the application. Software engineers traditionally have hold over the production environment.

The interface through which the model receives data, and sends out predictions, is called the **endpoint**.

### Endpoint

1. Allows the application to send **user data** to the model.
2. Receives **predictions** back from the model based upon that **user data**.
3. If it helps, in programming terms, the endpoing can be a function that takes a parameter of the user data, and returns a value of for the prediction.

 Endpoints facilitate communication between the application and the model, through an interface, known as the **Application Programming Interface**, or **API**.

1. Think of the API as "a set of rules that enable programs to communicate with each other"
2. Most API's use **RE**presentational **S**tate **T**ransfer, or **REST*, architecture, which provides a defined framework for the set of rules and constrants that must be adhered to for communication between programs.
3. This **REST API** uses HTTP requests and responses to enable communication between the **application** and **model**. (The application sends HTTP requests, the model sends HTTP responses.)

### HTTP Requests

Composed of *four* parts.

1. Endpoint - in the form of a URL or **Uniform Resource Locator**, which is commonly known as a web address.
2. HTTP Method - one of four **HTTP Methods** - **GET, POST, PUT, or DELETE**.
3. HTTP Headers - The headers will contain additional information, like the format of the data within the message, that's passed to the *receiving* program.
4. Message (sometimes *body* or *data*) - The final part - contains the input for the specific method.

### HTTP Responses

Three parts.

1. HTTP Status Code - If the model successfully received and processed the user's data that was sent in the **message**, the status code should start with a **2**, like *200*.
2. HTTP Headers - the **headers** contain additional information, like the format of the data within the **message**, that's passed to the receiving program.
3. Message (Data or Body) - What's returned as the *data* within the **message** is the *prediction* that's provided by the **model**.

This prediction is then presented to the *application user* through the **application**.

### Applications Responsibilities

1. To format the *user's data* in a way that can be easily put into the **HTTP Request** message, and be used by the model.
2. To translate the *predictions* of the from the **HTTP Response** message in a way that's easy for the *application user* to understand.

### **Common Standards**

* Often, the *user's data* will need to be in a CSV or JSON format with a specific *ordering* of the data that's dependent upon the **model** used.
* Often *predictions* will be returned in CSV or JSON format with a specific *ordering* of the returned *predictions* dependent upon the **model** used.

## Containers

Both the **model** and the **application** require a computing environment so that they can be run and available for use. One way to *create* and *maintain* these computing environments is through the use of **containers**.

* Specifically, the **model** and the **application** can each be run in a **container** computing environment. The **containers** are created using a **script** that contains instructions on which software packages, librareis, and other computing attributes are needed in order to run a *software application*, in our case either the **model**, or the **application**.

### Definition

A **container** can be thought of as a standardized collection/bundle of software that is to be used for the specific purpose of running an application.

A very common container software is *Docker*. Do it's popularity, sometimes *Docker* is synonymously used with **containers**.

### Containers Overview

Due to their generic structure, Docker containers can contain all types of software.

* The structure of a container enables the container to be created, saved, used, and deleted through a set of common tools.
* This common tool set works with any container, regardless of the software the container contains

### Container Structure

* The underlying *computational infrastructure* can be a cloud provider's data center, an on-premise data center, or even someone's local computer.
* Second, an *operating system* running on top of this *computation infrastructure*, in either the data center, or locally.
* Third, the *container engine*, this could be *Docker* software.
  * The container engine software enables one to create, save, use, and delete containers.
* Fourth, there is the *container* itself, which has two core components.
  * The *libraries and binaries* required to launch, run, and maintain the application layer.
  * Lastly, the *application* layer itself.

### Architecture Benefits

1. Isolates the application, which increases security.
2. Requires *only* the software needed to run the application, which uses computational resources *more efficiently* and allows for faster application deployment.
3. Makes application creation, replication, deletion, and maintenance easier, and the same across all applications that are deployed.
4. Provides a more simple and secure way to replicate, save, and share containers.

### Container Construction

1. Done via a **container script file**, which can easily be shared with others and provides a simple method to *replicate* a **particular container**. In docker, these scripts are referred to as *dockerfiles*.
2. The **container engine** then calls this script, generating a container. These scripts are stored in repositories, which provide a simple means to share and replicate themselves. For Docker, the Docker Hub is the official repository for storing and sharing *dockerfiles*.