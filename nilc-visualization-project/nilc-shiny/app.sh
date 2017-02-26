# shell script for domino

R -e '.libPaths(c(.libPaths(), "r-packages"));shiny::runApp("./", port=8888, host="0.0.0.0")'