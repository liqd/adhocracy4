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
      <div className="form-group">
        <label
          className="sr-only"
          htmlFor={'id_choices-' + this.props.index + '-name'}>
          {django.gettext('Choice') + ` #${this.props.index}`}
        </label>
        <div className="button-group input-action">
          <input
            id={'id_choices-' + this.props.index + '-name'}
            name={'choices-' + this.props.index + '-name'}
            type="text"
            className="input-action__input"
            defaultValue={this.props.choice.label}
            onChange={this.handleLabelChange} />
          <button
            className="input-action__action button button--light"
            onClick={this.handleDelete}
            aria-label={django.gettext('remove')}
            type="button">
            <i className="fa fa-times" />
          </button>
        </div>
        <ErrorList errors={this.props.errors} />
      </div>
    )
  }
})

module.exports = ChoiceForm
