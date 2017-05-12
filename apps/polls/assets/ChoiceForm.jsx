var React = require('react')
var django = require('django')
var ErrorList = require('../../contrib/static/js/ErrorList')

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
      <div className="form-group input-action input-action--center input-action--spaced">
        <label
          className="sr-only"
          htmlFor={'id_choices-' + this.props.index + '-name'}>
          {django.gettext('Choice') + ` #${this.props.index}:`}
        </label>
        <input
          id={'id_choices-' + this.props.index + '-name'}
          name={'choices-' + this.props.index + '-name'}
          type="text"
          className="input-action__input"
          defaultValue={this.props.choice.label}
          onChange={this.handleLabelChange} />
        <button
          className="input-action__action"
          onClick={this.handleDelete}
          ariaLabel={django.gettext('remove')}
          type="button">
          <i className="fa fa-times" />
        </button>
        <ErrorList errors={this.props.errors} />
      </div>
    )
  }
})

module.exports = ChoiceForm
