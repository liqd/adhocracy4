import django from 'django'
import React from 'react'
import $ from 'jquery' // FIXME needed to run test but file should be refactored to not include jquery

const affiliationStr = django.gettext('Affiliation')
const answeredQuestionsStr = django.gettext('Answered questions will be displayed in the statistics according to the chosen affiliation.')

export default class SelectCategory extends React.Component {
  componentDidMount () {
    const select = $('#categorySelect')
    select.on('change', this.props.onSelect)
  }

  render () {
    return (
      <div>
        {Object.keys(this.props.category_dict).length > 0 &&
          <div className="live_questions__select u-spacer-bottom">
            <label htmlFor="categorySelect">{affiliationStr}*</label>
            <div className="form-hint">
              {answeredQuestionsStr}
            </div>
            <select
              name="categorySelect"
              id="categorySelect"
              className="js-select2"
              required="required"
              data-minimum-results-for-search="Infinity"
            >
              <option value="">--------</option>
              {Object.keys(this.props.category_dict).map((categoryPk, index) => {
                return <option key={index} value={categoryPk}>{this.props.category_dict[categoryPk]}</option>
              })}
            </select>
          </div>}
      </div>
    )
  }
}
