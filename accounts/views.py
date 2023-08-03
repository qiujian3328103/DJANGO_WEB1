from django.shortcuts import render, redirect
from django.http import HttpResponse
import plotly.graph_objects as go
from plotly.offline import plot
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.resources import CDN
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, CustomJS, ColumnDataSource
from bokeh.resources import CDN
from django.views.generic import ListView
from .models import Person 
from django_tables2 import SingleTableView

# Create your views here.
from django.http import FileResponse
import os 
from .models import Person, Commodity
from .tables import PersonTable
import json 
from .forms import FormDataForm
from django.http import JsonResponse
from .models import FormData
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

def home(request):
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

class PersonListView(SingleTableView):
    model = Person
    table_class = PersonTable
    template_name = 'accounts/people.html'



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


# def form_view(request):
#     """_summary_
#     add a new username, if the username is exist, update the rest information 
#     else add the new username.
#     Args:
#         request (_type_): _description_

#     Returns:
#         _type_: _description_
#     """
#     if request.method == 'POST':
#         form = FormDataForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             email = form.cleaned_data['email']
#             hyperlink = form.cleaned_data['hyperlink']
#             text_area = form.cleaned_data['text_area']

#             # Check if the username already exists in the database
#             existing_entry = FormData.objects.filter(username=username).first()

#             if existing_entry:
#                 # If the username exists, update the other fields
#                 existing_entry.email = email
#                 existing_entry.hyperlink = hyperlink
#                 existing_entry.text_area = text_area
#                 existing_entry.save()
#             else:
#                 # If the username does not exist, create a new entry
#                 new_entry = FormData(username=username, email=email, hyperlink=hyperlink, text_area=text_area)
#                 new_entry.save()

#             return redirect('form')  # Redirect back to the form page or a different URL as needed

#     else:
#         form = FormDataForm()

#     return render(request, 'accounts/form_template.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from .forms import FormDataForm
from .models import FormData

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