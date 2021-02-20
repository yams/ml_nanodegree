# XGBoost as a model.

[Common Parameters](https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-algo-docker-registry-paths.html)

Early stopping rounds is used to determine if it should stop training the dataset early. For example, if the model starts to do worse on the validation set, then we're probably overfitting, and should stop.