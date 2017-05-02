var React = require('react')
var django = require('django')

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
      <div>
        <label
          htmlFor={'id_choices-' + this.props.key + '-name'}>
          {django.gettext('Choice:')}
        </label>
        <input
          className="form-control"
          id={'id_choices-' + this.props.key + '-name'}
          name={'choices-' + this.props.key + '-name'}
          type="text"
          defaultValue={this.props.choice.label}
          onChange={this.handleLabelChange} />
        <div className="button-group">
          <button
            className="button"
            onClick={this.handleDelete}
            type="button">
            <i className="fa fa-trash" />
          </button>
        </div>
        {this.props.errors && this.props.errors.label
          ? <ul className="errorlist">
            {this.props.errors.label.map(function (msg, index) {
              return <li key={msg}>{msg}</li>
            })}
          </ul>
          : null}
      </div>
    )
  }
})

module.exports = ChoiceForm
