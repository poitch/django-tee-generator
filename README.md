# django-tee-generator

django-tee-generator is a Django Application that generates an image of a tshirt based on provided parameters.

## Install

Add `tee` to the list of installed application in `settings.py`.
```
INSTALLED_APPS = [
    ...
    'tee',
    ...
]
```

Then make sure to include the URLs in your project `urls.py`

```
urlpatterns = [
    ...
    path('tee/', include('tee.urls')),
    ...
]
```

*Note: The application does not come with the required TrueType fonts so you will need to drop them into the `assets` directory.*

Copy `Avenir Next.ttc` and `Helvetica.ttc` in `tee/assets`

## Usage

Browse to your application with the following URL:

`/tee/create/{shape}/{color}/{text color}/{lines}/{filename}.png`

The shape can either be `crew` or `v` to generate a crew t-shirt of a v-neck t-shirt.

`color` and `text color` must be HEX colors with 6 characters.

`lines` will be the text that will be _printed_ on the t-shirt. Each line needs to be separated by a `/`.

`filename` can be arbitrary but will be the name contained in the HTTP response for the file.

*Example:*

`http://localhost:8000/tee/create/crew/40E0D0/207068/Helvetica/Soba&/Udon&/Somen&/Ramen./noodles.png`

This will generate the following:


![Noodles](images/noodles.png)