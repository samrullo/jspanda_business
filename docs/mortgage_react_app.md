# How to deploy react build into Flask app
I wanted to serve react app from Flask blueprint. For that I created blueprint with below argument values

```python
mortgage_app_bp = Blueprint("mortgage_app_bp",__name__,url_prefix="/mortgage",template_folder=str(current_app.config["REACT_MORTGAGE_APP_FOLDER"]),static_folder=str(current_app.config["REACT_MORTGAGE_APP_FOLDER"]/"static"))
```

**REACT_MORTGAGE_APP_FOLDER** app config points to absolute path of **react-mortgage-app**

Next I created *react-mortgage-app* directory right under the *project* folder.

Then I copied contents of *<react-app>/build* into *react-mortgage-app*

Next, I moved files that are in the same folder as react app's **index.html** (files such as **manifest.json**) into a new directory
under **static**. I called the new directory **react_index_files**

Next, I edited react app's *index.html* to have correct reference links to *manifest.json*.

Also I placed */mortgage* before */static*, whereever it appears in react app's *index.html*.

The reason to use url_prefix for this blueprint was to separate its static folder path from the Flask app's static folder path.
Without this url_prefix, Flask keeps on attempting to search for static files in the Flask app's static directory which is located under *application* folder.

Finally, we serve react app's *index.html* (which I renamed to mortgage_index.html)

```python
@mortgage_app_bp.route("/")
def mortgage_app():    
    return render_template("mortgage_index.html")
```


