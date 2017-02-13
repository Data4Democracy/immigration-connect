dir.create("r-packages", showWarnings=FALSE)
.libPaths(c('r-packages', .libPaths()))
install.packages(c('leaflet', 'ggmap'), lib='r-packages')
devtools::install_github('scottcame/geocode', lib='r-packages', dependencies=FALSE)