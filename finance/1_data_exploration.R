germanCredit = read.table('https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data', header = TRUE,  sep = '	',  stringsAsFactors = FALSE)

dim(germanCredit)

# germanCredit<-germanCredit[,c(1:5,21)]

str(germanCredit)

colnames(germanCredit)<-c("chkAcctStart","duration","credHist","purpose","amount","rating")

library(tibble)
germanCredit<-as_tibble(germanCredit)

summary(germanCredit)