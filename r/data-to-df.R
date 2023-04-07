library(foreign)
library(dplyr)

# read in dataset from Scalabrino
featuresDF = read.arff("features.arff.txt")
colnames(featuresDF)

# read in scores of the 200 snippets
scoresDF = read.csv("scores.csv")
scoresDF
colnames(scoresDF)
# transpose the dataframe so the columns are the evaluator scores
# and the rows are the snippets
scoresDF = t(scoresDF)
# make the first row the column heading
colnames(scoresDF) = scoresDF[1, ]
colnames(scoresDF)
# remove first row since it's just the colnames
scoresDF = scoresDF[-1, ]
# convert entries from chr to numeric
scoresDF = apply(scoresDF, 2, as.numeric)
# turn matrix into df
scoresDF = as.data.frame(scoresDF)
# add mean score column
scoresDF = scoresDF %>% mutate(meanScore = (Evaluator1 + Evaluator2 + Evaluator3 +
                                                Evaluator4 + Evaluator5 + Evaluator6 +
                                                Evaluator7 + Evaluator8 + Evaluator9)/9 )
head(scoresDF)

# Plot density and add mean line
meanTotalScore <- mean(scoresDF$meanScore)
plot(density(scoresDF$meanScore), col = "black", lwd = 2, main = "Density Plot of Last Column")
abline(v = meanTotalScore, col = "red", lty = 2)
text(meanTotalScore, max(density(scoresDF$meanScore)$y), paste0("Mean = ", round(meanTotalScore, 2)), pos = 2)
legend("topright", legend = c("Density", "Mean"), col = c("black", "red"), lty = c(1, 2), cex = 0.8)


# read in own features implementation
ownFeaturesDF = read.csv("feature_matrix_5.csv", header = FALSE)
head(ownFeaturesDF)
# name column header
colnames(ownFeaturesDF) = c("numLines", "numBlankLines", "numChars", "ratioBlank", "avgCharsLine", 
                            "halsteadVol", "numComment", "ratioComment", "commentReadabilityGF", 
                            "commentReadabilityFK", "numIdentifier", "numEngIdentifier", "numNewIdentifier", 
                            "numNewEngIdentifier", "avgNumId", "ratioEngIdOverId", "avgNewId",  
                            "ratioNewEngIdOverNewId", "numMeaningfulId", "ratioMeaningufulId", 
                            "avgIdLen", "numIndentBlocks", "ratioIndentNumLines", "maxIndent",  
                            "numCommentBlk", "ratioCommentBlock")


# extract the readable column into another dataframe
isReadable = featuresDF["Readable"]
# add both isReadable into ownFeaturesDF
ownFeaturesDF_isReadable = cbind(ownFeaturesDF, isReadable)
# copy dataset to ds, the dataset to test the subsets
ds = ownFeaturesDF_isReadable


# generate a heatmap of the correlation coefficient of each feature variables
library(corrplot)
matrix_plot = apply(ownFeaturesDF_isReadable, 2, as.numeric)
matrix_plot
str(matrix_plot)
corrplot(cor(matrix_plot),type="upper",method="color",addCoef.col = "black",number.cex = 0.6)
head(ds, 27)

# generate list of pairs of feature variables that are highly correlated
# turn the matrix of features into a dataframe
matrix_plot = as.data.frame(matrix_plot)
colnames(matrix_plot) = c("numLines", "numBlankLines", "numChars", "ratioBlank", "avgCharsLine", 
                          "halsteadVol", "numComment", "ratioComment", "commentReadabilityGF", 
                          "commentReadabilityFK", "numIdentifier", "numEngIdentifier", "numNewIdentifier", 
                          "numNewEngIdentifier", "avgNumId", "ratioEngIdOverId", "avgNewId",  
                          "ratioNewEngIdOverNewId", "numMeaningfulId", "ratioMeaningufulId", 
                          "avgIdLen", "numIndentBlocks", "ratioIndentNumLines", "maxIndent",  
                          "numCommentBlk", "ratioCommentBlock", "Readable")
# Create a list of all pairs of variables
var_pairs <- combn(names(matrix_plot), 2, simplify = FALSE)
# Calculate the correlation coefficient for each pair of variables
cor_vals <- sapply(var_pairs, function(x) cor(matrix_plot[[x[1]]], matrix_plot[[x[2]]]))
# Create a data frame with the variable pairs and their correlation coefficients
cor_df <- data.frame(Var1 = sapply(var_pairs, "[[", 1), Var2 = sapply(var_pairs, "[[", 2), Corr = cor_vals)
# Filter the data frame to show only highly correlated pairs (absolute correlation coefficient > 0.7)
high_corr_pairs <- subset(cor_df, abs(Corr) > 0.7)
# Print the highly correlated pairs
print(high_corr_pairs)





















predic_Model = c(1,
                      0,
                      1,
                      1,
                      0,
                      0,
                      1,
                      0,
                      1,
                      0,
                      1,
                      0,
                      0,
                      1,
                      1,
                      1,
                      1,
                      1,
                      0,
                      1,
                      0,
                      1,
                      0,
                      1,
                      0,
                      0,
                      0,
                      0,
                      0,
                      1,
                      0,
                      1,
                      1,
                      0,
                      0,
                      1,
                      0,
                      1,
                      0,
                      0,
                      0,
                      1,
                      1,
                      1,
                      1,
                      1,
                      0,
                      1,
                      0,
                      1,
                      1,
                      0,
                      1,
                      0,
                      1,
                      1,
                      1,
                      0,
                      1,
                      0,
                      1,
                      1,
                      0,
                      1,
                      1,
                      0,
                      1,
                      0,
                      0,
                      0,
                      0,
                      0,
                      1,
                      1,
                      1,
                      0,
                      1,
                      1,
                      1,
                      1,
                      0,
                      1,
                      1,
                      0,
                      0,
                      1,
                      0,
                      1,
                      0,
                      0,
                      1,
                      1,
                      0,
                      0,
                      1,
                      0,
                      0,
                      0,
                      0,
                      0,
                      1,
                      0,
                      1,
                      1,
                      1,
                      1,
                      0,
                      1,
                      0,
                      1,
                      0,
                      0,
                      0,
                      0,
                      0,
                      1,
                      1,
                      1,
                      1,
                      1,
                      0,
                      1,
                      1,
                      1,
                      0,
                      1,
                      0,
                      1,
                      0,
                      0,
                      0,
                      0,
                      1,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      0,
                      1,
                      1,
                      1,
                      0,
                      0,
                      0,
                      0,
                      0,
                      1,
                      0,
                      0,
                      0,
                      0,
                      0,
                      1,
                      0,
                      0,
                      0,
                      0,
                      0,
                      1,
                      0,
                      0,
                      1,
                      1,
                      1,
                      0,
                      0,
                      0,
                      0,
                      1,
                      1,
                      1,
                      0,
                      1,
                      0,
                      1,
                      0,
                      0,
                      1,
                      1,
                      1,
                      1,
                      1,
                      1,
                      0,
                      0,
                      1,
                      0,
                      1,
                      1,
                      0,
                      1,
                      0,
                      1,
                      1,
                      0,
                      0)
predic_Model
# create two sample data frames
actual <- data.frame(a = c(1,0,1,1,0), b = c(0,1,0,1,0))
predicted <- data.frame(a = c(1,0,0,1,0), b = c(0,1,1,1,0))

isReadable = as.factor(isReadable)
predic_Model = as.factor(predic_Model)

confusion_mat <- confusionMatrix(predic_Model, isReadable, mode = "everything", positive="1")
confusion_mat$overall['Accuracy']

