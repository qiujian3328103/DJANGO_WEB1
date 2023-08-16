from django.shortcuts import render, redirect,  get_object_or_404
from django.http import HttpResponse, JsonResponse, FileResponse
import plotly.graph_objects as go
from plotly.offline import plot
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import HoverTool, CustomJS, ColumnDataSource, Select, DateRangeSlider, DatePicker
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap
from bokeh.layouts import column, row 

from bokeh.resources import CDN
from django.views.generic import ListView

from .models import Person, Commodity, FormData, YieldData, ProductList, BinDescription
from django_tables2 import SingleTableView
from django.core.cache import cache
from django.views.decorators.cache import cache_page
import os 
import json 
import pandas as pd 
import datetime 
from .forms import FormDataForm
from .query import get_filtered_data

# https://blog.csdn.net/weixin_42289273/article/details/109408689
# https://www.twblogs.net/a/5c10ec5abd9eee5e40bb1105
# add button in front of the table 
# https://stackoverflow.com/questions/52478489/bootstrap-4-collapse-accordion-table-in-django


def products(request):
    return render(request,"accounts/product.html")

def customer(request):
    return render(request,"accounts/customer.html")


def serve_image(request, image_name):
    image_path = os.path.join('accounts', 'static', 'images', image_name)
    print(image_path)
    return FileResponse(open(image_path, 'rb'), content_type='image/jpeg')

def plot(request):
    # Sample data
    x = [1, 2, 3, 4, 5]
    y = [2, 5, 8, 2, 7]

    # Create a ColumnDataSource with the data
    source = ColumnDataSource(data={'x': x, 'y': y})

    # Create a simple Bokeh plot
    plot = figure(plot_width=400, plot_height=400, title='Hover over the data points to see the image')

    # Add the data points to the plot
    circle = plot.circle('x', 'y', source=source, size=15, fill_color='blue', line_color='black', fill_alpha=0.6)

    # Define the image URL to be shown on hover
    image_name = "R.jpg"  # Change this to the actual filename of your image
    image_url = f"/images/{image_name}"
    
    # Define the CustomJS callback to update the tooltip content with the image
    custom_hover_js = CustomJS(args={'image_url': image_url}, code="""
        if (cb_data.index.indices.length > 0) {
            const index = cb_data.index.indices[0];
            const img = new Image();
            img.src = image_url;
            img.style.max-width = '100px';  // Set the maximum width for the image in the tooltip
            img.style.max-height = '100px'; // Set the maximum height for the image in the tooltip

            // Create the tooltip content
            const div = document.createElement('div');
            div.appendChild(document.createTextNode('X: ' + cb_data.source.data.x[index]));
            div.appendChild(document.createElement('br'));
            div.appendChild(document.createTextNode('Y: ' + cb_data.source.data.y[index]));
            div.appendChild(document.createElement('br'));
            if (index === 1) {
                div.appendChild(img);
            }

            // Get the tooltip element and update its content
            const tooltips = document.getElementsByClassName('bk-tooltip');
            if (tooltips.length > 0) {
                tooltips[0].innerHTML = '';
                tooltips[0].appendChild(div);
            }
        }
    """)

    # Attach the CustomJS callback to the circle renderer using the HoverTool
    # hover = HoverTool(renderers=[circle], callback=custom_hover_js)
    hover = HoverTool(
            tooltips="""
            <div>
                <div>
                    <img
                        src="@pics" height="42" alt="@imgs" width="42"
                        style="float: left; margin: 0px 15px 15px 0px;"
                        border="2"
                    ></img>
                </div>
            <...other div tags for text>
            """
        )
    # Add the HoverTool to the plot
    plot.add_tools(hover)

    # Generate the necessary components to embed the plot
    script, div = components(plot, CDN)

    return render(request, 'accounts/dashboard.html', {'script': script, 'div': div})


def netinfo(request):  # ajax的url
    data_list = []
    query_set = Commodity.objects.all()
    for data_info in query_set:
        data_list.append({
            'id': data_info.id,
            'commodity_number': data_info.commodity_number,
            'three_type': data_info.three_type,
            'two_type': data_info.two_type,
            'commodity_name': data_info.commodity_name,
            'short_name': data_info.short_name,
            'agent_price': str(data_info.agent_price),
            "finance_sales": data_info.finance_sales,
            "income": str(data_info.income),
            'unit_price': str(data_info.unit_price),
            "agent_cost": str(data_info.agent_cost),
            "agent_profit": str(data_info.agent_profit),
            "date": str(data_info.date)
        })
    data_dic = {}
    data_dic['data'] = data_list  # 格式一定要符合官网的json格式，否则会出现一系列错误
    return HttpResponse(json.dumps(data_dic))


