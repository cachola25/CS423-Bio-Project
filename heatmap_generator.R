library(shiny)
library(heatmaply)

# Define UI
ui <- fluidPage(
  titlePanel("Heatmap Generator"),
  sidebarLayout(
    sidebarPanel(
      fileInput("file1", "Choose CSV File",
                accept = c(
                  "text/csv",
                  "text/comma-separated-values,text/plain",
                  ".csv")
      ),
      tags$hr(),
      checkboxInput("header", "Header", TRUE),
      actionButton('getHmap', 'Generate Heatmap')
    ),
    mainPanel(
      tabsetPanel(
        tabPanel("Heatmap",
                 plotlyOutput("themap")),
        tabPanel("Heatmap Table",
                 tableOutput("table.output"))
      )
    )
  )
)

# Server logic
server <- function(input, output, session) {
  data <- reactiveVal(NULL) # Stores the CSV data
  
  # Read and return CSV data
  observeEvent(input$file1, {
    inFile <- input$file1 
    if (!is.null(inFile)) {
      data(read.csv(inFile$datapath, header = input$header))
    }
  })
  
  # Renders CSV as table
  output$table.output <- renderTable({
    data()
  })
  
  # Process data for heatmap
  plotdata <- eventReactive(input$getHmap, {
    if (!is.null(data())) {
      # Select all gene columns dynamically
      genes <- grep("^Gene\\.\\d+", names(data()), value = TRUE)
      heatmap_data <- cbind(data()[genes], data()[["Cell"]])
      colnames(heatmap_data) <- c(genes, "Cell")
      heatmap_data[is.na(heatmap_data)] <- 0 
      heatmaply(heatmap_data)
    }
  })
  
  # Render heatmap
  output$themap <- renderPlotly({ 
    plotdata()
  })
}

# Run the application
shinyApp(ui = ui, server = server)
