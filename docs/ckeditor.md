# General

for general info see [ckeditor](https://github.com/liqd/adhocracy4/blob/main/docs/ckeditor.md) in
adhocracy4.

# Local Testing

To test mb with a local version of django-ckeditor-5 you need to follow these
steps:

```
# clone django-ckeditor-5
git clone git@github.com:liqd/django-ckeditor-5.git
# cd into the directory
cd django-ckeditor-5/django-ckeditor-5
# install npm dependencies
npm install
# build js files
npm run dev
```

Now in mb, do the folowing:

```
# activate the venv
source venv/bin/activate
# install the local django-ckeditor-5
# replace ../django-ckeditor-5 with the correct path if its not in the parent
# directory
pip install -e ../django-ckeditor-5
```