def datatable_view(request):
    data = Person.objects.all()
    return render(request, 'accounts/datatable_template.html', {'data': data})


def get_form_data_json(request):
    data = FormData.objects.values('id', 'username', 'email', 'hyperlink', 'text_area')
    return JsonResponse({'data': list(data)})


def datatable_view_form(request):
    return render(request, 'accounts/datatable_template2.html')


def form_view(request, entry_id=None):
    """_summary_
    Add a new username or update the rest information if the username already exists.
    Args:
        request (_type_): _description_
        entry_id (int, optional): The ID of the entry to edit. Defaults to None.

    Returns:
        _type_: _description_
    """
    show_modal_success = False

    if entry_id:
        existing_entry = get_object_or_404(FormData, id=entry_id)
        if request.method == 'POST':
            form = FormDataForm(request.POST, instance=existing_entry)
            if form.is_valid():
                form.save()
                show_modal_success = True
        else:
            form = FormDataForm(instance=existing_entry)
    else:
        if request.method == 'POST':
            form = FormDataForm(request.POST)
            if form.is_valid():
                form.save()
                show_modal_success = True
        else:
            form = FormDataForm()

    return render(request, 'accounts/form_template.html', {'form': form, 'show_modal_success': show_modal_success})


def delete_entry(request):
    if request.method == 'POST':
        entry_id = request.POST.get('entry_id')
        try:
            # Delete the entry from the database using the entry_id
            entry = FormData.objects.get(id=entry_id)
            entry.delete()
            return JsonResponse({'status': 'success'})
        except FormData.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Entry not found.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def home(request):
    """_summary_
    dashboard 
    Args:
        request (_type_): _description_
    """
    # Retrieve data from the yield_data table
    # Retrieve data from the yield_data table
    data = YieldData.objects.all()
    # conver the data to pandas dataframe 
    df = pd.DataFrame(list(data.values()))
    # coert the date column to a datetime object 
    df['date'] = pd.to_datetime(df['date'])
    # add a new column and covert to Month-Y
    df['current_date'] = df['date'].dt.strftime('%b-%Y')
    # get the average yield value for each date 
    grouped_data = df.groupby('current_date')['yield_value'].mean().reset_index()



    # Create a Bokeh plot
    plot = figure(x_range=grouped_data['current_date'],
                   title='Average Yield by Month',
                     x_axis_label='Month',
                       y_axis_label='Average Yield')

    # Create a ColumnDataSource for the data
    source = ColumnDataSource(grouped_data)

    # Create a Bokeh plot
    plot = figure(x_range=grouped_data['current_date'], title='Average Yield by Month', x_axis_label='Month', y_axis_label='Average Yield')

    # Create a factor_cmap for color mapping
    factors = grouped_data['current_date'].tolist()
    # colors = factor_cmap('current_date', palette='Category20', factors=factors)

    # Plot the initial bar chartcolors
    bars = plot.vbar(x='current_date', top='yield_value', source=source, width=0.5, line_color="white")

    # Create Select widget for plot type
    plot_type_select = Select(title='Plot Type', value='bar', options=['bar', 'line'])

    # Create DateRangeSlider widget for date filter
    date_range_slider = DateRangeSlider(title='Date Range', start=df['date'].min(), end=df['date'].max(), value=(df['date'].min(), df['date'].max()))

    def update_plot_type(attr, old, new):
        if plot_type_select.value == 'bar':
            plot.renderers = [bars]
        else:
            lines = plot.line(x='current_date', y='yield_value', source=source, line_width=2, line_color='blue')
            plot.renderers = [lines]

    # plot_type_select.on_change('value', update_plot_type)

    # def update_date_range(attr, old, new):
    #     date_filter = (df['date'] >= date_range_slider.value[0]) & (df['date'] <= date_range_slider.value[1])
    #     filtered_data = df[date_filter]
    #     grouped_data = filtered_data.groupby('current_date')['yield_value'].mean().reset_index()
    #     source.data = ColumnDataSource(grouped_data).data
    # date_range_slider.on_change('value', update_date_range)

    date_picker = DatePicker(
    title="Select date",
    value="2019-09-20",
    min_date="2019-08-01",
    max_date="2019-10-30",
    )
    date_picker.js_on_change("value", CustomJS(code="""
    console.log("date_picker: value=" + this.value, this.toString())
    """))
    
    widgets = row(plot_type_select, date_picker)

    # Show the Bokeh plot
    script, div = components(column(widgets, plot))

    context = {
        'script': script,
        'div': div,
    }
    return render(request, 'accounts/dashboard.html', context)


