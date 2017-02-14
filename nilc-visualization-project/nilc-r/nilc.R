.libPaths(c(.libPaths(), "r-packages"))

library(readr)
library(leaflet)
library(htmlwidgets)
library(dplyr)
library(geocode)

df <- read_csv('https://docs.google.com/spreadsheets/d/1Ho-Vhs8k3y5Dm8QvJHRlj8h8In9vcN0jeH5SgT-Y2Fw/pub?gid=0&single=true&output=csv', col_types=cols_only(col_character(), col_character(), col_character(), col_character(), col_character(), col_character(), col_integer(), col_integer()))
colnames(df) <- c('ID', 'DateStr', 'LocalTime', 'Description', 'Address', 'Location', 'MinPersons', 'MaxPersons')


geocodeables <- df %>%
  select(ID, Address) %>%
  filter(!is.na(Address))

coords <- cbind(geocode(geocodeables$Address), geocodeables) %>%
  mutate(addr1=paste0(Number, ' ', Street), addr2=paste0(City, ', ', State)) %>%
  select(ID, Latitude, Longitude, addr1, addr2)

df <- left_join(df, coords, by="ID") %>%
  filter(!is.na(Latitude)) %>% filter(!is.na(Longitude)) %>%
  mutate(size=ifelse(is.na(MinPersons) & is.na(MaxPersons), 1,
                     ifelse(is.na(MaxPersons), MinPersons,
                            ifelse(is.na(MinPersons), MaxPersons, (MinPersons+MaxPersons)/2)))) %>%
  mutate(SizeLabel=ifelse(is.na(MinPersons) & is.na(MaxPersons), 'Unknown',
                          ifelse(is.na(MaxPersons), as.character(MinPersons),
                                 ifelse(is.na(MinPersons), as.character(MaxPersons), paste0(MinPersons, '-', MaxPersons))))) %>%
  mutate(size=size*10000)

m <- leaflet(df) %>%
  addTiles() %>%
  addCircles(lng=~Longitude, lat=~Latitude, popup=~paste0(Description, '<br>', DateStr, '<br>', addr1, '<br>', addr2, '<br># of people: ', SizeLabel), radius=~size) #%>%

saveWidget(m, "test.html", FALSE)
