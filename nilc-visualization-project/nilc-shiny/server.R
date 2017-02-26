library(shiny)
library(leaflet)
library(dplyr)
library(readr)
library(geocode)

function(input, output, session) {
  
  df <- read_csv('https://docs.google.com/spreadsheets/d/1Ho-Vhs8k3y5Dm8QvJHRlj8h8In9vcN0jeH5SgT-Y2Fw/pub?gid=0&single=true&output=csv',
                 skip=1,
                 col_names=FALSE,
                 col_types=cols_only(X1=col_character(),
                                     X2=col_date(),
                                     X3=col_number(),
                                     X4=col_character(),
                                     X5=col_character(),
                                     X6=col_character(),
                                     X7=col_character(),
                                     X8=col_character(),
                                     X9=col_integer(),
                                     X10=col_character())
  ) %>%
    select(ID=X1, Date=X2, Name=X4, Address=X5, Locality=X6, State=X7, Zip=X8, Persons=X9, Notes=X10)
  
  geocodeables <- df %>%
    mutate(gAddress=trimws(paste0(ifelse(!is.na(Locality), paste0(Locality, ', '), ''), State, ' ', Zip))) %>%
    mutate(gAddress=ifelse(!is.na(Address), paste0(Address, ', ', gAddress), gAddress)) %>%
    mutate(gAddress=ifelse(!is.na(Zip) & is.na(Address) & is.na(Locality), trimws(Zip), gAddress)) %>%
    filter(!is.na(gAddress)) %>%
    select(ID, gAddress, Name, Persons, Notes, Date)
  
  df <- cbind(geocode(geocodeables$gAddress, cache='geocoder-cache.rds'), geocodeables) %>%
    select(ID, Latitude, Longitude, gAddress, Name, Persons, Notes, Date) %>%
    filter(!is.na(Latitude)) %>% filter(!is.na(Longitude)) %>%
    mutate(gAddress=gsub(x=gAddress, pattern='NA', replacement=''))
  
  minPersons <- min(df$Persons, na.rm=TRUE)
  maxPersons <- max(df$Persons, na.rm=TRUE)
  minDate <- min(df$Date, na.rm=TRUE)
  maxDate <- max(df$Date, na.rm=TRUE)
  
  addMapMarkers <- function(map, lng, lat, popup) {
    addMarkers(map,
               data=getMapData(map) %>% mutate(Date=ifelse(is.na(Date), 'Unknown Date', as.character(Date)),
                               Persons=ifelse(is.na(Persons), 'Unknown # of persons', as.character(Persons))),
               lng=~Longitude, lat=~Latitude, popup=~paste0(Name, '<br>', Date, '<br>', gAddress, '<br># of people: ', Persons))
  }
  
  getDataForDisplay <- function(df) {
    select(df, Date, gAddress, Name, Persons) %>%
      rename(Address=gAddress)
  }
  
  output$map <- renderLeaflet({
    leaflet(df) %>%
      addTiles(
        urlTemplate = "//{s}.tiles.mapbox.com/v3/jcheng.map-5ebohr46/{z}/{x}/{y}.png",
        attribution = 'Maps by <a href="http://www.mapbox.com/">Mapbox</a>'
      ) %>%
      addMapMarkers() %>%
      setView(lng = -93.85, lat = 37.45, zoom = 4)
  })
  
  output$table <- DT::renderDataTable(getDataForDisplay(df), options=list(searching=FALSE), selection='none')
  
  output$personsSlider <- renderUI(
    sliderInput("persons", "Number of persons:",
                min=minPersons, max=maxPersons, value=c(minPersons, maxPersons)
    )
  )
  
  output$dateRangeInput <- renderUI(
    dateRangeInput('dateRange', "Incident Date:", start=minDate, end=maxDate)
  )
  
  observe({
    
    if (!is.null(input$persons)) {
      
      minSelectedPersons <- input$persons[1]
      maxSelectedPersons <- input$persons[2]
      minSelectedDate <- input$dateRange[1]
      maxSelectedDate <- input$dateRange[2]
      
      showMissings <- input$showMissings
      
      pdf <- df %>%
        filter(Persons >= minSelectedPersons & Persons <= maxSelectedPersons | (is.na(Persons) & showMissings)) %>%
        filter(Date >= minSelectedDate & Date <= maxSelectedDate | (is.na(Date) & showMissings))
      
      leafletProxy("map", data=pdf) %>%
        clearMarkers() %>%
        addMapMarkers()
      
      DT::replaceData(DT::dataTableProxy('table'), getDataForDisplay(pdf))
      
    }
    
  })
  
}
