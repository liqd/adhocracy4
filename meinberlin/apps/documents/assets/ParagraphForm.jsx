var React = require('react')
var django = require('django')
var ErrorList = require('../../contrib/assets/ErrorList')

const ckGet = function (id) {
  return window.CKEDITOR.instances[id]
}

const ckReplace = function (id, config) {
  return window.CKEDITOR.replace(id, config)
}

class Paragraph extends React.Component {
  handleNameChange (e) {
    const name = e.target.value
    this.props.onNameChange(name)
  }

  ckId () {
    return 'id_paragraphs-' + this.props.id + '-text'
  }

  ckEditorDestroy () {
    const editor = ckGet(this.ckId())
    if (editor) {
      editor.destroy()
    }
  }

  ckEditorCreate () {
    if (!ckGet(this.ckId())) {
      var editor = ckReplace(this.ckId(), this.props.config)
      editor.on('change', function (e) {
        var text = e.editor.getData()
        this.props.onTextChange(text)
      }.bind(this))
      editor.setData(this.props.paragraph.text)
    }
  }

  componentWillUpdate (nextProps) {
    if (nextProps.index > this.props.index) {
      this.ckEditorDestroy()
    }
  }

  componentDidUpdate (prevProps) {
    if (this.props.index > prevProps.index) {
      this.ckEditorCreate()
    }
  }

  componentDidMount () {
    this.ckEditorCreate()
  }

  componentWillUnmount () {
    this.ckEditorDestroy()
  }

  render () {
    var ckEditorToolbarsHeight = 60 // measured on example editor
    return (
      <section>
        <div className="commenting">
          <div className="commenting__content commenting__content--border">
            <div className="form-group">
              <label
                htmlFor={'id_paragraphs-' + this.props.id + '-name'}>
                {django.gettext('Headline')}
                <input
                  className="form-control"
                  id={'id_paragraphs-' + this.props.id + '-name'}
                  name={'paragraphs-' + this.props.id + '-name'}
                  type="text"
                  value={this.props.paragraph.name}
                  onChange={this.handleNameChange.bind(this)} />
              </label>
              <ErrorList errors={this.props.errors} field="name" />
            </div>

            <div className="form-group">
              <label
                htmlFor={'id_paragraphs-' + this.props.id + '-text'}>
                {django.gettext('Paragraph')}
                <div
                  className="django-ckeditor-widget"
                  data-field-id={'id_paragraphs-' + this.props.id + '-text'}
                  style={{ display: 'inline-block' }}>
                  <textarea
                    // fix height to avoid jumping on ckeditor initalization
                    style={{ height: this.props.config.height + ckEditorToolbarsHeight }}
                    id={'id_paragraphs-' + this.props.id + '-text'} />
                </div>
              </label>
              <ErrorList errors={this.props.errors} field="text" />
            </div>
          </div>

          <div className="commenting__actions btn-group" role="group">
            <button
              className="btn btn--light btn--small"
              onClick={this.props.onMoveUp}
              disabled={!this.props.onMoveUp}
              title={django.gettext('Move up')}
              type="button">
              <i className="fa fa-chevron-up"
                aria-label={django.gettext('Move up')} />
            </button>
            <button
              className="btn btn--light btn--small"
              onClick={this.props.onMoveDown}
              disabled={!this.props.onMoveDown}
              title={django.gettext('Move down')}
              type="button">
              <i className="fa fa-chevron-down"
                aria-label={django.gettext('Move down')} />
            </button>
            <button
              className="btn btn--light btn--small"
              onClick={this.props.onDelete}
              title={django.gettext('Delete')}
              type="button">
              <i className="fas fa-trash-alt"
                aria-label={django.gettext('Delete')} />
            </button>
          </div>
        </div>
      </section>
    )
  }
}

module.exports = Paragraph
