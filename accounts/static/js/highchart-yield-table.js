/** 
 *  for the const yieldDataURL only works in the Django template, the JS cannot read the {{}} tag
 *  to solve the issue, need to pass the url from the html into the js to do that, need to fetch the 
 *  variable in the js code 
 *  no longer have access to Django template tags directly.
 * 
 *  // for AJAX fetch the correct url
 *  const yieldDataURL = "{% url 'get_yield_data_for_modal' %}";
 * 
 * **/

var plotTypeSelect = document.getElementById("plotTypeSelect");
var startDatePicker = document.getElementById("startDatePicker");
var endDatePicker = document.getElementById("endDatePicker");
var groupDateSelect = document.getElementById("groupDateSelect");
var chart; // Variable to store the Highcharts chart instance
// var detailsDataTable; // Define it at the top level

const yieldDataURL = document.getElementById('yieldDataURL').getAttribute('data-url');

if (plotTypeSelect.value === "bar") {
  var plot_type = "column";
} else if (plotTypeSelect.value == "line") {
  var plot_type = "line";
} else {
  // force to other options to vertical bar chart
  var plot_type = "column";
}

// update the binType based on the product id 
function updateBinTypeOptions() {
  var selectedProductID = productID.value;
  fetch(`/get_bin_groups/?product_id=${selectedProductID}`)
      .then(response => response.json())
      .then(data => {
          binType.innerHTML = "";  // Clear current options
          data.forEach(binGroup => {
              var option = document.createElement("option");
              option.value = binGroup;
              option.text = binGroup;
              binType.appendChild(option);
          });
      });
}

productID.addEventListener("change", function() {
  updateBinTypeOptions();
  updateChart();
});



function createChart(data) {
  // Destroy previous chart instance if exists
  var by_date = document.getElementById("groupDateSelect").value;
  if (chart) {
    chart.destroy();
  }
  if (data.chart_type === "line" || data.chart_type === "bar") {
    // if bar chart use the column to make it vertical bar 
    if (data.chart_type === "bar"){
        var plot_type_select = "column"
    }else{
      var plot_type_select = "line"
    }
    // define the highcharts 
    Highcharts.chart("chartContainer", {
      chart: {
        type: plot_type_select,
      },
      title: {
        text: `Average Yield Data by ${by_date}`,
      },
      xAxis: {
        categories: data.x_labels,
        title: {
          text: by_date,
        },
      },
      yAxis: {
        title: {
          text: "Average Yield",
        },
      },
      series: [
        {
          name: "Average Yield",
          data: data.y_values,
        },
      ],
      legend: {
        layout: "vertical",
        align: "right",
        verticalAlign: "middle",
      },
      // Add other Highcharts options as needed
    });
  } else {
    // console.log(data.bin_types);
    Highcharts.chart("chartContainer", {
      chart: {
        type: "column",
      },
      title: {
        text: "Average Yield Data",
      },
      xAxis: {
        categories: data.bin_types,
        title: {
          text: "Bin Type",
        },
      },
      yAxis: {
        title: {
          text: "Average Yield",
        },
      },
      series: data.series,
      legend: {
        layout: "vertical",
        align: "right",
        verticalAlign: "middle",
      },
    });
  }
}

// update the highchart plot to create a new chart
function updateChart() {
  var startDate = startDatePicker.value;
  var endDate = endDatePicker.value;
  var product_id = productID.value;
  var group_date = groupDateSelect.value;
  var selectedBinTypes = Array.from(
    binType.selectedOptions,
    (option) => option.value
  );
  
  // AJAX to fetch the current selection then post to views.py to do the data process 
  fetch(
    `/get_data_highchart/?plot_type=${plotTypeSelect.value}&group_date=${group_date}&start_date=${startDate}&end_date=${endDate}&bin_types=${selectedBinTypes}&product_id=${product_id}`
    )
    .then((response) => response.json())
    .then((data) => {
      // pass the data from views.py processed data to js function to create highcharts
      createChart(data.highcharts_data);
      updateDataTable(data.datatable_data);
    });
}

