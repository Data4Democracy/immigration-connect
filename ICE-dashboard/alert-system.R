.libPaths(c(.libPaths(), "r-packages"))
library(mailR)
 
 
#step 1, if there is an edit in the google spreadsheet in the last hour, we need to send out some texts
NILC <- read.csv('https://docs.google.com/spreadsheets/d/1Ho-Vhs8k3y5Dm8QvJHRlj8h8In9vcN0jeH5SgT-Y2Fw/pub?gid=0&single=true&output=csv')
#Let's figure out the dates first
Date <- Sys.Date()
NILC$DATE <- as.Date(NILC$DATE)
NewNILC <- NILC[NILC$DATE == Date,]
rm(NILC)
 
 
x <- Sys.time()
y <- substr(x, 12, 16)
y <- gsub(":", ".", y)
y <- as.numeric(y)
y = y -5
 
NewNILC$subtract <- y - NewNILC$TIMESTAMP 
NILCFINAL <- NewNILC[NewNILC$subtract < 1,]
NILCFINAL <- NILCFINAL[NILCFINAL$subtract >0,]
#NILCFINAL <- NILCFINAL[-1,]
 
if (nrow(NILCFINAL)>0){
  Db <- read.csv('https://docs.google.com/spreadsheets/d/1GE0XsKwf5UrSIvyQ6gQ6Z25HiO9XGMHplBABWwRC_AQ/pub?gid=0&single=true&output=csv')
 
  sender <- "tylerjrichards@gmail.com"
  for(i in 1:nrow(Db)) {
    
    
    
    
    if ( NILCFINAL$Zip.Code[1] == Db$Location[i]){
      
      print("hello")
      recipients <- paste(Db$Phone_Number[1], "@tmomail.net", sep = "")
      message <- paste("There was an ICE Raid in your area, the reported area is ", NILCFINAL$Zip.Code[1], ". And the Number of affected people is " , NILCFINAL$PERSONS[1], sep = "")
      send.mail(from = sender,
                to = recipients,
                subject = "ICE Raid",
                body = message,
                smtp = list(host.name = "smtp.gmail.com", port = 465, 
                            user.name = "RaidAlertFSU@gmail.com",            
                            passwd = "", ssl = TRUE),
                authenticate = TRUE,
                send = TRUE)
    }
    if ( as.character(NILCFINAL$STATE..Required.[1]) == as.character(Db$Location[i])){
      
      print("hello")
      recipients <- paste(Db$Phone_Number[1], "@tmomail.net", sep = "")
      message <- paste("There was an ICE Raid in your area, the reported area is ", NILCFINAL$Zip.Code[1], ". And the Number of affected people is " , NILCFINAL$PERSONS[1], sep = "")
      send.mail(from = sender,
                to = recipients,
                subject = "ICE Raid",
                body = message,
                smtp = list(host.name = "smtp.gmail.com", port = 465, 
                            user.name = "RaidAlertFSU@gmail.com",            
                            passwd = "", ssl = TRUE),
                authenticate = TRUE,
                send = TRUE)
    }
    
  }
}
