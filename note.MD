## django-admin startproject projectname 
## python manage.py runserver 
## Start a new app 
## python manage.py startapp appname
## jquery 3.5.1.js
## Django Load to the VirtualEnv Dir cannot read the template 
https://stackoverflow.com/questions/50294869/django-looks-for-templates-in-my-envs-folder-django-admin

Django was looking for templates in my venv dir (my virtual environment dir) too, in my case, I solved it after I added my app in the settings file of the main project dir.

Basically in your app dir, there's an apps.py file which has a class named *YOURAPPNAME*Config. In my case, the app is accounts so the class is AccountsConfig. Then go into your main project dir, which is located in same directory as your manage.py file, open settings.py, scroll down to INSTALLED_APPS and add your class there. For me it would be accounts.apps.AccountsConfig
 <link rel="stylesheet" href="{% static 'select2/css/bootstrap.min.css' %}"> 
  <link rel="stylesheet" href="{% static 'select2/css/select2.min.css' %}"> 
  <link rel="stylesheet" href="{% static 'select2/css/select2-bootstrap-5-theme.min.css' %}"> 
  <script src="{% static 'select2/js/jquery.slim.min.js' %}"></script>
  <script src="{% static 'select2/js/bootstrap.bundle.min.js' %}"></script>
  <script src="{% static 'select2/js/select2.full.min.js' %}"></script>
  <select class="form-select" id="productID" data-placeholder="Choose one thing">
      {% for process_id in unique_process_list %}
          <option value="{{ process_id }}">{{process_id}}</option>
      {% endfor %}
  </select>

        $( '#productID' ).select2( {
            theme: "bootstrap-5",
            tags: true,
            width: $( this ).data( 'width' ) ? $( this ).data( 'width' ) : $( this ).hasClass( 'w-100' ) ? '100%' : 'style',
            placeholder: $( this ).data( 'placeholder' ),
          } );
        
        $('#productID').on("select2:selecting", function(e) { 
            // what you would like to happen
            console.log("test");
          });
