import React, { useRef, useEffect } from 'react'
import django from 'django'
import FormFieldError from 'adhocracy4/adhocracy4/static/FormFieldError'

// translations
const translations = {
  headline: django.gettext('Headline'),
  paragraph: django.gettext('Paragraph'),
  moveUp: django.gettext('Move up'),
  moveDown: django.gettext('Move down'),
  delete: django.gettext('Delete'),
  helpText: django.gettext(
    'If you add an image, please provide an ' +
      'alternate text. It serves as a textual description of the image ' +
      'content and is read out by screen readers. Describe the image in ' +
      'approx. 80 characters. Example: A busy square with people in summer.'
  )
}

const ParagraphForm = (props) => {
  const editor = useRef(null)
  const index = useRef(props.index)
  const id = 'id_paragraphs-' + props.id + '-text'

  useEffect(() => {
    // destroy if component renders multiple times to prevent
    // multiple CKEditors
    let destroy = false
    const createEditor = async () => {
      const config = props.config
      window.ckeditorSetSpecialConfigValues(
        config,
        props.csrfCookieName,
        props.uploadUrl,
        props.uploadFileTypes
      )
      const ckeditor = await window.ClassicEditor.create(
        document.querySelector('#' + id),
        config
      )
      if (destroy) {
        ckeditor.destroy()
      } else {
        editor.current = ckeditor
        editor.current.model.document.on('change:data', (e) => {
          const text = editor.current.getData()
          props.onTextChange(text)
        })
        editor.current.setData(props.paragraph.text)
      }
    }
    if (editor.current) {
      if (index.current !== props.index) {
        // recreate if index changed
        destroyEditor()
      }
    }
    index.current = props.index
    if (!editor.current) {
      createEditor()
      return () => {
        // destroy if still in process of creating
        destroy = true
        // destroy if already created
        destroyEditor()
      }
    }
  }, [props.index])

  const destroyEditor = () => {
    if (editor.current) {
      editor.current.destroy()
      editor.current = null
    }
  }
  const handleNameChange = (e) => {
    const name = e.target.value
    props.onNameChange(name)
  }

  return (
    <section>
      <div className="row">
        <div className="col-lg-9">
          <div className="commenting__content--border">
            <div className="form-group">
              <label htmlFor={'id_paragraphs-' + props.id + '-name'}>
                {translations.headline}
                <input
                  className="form-control"
                  id={'id_paragraphs-' + props.id + '-name'}
                  name={'paragraphs-' + props.id + '-name'}
                  type="text"
                  value={props.paragraph.name}
                  onChange={handleNameChange}
                  aria-invalid={props.errors ? 'true' : 'false'}
                  aria-describedby={props.errors && 'id_error-' + props.id}
                />
                <FormFieldError
                  id={'id_error-' + props.id}
                  error={props.errors}
                  field="name"
                />
              </label>
            </div>

            <div className="form-group">
              <label htmlFor={'id_paragraphs-' + props.id + '-text'}>
                {translations.paragraph}
                <div
                  id={'id_paragraph-help-text-' + props.id}
                  className="form-hint"
                >
                  {translations.helpText}
                </div>
                <div
                  className="django-ckeditor-widget"
                  data-field-id={'id_paragraphs-' + props.id + '-text'}
                  style={{ display: 'inline-block' }}
                >
                  <textarea
                    id={'id_paragraphs-' + props.id + '-text'}
                    aria-invalid={props.errors ? 'true' : 'false'}
                    aria-describedby={
                      (props.errors ? 'id_paragraph-help-text-' : 'id_error-') +
                      props.id
                    }
                  />
                </div>
                <FormFieldError
                  id={'id_error-' + props.id}
                  error={props.errors}
                  field="text"
                />
              </label>
            </div>
          </div>
        </div>

        <div className="commenting__actions btn-group" role="group">
          <button
            className="btn btn--light btn--small"
            onClick={props.onMoveUp}
            disabled={!props.onMoveUp}
            title={translations.moveUp}
            type="button"
          >
            <i className="fa fa-chevron-up" aria-label={translations.moveUp} />
          </button>
          <button
            className="btn btn--light btn--small"
            onClick={props.onMoveDown}
            disabled={!props.onMoveDown}
            title={translations.moveDown}
            type="button"
          >
            <i
              className="fa fa-chevron-down"
              aria-label={translations.moveDown}
            />
          </button>
          <button
            className="btn btn--light btn--small"
            onClick={props.onDelete}
            title={translations.delete}
            type="button"
          >
            <i className="fas fa-trash-alt" aria-label={translations.delete} />
          </button>
        </div>
      </div>
    </section>
  )
}

module.exports = ParagraphForm
