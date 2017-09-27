var React = require('react')
var django = require('django')
var ErrorList = require('../../contrib/assets/ErrorList')

class ChoiceForm extends React.Component {
  handleLabelChange (e) {
    var index = this.props.index
    var label = e.target.value
    this.props.updateChoiceLabel(index, label)
  }

  handleDelete () {
    this.props.deleteChoice(this.props.index)
  }

  render () {
    return (
      <div className="form-group form-group--narrow">
        <label
          className="sr-only"
          htmlFor={'id_choices-' + this.props.id + '-name'}>
          {django.gettext('Choice') + ` #${this.props.index + 1}`}
        </label>
        <div className="input-group">
          <input
            id={'id_choices-' + this.props.id + '-name'}
            name={'choices-' + this.props.id + '-name'}
            type="text"
            className="input-group__input"
            value={this.props.choice.label}
            onChange={this.handleLabelChange.bind(this)} />
          <button
            className="input-group__after btn btn--light"
            onClick={this.handleDelete.bind(this)}
            title={django.gettext('remove')}
            type="button">
            <i className="fa fa-times"
              aria-label={django.gettext('remove')} />
          </button>
        </div>
        <ErrorList errors={this.props.errors} field="label" />
      </div>
    )
  }
}

module.exports = ChoiceForm
