library(shiny)
library(pheatmap)
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
        tabPanel("Customize Heatmap",
                 selectInput("variable1", "Select Variable 1", choices = NULL),
                 selectInput("variable2", "Select Variable 2", choices = NULL),
                 actionButton("update_heatmap", "Update Heatmap")
        )
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
      a <- as.matrix(data()[-1])
      row.names(a) <- data()$Name 
      a[is.na(a)] <- 0 
      a
    }
  })
  
  # Render heatmap
  output$themap <- renderPlot({ 
    if (!is.null(plotdata())) {
      pheatmap(plotdata())
    }
  })
  
  # Update selectInput choices when data is available
  observe({
    if (!is.null(data())) {
      updateSelectInput(session, "variable1", choices = colnames(data()))
      updateSelectInput(session, "variable2", choices = colnames(data()))
    }
  })
  
  # Generate heatmap based on selected variables
  observeEvent(input$update_heatmap, {
    if (!is.null(data())) {
      plotdata(matrix(data()[, c(input$variable1, input$variable2)]))
    }
  })
}

# Run the application
shinyApp(ui = ui, server = server)
