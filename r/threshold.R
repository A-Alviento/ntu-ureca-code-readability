library(glmnet)
library(caret)
library(pROC)
library(ROCR)
library("MLmetrics")

f1 <- function(x) {
  set.seed(x)
  training.idx = sample(1: nrow(ownFeaturesDF_isReadable), nrow(ownFeaturesDF_isReadable)*0.8)
  train.data = ownFeaturesDF_isReadable[training.idx, ]
  test.data = ownFeaturesDF_isReadable[-training.idx, ]
  
  # Training final model with selected features
  final_model <- train(Readable~numLines + avgCharsLine + ratioComment + ratioBlank + 
                         avgNewId + avgIdLen + ratioIndentNumLines + commentReadabilityFK,
                       data = train.data, trControl = trainControl(method = "cv", number = 10), 
                       method = "glm", family = binomial())
  # Compute the prediction object
  test_probs <- predict(final_model, newdata = test.data, type = "prob")
  # Change the threshold
  threshold <- 0.35767
  pred_class <- ifelse(test_probs[2] > threshold, 1, 0)
  # Compute the confusion matrix for the new threshold
  conf_mat <- confusionMatrix(as.factor(pred_class), test.data$Readable, mode = "everything", positive="1")
  return(c(conf_mat$overall['Accuracy'], conf_mat$byClass['F1']))
}

y = c(0,0)

for(k in 1:1000){
  y = y + f1(k)
}
y/1000
  