// update the DataTable
function updateDataTable(data) {
  // remove the dataTable if exist 
  if ($.fn.DataTable.isDataTable('#dataTableContainer')) {
    $('#dataTableContainer').off("click", ".date-link");
    console.log("test if there is a datatbale ")
    $('#dataTableContainer').DataTable().destroy();
  }
  
  // if ($.fn.DataTable.isDataTable('#detailsDataTable')) {
  //   console.log("there is a datatable");
  //   $('#detailsDataTable').off("click", ".lot-link"); 
  //   $('#detailsDataTable').DataTable().destroy();
  // }

  var dataTableContainer = document.getElementById("dataTableContainer");
  var current_plot_type = plotTypeSelect.value;
  var dataTable;

  console.log("Current plot type", current_plot_type)
  var columns;
  let allKeys = Object.keys(data[0]);
  
  // Define columns based on the chart_type
  columns = allKeys.map(key => {
    return {
      title: key.charAt(0).toUpperCase() + key.slice(1).replace(/_/g, ' '),
      data: key,
      render: function (data, type, row) {
        // render link to click show modal
        if (type === "display" && key === "current_date" ) {
          return '<a href="#" class="date-link">' + data + "</a>";
        }
        return data;
      },
    }
  })


  // ************************** import step *********************************//
  // Clear the table body and header to to ensure that the old data is removed.
  $('#dataTableContainer thead').empty();
  $('#dataTableContainer tbody').empty();
  // $('#detailsDataTable thead').empty();
  // $('#detailsDataTable tbody').empty();
  // fill the data and set the datatable 
  dataTable = $(dataTableContainer).DataTable({
    destroy: true,
    scrollY: "200px", // add a scroll bar
    data: data, // Replace with actual data from 'data' object
    columns: columns,
    searching: false, // Disable search bar
    paging: false, // Disable pagination
    info: false, // Disable info display
  });

  // Handle click event for date link and show modal
  $("#dataTableContainer").on("click", ".date-link", function () {
    // console.log($(this));

    var rowData = dataTable.row($(this).closest("tr")).data();
    // console.log(rowData);
    var modalDate = rowData.current_date;

    // get the current selection status and use AJAX to fetch back to views.py
    var product_id = document.getElementById("productID").value;
    var start_date = document.getElementById("startDatePicker").value;
    var end_date = document.getElementById("endDatePicker").value;
    
    // AJAX request to get the yield data
    $.get(
      yieldDataURL,
      { product_id: product_id, start_date: start_date, end_date: end_date },
      function (data) {
        // delete the modal if modal already created
        // remove the modal datatable if exist 

        var detailsDataTable = $("#detailsDataTable").DataTable({
          // ... options for the details DataTable ...
          data: data, // Replace with the actual details data
          columns: [
            { title: "Root Lot ID",
              data: "root_lot_id",
              render: function (data, type, row) {
                // render link to click show modal
                if (type === "display") {
                  return '<a href="#" class="lot-link">' + data + "</a>";
                }
                return data;
              },
            },
            { title: "Wafer ID", data: "wafer_id" },
            { title: "Yield", data: "yield_value" },
            { title: "PRODUCT_ID", data: "product_id" },
            { title: "BIN TYPE", data: "bin_type" },
          ],
          searching: false, // Disable search bar
          info: false, // Disable info display
          scrollY: "200px", // add a scroll bar
        });
        $("#modalDate").text(modalDate);
        $("#detailsModal").modal("show");
      }
    );
  });


  $("#detailsDataTable").on("click", ".lot-link", function (event) {
    event.preventDefault(); // Prevent the default action of the hyperlink
    /*
     * detailsDataTable.row  method being undefined is likely because of the scope of the 
     * detailsDataTable variable. In updateDataTable function,  define detailsDataTable as
     * a local variable: means that the detailsDataTable variable is only accessible within
     * the updateDataTable function. When you try to access it in the event handler for the 
     * .lot-link click event, it's out of scope, and thus, it's undefined.
     * 
     * // Fetch the data for the row that was clicked
     * var rowData = detailsDataTable.row($(this).closest("tr")).data();
     * use a more direct approach with jQuery.
     * 
     * var $row = $(this).closest("tr");
     * // Extract data directly from the row's cells
     * var rowData = {
     * root_lot_id: $row.find("td:eq(0)").text(),
     * wafer_id: $row.find("td:eq(1)").text(),
     * yield_value: $row.find("td:eq(2)").text(),
     * product_id: $row.find("td:eq(3)").text(),
     * bin_type: $row.find("td:eq(4)").text()
     * }
     * 
     * Downside for this method is that, it can only use on the fix structure table, 
     * if data is dynamic, then cannot determine each columns value. 
     * 
     */


    // Get the parent row of the clicked link
    var $row = $(this).closest("tr");
    // Extract data directly from the row's cells
    var root_lot_id = $row.find("td:eq(0)").text();
    console.log(root_lot_id);

    // Redirect to the desired URL use '_blank' to open a new tab. 
    var newTabURL = `http://127.0.0.1:8000/wafermap/`;
    window.open(newTabURL, '_blank');
    // window.location.href = `http://127.0.0.1:8000/wafermap/`;
  });
}

plotTypeSelect.addEventListener("change", updateChart);
startDatePicker.addEventListener("change", updateChart);
endDatePicker.addEventListener("change", updateChart);
// binType.addEventListener("change", updateChart);
productID.addEventListener("change", updateChart);
groupDateSelect.addEventListener("change", updateChart);

// Calculate default start and end dates
var currentDate = new Date();
var defaultEndDate = currentDate.toISOString().split("T")[0];
var fourteenDaysAgo = new Date(currentDate);
fourteenDaysAgo.setDate(currentDate.getDate() - 14);
var defaultStartDate = fourteenDaysAgo.toISOString().split("T")[0];

startDatePicker.value = defaultStartDate;
endDatePicker.value = defaultEndDate;

// Call updateChart initially to populate the initial data
updateChart();


