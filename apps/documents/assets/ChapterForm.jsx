var React = require('react')
var django = require('django')
var ErrorList = require('../../contrib/static/js/ErrorList')
var ParagraphForm = require('./ParagraphForm')

const ChapterForm = React.createClass({

  handleChapterNameChange: function (e) {
    var name = e.target.value
    this.props.onChapterNameChange(name)
  },

  render: function () {
    return (
      <section className="commenting-form">
        <div className="commenting">
          <div className="form-group commenting__content">
            <label>
              {django.gettext('Chapter title')}
              <input
                type="text"
                value={this.props.chapter.name}
                onChange={this.handleChapterNameChange} />
            </label>
            <ErrorList errors={{}} />
          </div>
        </div>

        {
          this.props.chapter.paragraphs.map(function (paragraph, index, arr) {
            return (
              <ParagraphForm
                id={paragraph.id || paragraph.key}
                key={paragraph.id || paragraph.key}
                index={index} // why is this needed for ck?
                paragraph={paragraph}
                errors={{}}
                config={this.props.config}
                onDelete={() => { this.props.onParagraphDelete(index) }}
                onMoveUp={index !== 0 ? () => { this.props.onParagraphMoveUp(index) } : null}
                onMoveDown={index < arr.length - 1 ? () => { this.props.onParagraphMoveDown(index) } : null}
                onParagraphAddBefore={() => { this.props.onParagraphAddBefore(index) }}
                onNameChange={(name) => { this.props.onParagraphNameChange(index, name) }}
                onTextChange={(text) => { this.props.onParagraphTextChange(index, text) }}
              />
            )
          }.bind(this))
        }

        <button
          className="button button--light button--small"
          onClick={this.props.onParagraphAppend}
          type="button">
          <i className="fa fa-plus" /> {django.gettext('Add a new paragraph')}
        </button>
      </section>
    )
  }
})

module.exports = ChapterForm
