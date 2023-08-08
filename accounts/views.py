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

from .models import Person, Commodity, FormData, YieldData
from django_tables2 import SingleTableView

import os 
import json 
import pandas as pd 
import datetime 
from .forms import FormDataForm


# def home(request):
#     return render(request,'accounts/dashboard.html')

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
# https://blog.csdn.net/weixin_42289273/article/details/109408689
# https://www.twblogs.net/a/5c10ec5abd9eee5e40bb1105
# add button in front of the table 
# https://stackoverflow.com/questions/52478489/bootstrap-4-collapse-accordion-table-in-django

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
        # Calculate default start and end dates
    current_date = datetime.datetime.now().date()
    default_end_date = current_date.strftime('%Y-%m-%d')
    default_start_date = (current_date - datetime.timedelta(days=14)).strftime('%Y-%m-%d')

    context = {
        'default_start_date': default_start_date,
        'default_end_date': default_end_date,
    }

    return render(request, 'accounts/highchart.html', context)
    # return render(request, 'accounts/highchart.html')


def get_data_highchart(request):
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

    chart_data = {
        'x_labels': grouped_data['current_date'].tolist(),
        'y_values': grouped_data['yield_value'].tolist(),
        'chart_type': plot_type,
    }

    return JsonResponse(chart_data)