const React = require('react')
const FlipMove = require('react-flip-move').default
const django = require('django')
const FormFieldError = require('adhocracy4/adhocracy4/static/FormFieldError')
const ParagraphForm = require('./ParagraphForm')

const translated = {
  title: django.gettext('Chapter title'),
  addParagraph: django.gettext('Add a new paragraph')
}

const ChapterForm = (props) => {
  return (
    <section className="u-spacer-bottom-double">
      <div className="row">
        <div className="form-group commenting__content">
          <label htmlFor={'id_chapters-' + props.id + '-name'}>
            {translated.title}
            <input
              id={'id_chapters-' + props.id + '-name'}
              name={'chapters-' + props.id + '-name'}
              type="text"
              value={props.chapter.name}
              onChange={(e) => { props.onChapterNameChange(e.target.value) }}
              aria-invalid={props.errors ? 'true' : 'false'}
              aria-describedby={props.errors && 'id_error-' + props.id}
            />
            <FormFieldError id={'id_error-' + props.id} error={props.errors} field="name" />
          </label>
        </div>
      </div>

      <FlipMove easing="cubic-bezier(0.25, 0.5, 0.75, 1)">
        {
          props.chapter.paragraphs.map(function (paragraph, index, arr) {
            const key = paragraph.id || paragraph.key
            return (
              <div key={key}>
                <ParagraphForm
                  id={key}
                  key={key}
                  index={index}
                  paragraph={paragraph}
                  csrfCookieName={props.csrfCookieName}
                  uploadUrl={props.uploadUrl}
                  uploadFileTypes={props.uploadFileTypes}
                  config={props.config}
                  onDelete={() => { props.onParagraphDelete(index) }}
                  onMoveUp={index !== 0 ? () => { props.onParagraphMoveUp(index) } : null}
                  onMoveDown={index < arr.length - 1 ? () => { props.onParagraphMoveDown(index) } : null}
                  onParagraphAddBefore={() => { props.onParagraphAddBefore(index) }}
                  onNameChange={(name) => { props.onParagraphNameChange(index, name) }}
                  onTextChange={(text) => { props.onParagraphTextChange(index, text) }}
                  errors={props.errors && props.errors.paragraphs ? props.errors.paragraphs[index] : {}}
                />
              </div>
            )
          })
        }
      </FlipMove>

      <button
        className="u-spacer-top btn btn--light btn--small"
        onClick={props.onParagraphAppend}
        type="button"
      >
        <i className="fa fa-plus" /> {translated.addParagraph}
      </button>
    </section>
  )
}

module.exports = ChapterForm
