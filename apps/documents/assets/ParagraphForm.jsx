var React = require('react')
var django = require('django')
var ErrorList = require('../../contrib/static/js/ErrorList')

const ckGet = function (id) {
  return window.CKEDITOR.instances[id]
}

const ckReplace = function (id, config) {
  return window.CKEDITOR.replace(id, config)
}

const Paragraph = React.createClass({

  handleNameChange: function (e) {
    const name = e.target.value
    this.props.onNameChange(name)
  },

  handleTextChange: function (text) {
    this.props.onTextChange(text)
  },

  ckId: function () {
    return 'id_paragraphs-' + this.props.id + '-text'
  },

  ckEditorDestroy: function () {
    const editor = ckGet(this.ckId())
    if (editor) {
      editor.destroy()
    }
  },

  ckEditorCreate: function () {
    if (!ckGet(this.ckId())) {
      var editor = ckReplace(this.ckId(), this.props.config)
      editor.on('change', function (e) {
        var text = e.editor.getData()
        this.handleTextChange(text)
      }.bind(this))
      editor.setData(this.props.paragraph.text)
    }
  },

  componentWillUpdate: function (nextProps) {
    if (nextProps.index > this.props.index) {
      this.ckEditorDestroy() // why is this needed?
    }
  },

  componentDidUpdate: function (prevProps) {
    if (this.props.index > prevProps.index) {
      this.ckEditorCreate() // why is this needed?
    }
  },

  componentDidMount: function () {
    this.ckEditorCreate()
  },

  componentWillUnmount: function () {
    this.ckEditorDestroy()
  },

  render: function () {
    var ckEditorToolbarsHeight = 60  // measured on example editor
    return (
      <section>
        <button
          className="button button--full"
          onClick={this.props.onParagraphAddBefore}
          type="button">
          <i className="fa fa-plus" /> {django.gettext('Add a new paragraph')}
        </button>

        <div className="commenting">
          <div className="commenting__content">
            <div className="form-group">
              <label
                htmlFor={'id_paragraphs-' + this.props.id + '-name'}>
                {django.gettext('Headline')}
              </label>
              <input
                className="form-control"
                id={'id_paragraphs-' + this.props.id + '-name'}
                name={'paragraphs-' + this.props.id + '-name'}
                type="text"
                value={this.props.paragraph.name}
                onChange={this.handleNameChange} />
              <ErrorList errors={this.props.errors.name} />
            </div>

            <div className="form-group">
              <label
                htmlFor={'id_paragraphs-' + this.props.id + '-text'}>
                {django.gettext('Paragraph')}
              </label>
              <div
                className="django-ckeditor-widget"
                data-field-id={'id_paragraphs-' + this.props.id + '-text'}
                style={{display: 'inline-block'}}>
                <textarea
                  // fix height to avoid jumping on ckeditor initalization
                  style={{height: this.props.config.height + ckEditorToolbarsHeight}}
                  id={'id_paragraphs-' + this.props.id + '-text'} />
              </div>
              <ErrorList errors={this.props.errors.text} />
            </div>
          </div>

          <div className="commenting__actions button-group">
            <button
              className="button"
              onClick={this.props.onMoveUp}
              disabled={!this.props.onMoveUp}
              title={django.gettext('Move up')}
              type="button">
              <i className="fa fa-chevron-up"
                aria-label={django.gettext('Move up')} />
            </button>
            <button
              className="button"
              onClick={this.props.onMoveDown}
              disabled={!this.props.onMoveDown}
              title={django.gettext('Move down')}
              type="button">
              <i className="fa fa-chevron-down"
                aria-label={django.gettext('Move down')} />
            </button>
            <button
              className="button"
              onClick={this.props.onDelete}
              title={django.gettext('Delete')}
              type="button">
              <i className="fa fa-trash"
                aria-label={django.gettext('Delete')} />
            </button>
          </div>
        </div>
      </section>
    )
  }
})

module.exports = Paragraph
