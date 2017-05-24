var React = require('react')
var django = require('django')

var ckGet = function (id) {
  return window.CKEDITOR.instances[id]
}

var ckReplace = function (id, config) {
  return window.CKEDITOR.replace(id, config)
}

var Paragraph = React.createClass({
  add: function () {
    this.props.addParagraphBeforeIndex(this.props.index)
  },
  delete: function () {
    this.props.deleteParagraph(this.props.index)
  },
  up: function () {
    this.props.moveParagraphUp(this.props.index)
  },
  down: function () {
    this.props.moveParagraphDown(this.props.index)
  },
  handleNameChange: function (e) {
    var index = this.props.index
    var text = e.target.value
    this.props.updateParagraphName(index, text)
  },
  ckEditorDestroy: function () {
    var id = 'id_paragraphs-' + this.props.id + '-text'
    var editor = ckGet(id)
    if (editor) {
      editor.destroy()
    }
  },
  ckEditorCreate: function () {
    var id = 'id_paragraphs-' + this.props.id + '-text'
    if (!ckGet(id)) {
      var editor = ckReplace(id, this.props.config)
      editor.on('change', function (e) {
        var text = e.editor.getData()
        var index = this.props.index
        this.props.updateParagraphText(index, text)
      }.bind(this))
      editor.setData(this.props.paragraph.text)
    }
  },
  componentWillUpdate: function (nextProps) {
    if (nextProps.index > this.props.index) {
      this.ckEditorDestroy()
    }
  },
  componentDidUpdate: function (prevProps) {
    if (this.props.index > prevProps.index) {
      this.ckEditorCreate()
    }
  },
  componentDidMount: function () {
    this.ckEditorCreate()
  },
  componentWillUnmount: function () {
    this.ckEditorCreate()
  },
  render: function () {
    var ckEditorToolbarsHeight = 60  // measured on example editor
    return (
      <section>
        <button
          className="button button--full"
          onClick={this.add}
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
                defaultValue={this.props.paragraph.name}
                onChange={this.handleNameChange} />
              {this.props.errors && this.props.errors.name ? <ul className="errorlist">
                {this.props.errors.name.map(function (msg, index) {
                  return <li key={msg}>{msg}</li>
                })}
              </ul> : null}
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
              {this.props.errors && this.props.errors.text ? <ul className="errorlist">
                {this.props.errors.text.map(function (msg, index) {
                  return <li key={msg}>{msg}</li>
                })}
              </ul> : null}
            </div>
          </div>

          <div className="commenting__actions button-group">
            <button
              className="button"
              onClick={this.up}
              disabled={!this.props.moveParagraphUp}
              type="button">
              <i className="fa fa-chevron-up" />
            </button>
            <button
              className="button"
              onClick={this.down}
              disabled={!this.props.moveParagraphDown}
              type="button">
              <i className="fa fa-chevron-down" />
            </button>
            <button
              className="button"
              onClick={this.delete}
              type="button">
              <i className="fa fa-trash" />
            </button>
          </div>
        </div>
      </section>
    )
  }
})

module.exports = Paragraph
