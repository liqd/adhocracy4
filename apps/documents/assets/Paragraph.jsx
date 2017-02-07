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
    this.ckEditorDestroy()
  },
  componentDidUpdate: function (prevProps) {
    this.ckEditorCreate()
  },
  componentDidMount: function () {
    this.ckEditorCreate()
  },
  componentWillUnmount: function () {
    this.ckEditorCreate()
  },
  render: function () {
    return (
      <div>
        <button
          className="button"
          onClick={this.add}
          type="button">
          <i className="fa fa-plus" /> {django.gettext('add a new paragraph')}
        </button>

        <div className="commenting-paragraph">
          <label
            htmlFor={'id_paragraphs-' + this.props.id + '-name'}>
            {django.gettext('Headline:')}
          </label>
          <input
            className="form-control"
            id={'id_paragraphs-' + this.props.id + '-name'}
            name={'paragraphs-' + this.props.id + '-name'}
            type="text"
            defaultValue={this.props.paragraph.name}
            onChange={this.handleNameChange} />
          {this.props.errors && this.props.errors.name ? <ul className="errorlist">
            <li>{this.props.errors.name[0]}</li>
          </ul> : null}

          <label
            htmlFor={'id_paragraphs-' + this.props.id + '-text'}>
            {django.gettext('Paragraph:')}
          </label>
          <div
            className="django-ckeditor-widget"
            data-field-id={'id_paragraphs-' + this.props.id + '-text'}
            style={{display: 'inline-block'}}>
            <textarea
              id={'id_paragraphs-' + this.props.id + '-text'} />
            { this.props.errors && this.props.errors.text ? <ul className="errorlist">
              <li>{this.props.errors.text[0]}</li>
            </ul> : null }
          </div>

          <div className="action-bar">
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
      </div>
    )
  }
})

module.exports = Paragraph
