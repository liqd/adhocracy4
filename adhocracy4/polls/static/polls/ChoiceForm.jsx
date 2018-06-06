var React = require('react')
var django = require('django')
var ErrorList = require('../../../static/ErrorList')

const ChoiceForm = (props) => {
  return (
    <div className="form-group form-group--narrow">
      <label
        className="sr-only"
        htmlFor={'id_choices-' + props.id + '-name'}>
        {props.label}
      </label>
      <div className="input-group">
        <input
          id={'id_choices-' + props.id + '-name'}
          name={'choices-' + props.id + '-name'}
          type="text"
          className="input-group__input"
          value={props.choice.label}
          onChange={(e) => { props.onLabelChange(e.target.value) }} />
        <button
          className="input-group__after btn btn--light"
          onClick={props.onDelete}
          title={django.gettext('remove')}
          type="button">
          <i className="fa fa-times"
            aria-label={django.gettext('remove')} />
        </button>
      </div>
      <ErrorList errors={props.errors} field="label" />
    </div>
  )
}

module.exports = ChoiceForm