def chartjs_plot(request):
    data = YieldData.objects.all()

    # Convert data to a Pandas DataFrame
    df = pd.DataFrame(list(data.values()))

    # Convert the 'date' column to a datetime object
    df['date'] = pd.to_datetime(df['date'])

    # Add a new column 'current_date' in "Month-Y" format
    df['current_date'] = df['date'].dt.strftime('%b-%Y')

    # Group data by 'current_date' and calculate the average yield_value
    grouped_data = df.groupby('current_date')['yield_value'].mean().reset_index()

    # Get unique values of 'current_date' for x-axis labels
    x_labels = grouped_data['current_date'].tolist()

    context = {
        'x_labels': x_labels,
    }
    return render(request, 'accounts/dashboard2.html', context)


def get_data(request):
    # Get plot type and date range filter parameters from AJAX request
    plot_type = request.GET.get('plot_type', 'bar')
    start_date = pd.to_datetime(request.GET.get('start_date'))
    end_date = pd.to_datetime(request.GET.get('end_date'))

    data = YieldData.objects.all()

    # Convert data to a Pandas DataFrame
    df = pd.DataFrame(list(data.values()))

    # Convert the 'date' column to a datetime object
    df['date'] = pd.to_datetime(df['date'])

    # Add a new column 'current_date' in "Month-Y" format
    df['current_date'] = df['date'].dt.strftime('%b-%Y')

    # Filter data based on date range
    filtered_data = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # Group data by 'current_date' and calculate the average yield_value
    grouped_data = filtered_data.groupby('current_date')['yield_value'].mean().reset_index()

    if plot_type == 'bar':
        chart_type = 'bar'
    else:
        chart_type = 'line'

    chart_data = {
        'labels': grouped_data['current_date'].tolist(),
        'data': grouped_data['yield_value'].tolist(),
        'chart_type': chart_type,
    }

    return JsonResponse(chart_data)


def highchart_plot(request):
    product_data = ProductList.objects.all() 
    unique_bin_groups = BinDescription.objects.values_list('BIN_GROUP', flat=True).distinct()
    context = {
        'product_data': product_data,
        'unique_bin_groups': unique_bin_groups,
    }
    return render(request, 'accounts/highchart.html', context)
    # return render(request, 'accounts/highchart.html')

def get_data_highchart(request):
    # Get plot type and date range filter parameters from AJAX request
    plot_type = request.GET.get('plot_type', 'bar')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    product_id = request.GET.get('product_id')
    bin_types = request.GET.get('bin_types')
    group_date = request.GET.get('group_date')

    cache_key = f"data_highchart_{product_id}_{start_date_str}_{end_date_str}"
    df_raw = cache.get(cache_key)

    if df_raw is None:
        print("test start cache")
        df_raw = get_filtered_data(product_id=product_id, start_date=start_date_str, end_date=end_date_str)
        cache.set(cache_key, df_raw, 3600)
        print(df_raw)

    if plot_type == "bar":
        # vertical bar plot 
        plot_type == "column"
    elif plot_type == "line":
        plot_type == "line"


    if bin_types=='':
        bin_types_list = ["YIELD"]
    else:
        bin_types_list = bin_types.split(",")
    
    start_date = pd.to_datetime(start_date_str)
    
    end_date = pd.to_datetime(end_date_str)
 

    df = df_raw

    # fitler the data 
    # print(product_id)
    df = df[df['product_id'] == product_id]

    # convert the data base on the select date 
    df["date"] = pd.to_datetime(df['date'])
    if group_date == "Month":
        df['current_date'] = df['date'].dt.strftime('%Y-%m')
    elif group_date == "Week":
        df['current_date'] = df['date'].dt.strftime('%Y-%W')
    elif group_date == "Quarter":
        df['current_date'] = df['date'].dt.to_period('Q').dt.strftime('%Y-Q%q')

    # Filter data based on date range
    filtered_data = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    print(filtered_data.head(n=50))
    # based on the plot type to decide the plot 
    if plot_type == "bin_group":
        # select bin_group, use the bin_types_list to filter the the customer select bin_types 
        filtered_data = filtered_data[filtered_data['bin_type'].isin(bin_types_list)]
        # Process the data to calculate average yield values for each bin type and current date
        grouped_data = filtered_data.groupby(['bin_type', 'current_date'])['yield_value'].mean().reset_index()
        # Prepare the data in a format suitable for Highcharts
        unique_bin_types = grouped_data['bin_type'].unique()

        series_data = []
        for current_date in grouped_data['current_date'].unique():
            series_data.append({
                'name': current_date,
                'data': grouped_data[grouped_data['current_date'] == current_date]['yield_value'].tolist()
            })
        highcharts_data = {
            'bin_types': unique_bin_types.tolist(),
            'series': series_data,
            'chart_type': plot_type
        }
        # Pivot the DataFrame
        datatable_data = filtered_data.pivot_table(index='current_date', columns='bin_type', values='yield_value', aggfunc='mean')
        # Reset the index
        datatable_data = datatable_data.reset_index()
        datatable_data = datatable_data.sort_values(by='current_date')

        # Prepare the data in a format suitable for DataTables
        chart_data = {
            "highcharts_data": highcharts_data,
            "datatable_data": datatable_data.to_dict("records") if not datatable_data.empty else [],
        }

    else:
        # Group data by 'current_date' and calculate the average yield_value
        grouped_data = filtered_data.groupby('current_date')['yield_value'].mean().reset_index()
        # highchart data to render 
        highcharts_data = {
            'x_labels': grouped_data['current_date'].tolist(),
            'y_values': grouped_data['yield_value'].tolist(),
            'chart_type': plot_type,
        }
        # datatable_data to render 
        datatable_data = (
            filtered_data
            .groupby("current_date")
            .agg(
                total_lots=("root_lot_id", "nunique"),
                total_wafers=("wafer_id", "count"),
                avg_yield=("yield_value", "mean")
            )
            .reset_index()
        )

        datatable_data = datatable_data.sort_values(by='current_date')

        chart_data = {
        "highcharts_data": highcharts_data,
        "datatable_data": datatable_data.to_dict("records") if not datatable_data.empty else [],
        }


    return JsonResponse(chart_data)


