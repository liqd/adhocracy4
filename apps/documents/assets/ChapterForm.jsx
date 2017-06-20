var React = require('react')
var django = require('django')
var ErrorList = require('../../contrib/static/js/ErrorList')
var ParagraphForm = require('./ParagraphForm')

function handleChapterNameChange (props, e) {
  var name = e.target.value
  props.onChapterNameChange(name)
}

const ChapterForm = (props) => {
  return (
    <section className="commenting-form">
      <div className="commenting">
        <div className="form-group commenting__content">
          <label>
            {django.gettext('Chapter title')}
            <input
              type="text"
              value={props.chapter.name}
              onChange={(e) => handleChapterNameChange(props, e)} />
          </label>
          <ErrorList errors={props.errors} field="name" />
        </div>
      </div>

      {
        props.chapter.paragraphs.map(function (paragraph, index, arr) {
          return (
            <ParagraphForm
              id={paragraph.id || paragraph.key}
              key={paragraph.id || paragraph.key}
              index={index}
              paragraph={paragraph}
              config={props.config}
              onDelete={() => { props.onParagraphDelete(index) }}
              onMoveUp={index !== 0 ? () => { props.onParagraphMoveUp(index) } : null}
              onMoveDown={index < arr.length - 1 ? () => { props.onParagraphMoveDown(index) } : null}
              onParagraphAddBefore={() => { props.onParagraphAddBefore(index) }}
              onNameChange={(name) => { props.onParagraphNameChange(index, name) }}
              onTextChange={(text) => { props.onParagraphTextChange(index, text) }}
              errors={props.errors && props.errors.paragraphs ? props.errors.paragraphs[index] : {}}
            />
          )
        })
      }

      <button
        className="button button--light button--small"
        onClick={props.onParagraphAppend}
        type="button">
        <i className="fa fa-plus" /> {django.gettext('Add a new paragraph')}
      </button>
    </section>
  )
}

module.exports = ChapterForm
