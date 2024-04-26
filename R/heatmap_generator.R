library(shiny)
library(pheatmap)
library(dplyr)

# Define UI
ui <- fluidPage(
  titlePanel("Heatmap Generator"),
  sidebarLayout(
    sidebarPanel(
      # Tabs for different sections
      tabsetPanel(
        tabPanel("Generate Heatmap",
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
      )
    ),
    mainPanel(
      tabsetPanel(
        tabPanel("Heatmap",
                 plotOutput("themap")),
        tabPanel("Heatmap Table",
                 tableOutput("table.output"))
      )
    )
  )
)

# Server logic
server <- function(input, output, session) {
  data <- reactiveVal(NULL)
  
  # Read and return CSV data
  observeEvent(input$file1, {
    inFile <- input$file1 
    if (!is.null(inFile)) {
      data(read.csv(inFile$datapath, header = input$header))
    }
  })
  
  # Render CSV as table
  output$table.output <- renderTable({
    data()
  })
  
  # Process data for heatmap
  plotdata <- eventReactive(input$getHmap, {
    if (!is.null(data())) {
      clustered_data <- data() %>%
        group_by(Celltype) %>%
        summarise(across(-Barcode, sum)) %>%
        ungroup()
      
      rownames(clustered_data) <- clustered_data$Celltype
      clustered_data <- clustered_data[, -1]
      clustered_data[is.na(clustered_data)] <- 0
      clustered_data
    }
  })
  
  # Render heatmap
  output$themap <- renderPlot({ 
    if (!is.null(plotdata())) {
      pheatmap(plotdata())
    }
  })
  
  
}

# Run the application
shinyApp(ui = ui, server = server)
