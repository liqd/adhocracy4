var React = require('react')
var django = require('django')
var ErrorList = require('../../contrib/assets/ErrorList')

let ChoiceForm = React.createClass({
  handleLabelChange: function (e) {
    var index = this.props.index
    var label = e.target.value
    this.props.updateChoiceLabel(index, label)
  },

  handleDelete: function () {
    this.props.deleteChoice(this.props.index)
  },

  render: function () {
    return (
      <div className="form-group form-group--narrow">
        <label
          className="sr-only"
          htmlFor={'id_choices-' + this.props.index + '-name'}>
          {django.gettext('Choice') + ` #${this.props.index}`}
        </label>
        <div className="button-group input-addon">
          <input
            id={'id_choices-' + this.props.index + '-name'}
            name={'choices-' + this.props.index + '-name'}
            type="text"
            className="input-addon__input"
            value={this.props.choice.label}
            onChange={this.handleLabelChange} />
          <button
            className="input-addon__after button button--light"
            onClick={this.handleDelete}
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
})

module.exports = ChoiceForm
