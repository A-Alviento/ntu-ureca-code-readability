library(glmnet)
library(caret)
library(pROC)
library(ROCR)
library("MLmetrics")
library(car)
library(FSelector)

# List of features:
# "numLines", "numBlankLines", "numChars", "ratioBlank", "avgCharsLine", 
# "halsteadVol", "numComment", "ratioComment", "commentReadabilityGF", 
# "commentReadabilityFK", "numIdentifier", "numEngIdentifier", "numNewIdentifier", 
# "numNewEngIdentifier", "avgNumId", "ratioEngIdOverId", "avgNewId",  
# "ratioNewEngIdOverNewId", "numMeaningfulId", "ratioMeaningufulId", 
# "avgIdLen", "numIndentBlocks", "ratioIndentNumLines", "maxIndent",  
# "numCommentBlk", "ratioCommentBlock"

# renew values for the dataset
ownFeaturesDF_isReadable = ds
ds
# Loop through identified columns and remove outliers from active features being used
for (col in colnames(ownFeaturesDF_isReadable[,c("numLines", "avgCharsLine","ratioComment", "ratioBlank", 
                                                 "avgNewId", "avgIdLen", "ratioIndentNumLines", "commentReadabilityFK")])) {
  q <- quantile(ownFeaturesDF_isReadable[[col]], c(0.25, 0.75), na.rm=TRUE)
  iqr <- q[2] - q[1]
  lower_bound <- q[1] - 1.5 * iqr
  upper_bound <- q[2] + 1.5 * iqr
  ownFeaturesDF_isReadable[[col]][ownFeaturesDF_isReadable[[col]] < lower_bound | ownFeaturesDF_isReadable[[col]] > upper_bound] <- NA
}
ownFeaturesDF_isReadable = na.omit(ownFeaturesDF_isReadable)


# function to train a model on a specific seed
f2 <- function(x, z) {
  set.seed(101)
  
  # split dataset into training and testing sets
  training.idx = sample(1: nrow(ownFeaturesDF_isReadable), nrow(ownFeaturesDF_isReadable)*0.8)
  train.data = ownFeaturesDF_isReadable[training.idx, ]
  test.data = ownFeaturesDF_isReadable[-training.idx, ]
  
  # Training final model with selected features
  final_model <- train(Readable~numLines + avgCharsLine + ratioComment + ratioBlank + 
                         avgNewId + avgIdLen + ratioIndentNumLines + commentReadabilityFK,
                       data = train.data, trControl = trainControl(method = "cv", number = 10), 
                       method = "glm", family = binomial())
  final_model
  summary(final_model)
  
  # relief_scores = relief(final_model, data = train.data)
  # relief_scores
  
  # Make predictions on test set
  predictions <- predict(final_model, newdata = test.data, type = "raw")
  # Calculate performance metrics
  confusion_mat <- confusionMatrix(predictions, test.data$Readable, mode = "everything", positive="1")
  roc_obj <- roc(as.numeric(test.data$Readable)-1, as.numeric(predictions), levels = c("0", "1"))
  auc <- auc(roc_obj)
  
  
  confusion_mat$overall['Accuracy']
  confusion_mat$byClass['F1']
  
  #return (as.data.frame(final_model$finalModel["coefficients"]))
  return (c(confusion_mat$overall['Accuracy'], confusion_mat$byClass['F1'], as.numeric(auc)))
}

# variable to hold accuracy, F1 value and AUC
y = c(0, 0, 0)
y = as.data.frame(y)
# dataframe to hold all accuracy, F1 and AUC of each seed
z <- data.frame(Accuracy = numeric(), F1 = numeric(), AUC = numeric())
# multiple seeded runs
for(k in 1:1000){
  y = y + f2(k, z)
  new_row <- f2(k,z)
  z <- rbind(z, new_row)
}
# output average accuracy, F1 value and AUC
y/1000

colnames(z) = c("Accuracy", "F1", "AUC")
z

ggplot(z, aes(x = "Accuracy", y = Accuracy)) + 
  geom_boxplot() + labs(x = "Seeded Runs")
