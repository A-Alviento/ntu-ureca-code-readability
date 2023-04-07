library(glmnet)
library(caret)
library(pROC)
library(ROCR)
library("MLmetrics")

# function to train a model on a specific seed
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
  
  # Function to calculate F1 score
  F1_Score <- function(true_labels, predicted_labels) {
    tp <- sum(true_labels == 1 & predicted_labels == 1)
    fp <- sum(true_labels == 0 & predicted_labels == 1)
    fn <- sum(true_labels == 1 & predicted_labels == 0)
    precision <- tp / (tp + fp)
    recall <- tp / (tp + fn)
    f1_score <- 2 * precision * recall / (precision + recall)
    return(f1_score)
  }
  calc_f1 <- function(threshold) {
    predicted <- as.numeric(f1_data$prob >= threshold)
    f1 <- F1_Score(f1_data$true, predicted)
    return(f1)
  }
  
  # Obtain predicted probabilities of test data
  test_probs <- predict(final_model, newdata = test.data, type = "prob")
  # Create dataframe with predicted probabilities and true labels
  f1_data <- data.frame(prob = test_probs[,2], true = test.data$Readable)
  thresholds <- seq(0, 1, by = 0.01)
  f1_scores <- sapply(thresholds, calc_f1)
  best_threshold_index <- which.max(f1_scores)
  return(thresholds[best_threshold_index])
}

y = 0

for(k in 1:1000){
  y = y + f1(k)
}
y/1000
