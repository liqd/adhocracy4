# CKEditor 5 Integration

## Introduction

This documentation outlines the rationale behind the choice of CKEditor 5 as
the rich text editor for our Django projects.
The code lives in [django-ckeditor-5](https://github.com/liqd/django-ckeditor-5)
and was forked from [django-ckeditor-5 repository](https://github.com/hvlads/django-ckeditor-5).

## Why CKEditor 5?

- We already have experience with CKEditor4
- It's open source
- It's backed by a company and therefore well maintained

## Custom Plugins

1. **File Upload**: To meet our project's specific needs, we have implemented a custom file upload plugin for CKEditor 5. This plugin enables users to seamlessly upload and embed files directly within the editor, enhancing the overall content creation process. The source code for the file upload plugin is available at [liqd/ckeditor5-file-uploader](https://github.com/liqd/ckeditor5-file-uploader).

2. **Accordion**: The custom accordion (previously called collapsible) plugin adds the ability to create accordion-style content within the CKEditor 5 editor. The source code for the accordion plugin is available at [liqd/ckeditor5-accordion](https://github.com/liqd/ckeditor5-accordion).

## Integration Details

1. **Forked from django-ckeditor-5**: Our CKEditor 5 integration is based on a fork from [django-ckeditor-5](https://github.com/hvlads/django-ckeditor-5).

2. **Form Considerations**: When integrating CKEditor into forms, it's important to note that forms using CKEditor fields either need to mark the CKEditor form field as not required or add `novalidate` to the whole form as otherwise the browser blocks form submital.

## Switch from CKeditor4 to CKeditor5

We migrated from [django-ckeditor](https://github.com/django-ckeditor/django-ckeditor) which is based on CKEditor4. As CKEditor4 became EOL in June 2023 and django-ckeditor didn't have any immediate
plans to migrateo to CKEditor5 we deciced to start off with django-ckeditor-5
and customise it to our needs.
