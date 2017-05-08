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
          htmlFor={'id_choices-' + this.props.key + '-name'}>
          {django.gettext('Choice:')}
        </label>
        <input
          id={'id_choices-' + this.props.key + '-name'}
          name={'choices-' + this.props.key + '-name'}
          type="text"
          defaultValue={this.props.choice.label}
          onChange={this.handleLabelChange} />
        <div className="button-group">
          <button
            className="button button--light"
            onClick={this.handleDelete}
            type="button">
            <i className="fa fa-trash" />
          </button>
        </div>
        <ErrorList errors={this.props.errors} />
      </div>
    )
  }
})

module.exports = ChoiceForm
