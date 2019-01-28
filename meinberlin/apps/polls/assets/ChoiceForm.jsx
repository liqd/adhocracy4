var React = require('react')
var django = require('django')
var ErrorList = require('../../contrib/assets/ErrorList')

const ChoiceForm = (props) => {
  return (
    <div className="form-group form-group--narrow">
      <div className="input-group">
        <label htmlFor={'id_choices-' + props.id + '-name'}>
          <span className="sr-only">{props.label}</span>
          <input
            id={'id_choices-' + props.id + '-name'}
            name={'choices-' + props.id + '-name'}
            type="text"
            className="input-group__input"
            value={props.choice.label}
            onChange={(e) => { props.onLabelChange(e.target.value) }} />
        </label>
        <button
          className="input-group__after input-group__after-outside btn btn--light"
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
