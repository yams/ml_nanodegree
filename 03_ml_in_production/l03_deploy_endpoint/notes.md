

# Deploying the Model using SageMaker

## Deploying the Model

Relatively straightforward. If we're utilizing the high level SageMaker algorithms, add a function call.

```python
xgb_predictor = xgb.deploy(initial_instance_count=1, instance_type='m1.m4.xlarge')
```

Under the hood, SageMaker has created a container with our virtual machine, running our model, that can be accessed at an endpoint URL.

**Deploying a Model** in SageMaker means <u>**creating an endpoint**.</u>

## Endpoint Adjustments + Considerations (Libraries)

Once the virtual machine has been created, we need to send it some additional information that we used to calculate in our local program.

- **Data Format**

```python
xgb_predictor.content_type = 'text/csv'
xgb_predictor.serializer = csv_serializer
```

- **Prediction**

```python
# This line slightly adjusted for text encoding, and CSV.
Y_pred = xgb_predictor.predict(X_test.values).decode('utf-8')
```

* **Convert back to numpy array**

```python
Y_pred = np.fromstring(Y_pred, sep=',')
```

* **Delete the endpoint**

```python
# We need to shut it down, else charges will rise.
xgb_predictor.delete_endpoint()
```

## Endpoint Adjustments + Considerations (Low Level)

In these ins
