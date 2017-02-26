library(shiny)
library(leaflet)

shinyUI(fluidPage(
  
  tags$head(
    # Include our custom CSS
    includeCSS("styles.css")
  ),

  # Application title
  titlePanel("Immigration Incident Map"),

  sidebarLayout(
    sidebarPanel(
      h5("Filters"),
      uiOutput('personsSlider'),
      uiOutput('dateRangeInput'),
      checkboxInput('showMissings', 'Show incidents w/ missing date or #persons', value=TRUE),
      width = '3'),
    mainPanel(leafletOutput("map", width="100%", height="500"),
              DT::dataTableOutput('table'),
              width='9')
  )
  
))