def get_data_for_table_modal(request):
    product_id = request.GET.get('product_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    print(product_id, start_date, end_date)
    # query the data from the datatable 
    data = YieldData.objects.filter(
        product_id=product_id,
        date__range=[start_date, end_date]
    ).values() 

    return JsonResponse(list(data), safe=False)


def wafermap(request):
    # df_raw = pd.read_csv(r"C:\Users\Jian Qiu\Dropbox\pythonprojects\django_web1\sample.csv", index_col=False)
    df_raw = pd.read_csv(r"/Users/JianQiu/Dropbox/pythonprojects/django_web1/sample.csv", index_col=False)
    
    # Filter out rows based on "sort_test_flag"
    df = df_raw[df_raw["sort_test_flag"] == "T"]
    width = 7270.96*0.001
    height = 6559.46*0.001

    df['left'] = df['ucs_die_origin_x']*0.001 
    df['right'] = df['ucs_die_origin_x']*0.001
    df['bottom'] = df['ucs_die_origin_y'] *0.001
    df['top'] = df['ucs_die_origin_y']*0.001
    # Setting the width and height

    # Map the ucs_die_origin_x and ucs_die_origin_y to x and y, and set color
    df["color"] = "green"
    
    # Generate a list of dictionaries to match the format needed for D3.js
    wafer_data = df.apply(lambda row: {
        "x": row["left"],
        "y": row["bottom"],
        "color": row["color"],
        "mouseover": f"Die_x: {int(row['sort_die_x'])}\nDie_y: {int(row['sort_die_y'])}"
    }, axis=1).tolist()

    context = {
        'waferData': wafer_data,
        'rectWidth': width,
        'rectHeight': height,
        'wafer_range': range(1, 26), 
    }
    return render(request, 'accounts/wafermap.html', context)


def table_sparkline(request):
    """_summary_
    Show datatable with a sparkline. Use the yield_table data 

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    return render(request, 'accounts/datatable_sparkline.html')


def get_sparkline_data(request):
    """_summary_
    Get data for the sparkline. Use the yield_table data 

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Get the data from the yield_table
    data = YieldData.objects.all()

    # Filter the data
    # Convert data to a Pandas DataFrame
    df = pd.DataFrame(list(data.values()))

    # convert the data base on the select date 
    df["date"] = pd.to_datetime(df['date'])

    # get bin types 
    bin_types = df['bin_type'].unique().tolist()
    context = []
    # loop by the bin types and get the week list 
    for bin_type in bin_types:
        bin_data = df[df['bin_type'] == bin_type]
        sparkline_data = bin_data.groupby(bin_data['date'].dt.week)['yield_value'].mean()
        sparkline = [round(val, 2) for val in sparkline_data.tolist()]
        
        context.append({
            'bin_type': bin_type,
            'sparkline': sparkline,
        })

    return JsonResponse({'data': context})



    # wafer_data = df[['left', 'right', 'bottom', 'top', 'color']].to_dict(orient='records')
    # df = df.head(n=1200)
    
    # drop the na 
    # wafer_data = []
    # for _, row in df.iterrows():
    #     x = (row['left'] + row['right']) / 2
    #     y = (row['bottom'] + row['top']) / 2
    #     color = row["color"]
    #     wafer_data.append({'x': x, 'y': y, 'color': color})
