server <- function(input, output, session) {
  data <- reactiveVal(NULL) # Stores the CSV data
  
  # Read and return CSV data
  observeEvent(input$file1, {
    inFile <- input$file1 
    if (!is.null(inFile)) {
      data(read.csv(inFile$datapath, header = input$header))
    }
  })
  
  # Process data for heatmap
  plotdata <- eventReactive(input$getHmap, {
    if (!is.null(data())) {
      # Reshape data to wide format for heatmap
      data_wide <- reshape2::dcast(data(), Celltype ~ `Gene 1`, value.var = "Cell")
      
      # Extract cell type as row names
      row.names(data_wide) <- data_wide$Celltype
      data_wide$Celltype <- NULL
      
      # Replace NAs with 0
      data_wide[is.na(data_wide)] <- 0 
      
      # Create heatmap
      heatmaply(data_wide, xlab = "Genes", ylab = "Cell Types", main = "Heatmap of Cell Counts")
    }
  })
  
  # Render heatmap
  output$themap <- renderPlotly({ 
    plotdata()
  })
}
