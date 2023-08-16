var plotTypeSelect = document.getElementById("plotTypeSelect");
var startDatePicker = document.getElementById("startDatePicker");
var endDatePicker = document.getElementById("endDatePicker");
var groupDateSelect = document.getElementById("groupDateSelect");
var chart; // Variable to store the Highcharts chart instance


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

const yieldDataURL = document.getElementById('yieldDataURL').getAttribute('data-url');

if (plotTypeSelect.value === "bar") {
  var plot_type = "column";
} else if (plotTypeSelect.value == "line") {
  var plot_type = "line";
} else {
  // force to other options to vertical bar chart
  var plot_type = "column";
}

function createChart(data) {
  // Destroy previous chart instance if exists
  if (chart) {
    chart.destroy();
  }
  if (data.chart_type === "line" || data.chart_type === "bar") {
    // console.log(data.chart_type);
    // console.log(data.x_labels);
    Highcharts.chart("chartContainer", {
      chart: {
        type: data.chart_type,
      },
      title: {
        text: "Average Yield Data by Month",
      },
      xAxis: {
        categories: data.x_labels,
        title: {
          text: "Month",
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
        text: "Average Yield Data by Bin Type and Current Date",
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


  // fetch(
  //   yieldDataURL + '/?plot_type=' + plotTypeSelect.value + '&group_date=' + group_date + '&start_date=' + startDate + '&end_date=' + endDate + '&bin_types=' + selectedBinTypes + '&product_id=' + product_id
  // )
  fetch(
    `/get_data_highchart/?plot_type=${plotTypeSelect.value}&group_date=${group_date}&start_date=${startDate}&end_date=${endDate}&bin_types=${selectedBinTypes}&product_id=${product_id}`
    )
    .then((response) => response.json())
    .then((data) => {
      // pass the data from view to js function to create highcharts
      createChart(data.highcharts_data);
      updateDataTable(data.datatable_data);
    });
}

// update the DataTable
function updateDataTable(data) {
  // Destroy existing DataTable if it exists
  if ($.fn.DataTable.isDataTable(dataTableContainer)) {
    dataTable = $(dataTableContainer).DataTable();
    dataTable.clear().destroy();
  }
  
  var dataTableContainer = document.getElementById("dataTableContainer");
  var current_plot_type = plotTypeSelect.value;
  var dataTable;
  console.log(data);

  // Create or update DataTable using the 'data' parameter
  // Define columns based on the chart_type
  console.log("Current plot type", current_plot_type)
  var columns;
  if (current_plot_type === "bar" || current_plot_type === "line") {
    columns = [
      {
        title: "Date",
        data: "current_date",
        render: function (data, type, row) {
          // render link to click show modal
          if (type === "display") {
            return '<a href="#" class="date-link">' + data + "</a>";
          }
          return data;
        },
      },
      { title: "Total Lots", data: "total_lots" },
      { title: "Total Wafers", data: "total_wafers" },
      { title: "Average Yield", data: "avg_yield" },
    ];
  } else {
    console.log("process here");
    // Define columns for other chart types if needed
      // Create columns dynamically based on the first data item keys
      Object.keys(data[0]).map(key => {
        // var show_data = {"title":key, "data":key, "function":function(data, type, row){return data}};
        // console.log(show_data);
        console.log("pass");
        console.log(key);
      });
      columns = Object.keys(data[0]).map(key => {
        return {
            title: key,
            data: key
        };
    });
  }

  console.log("------------------------------------------------------------------------")
  console.log(columns);
  console.log("------------------------------------------------------------------------")


  // fill the data and set the datatable 
  $(dataTableContainer).DataTable({
    destroy: true,
    scrollY: "200px", // add a scroll bar
    data: data, // Replace with actual data from 'data' object
    columns: columns,
    searching: false, // Disable search bar
    paging: false, // Disable pagination
    info: false, // Disable info display
  });

  $(document).ready(function () {
    dataTable = $("#dataTableContainer").DataTable();
  });

  // Handle click event for date link and show modal
  $("#dataTableContainer").on("click", ".date-link", function () {
    // console.log($(this));

    var rowData = dataTable.row($(this).closest("tr")).data();
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
        if ($.fn.dataTable.isDataTable("#detailsDataTable")) {
          $("#detailsDataTable").DataTable().destroy();
        }
        console.log("AJAX data:");
        console.log(data);
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
            // ... other columns ...
          ],
          // ... other options ...
          searching: false, // Disable search bar
          info: false, // Disable info display
          scrollY: "200px", // add a scroll bar
        });
        $("#modalDate").text(modalDate);
        $("#detailsModal").modal("show");
      }
    );
  });

  
//   $(document).ready(function () {
//     dataTable_details = $("#detailsTableContainer").DataTable();
//   });
//     // Handle click event for lot link and direct it another page 
//     $("#detailsTableContainer").on("click", ".lot-link", function () {
//         var rowData = dataTable_details.row($(this).closest("tr")).data();
//         console.log(rowData);
//         var rootLotId = rowData.root_lot_id; // assuming root_lot_id is the key for the Root Lot ID

//         // Construct the URL. If Root Lot ID is a parameter in the URL
//         var newTabURL = `http://127.0.0.1:8000/wafermap/`;  // adjust this based on how your backend is set up

//         // Open the URL in a new tab
//         window.open(newTabURL, '_blank');
//     });

}



plotTypeSelect.addEventListener("change", updateChart);
startDatePicker.addEventListener("change", updateChart);
endDatePicker.addEventListener("change", updateChart);
binType.addEventListener("change", updateChart);
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
