import django from 'django'
import React from 'react'
import { updateItem } from './helpers.js'

export default class QuestionForm extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      question: '',
      selectedCategory: ''
    }
  }

  selectCategory (e) {
    this.setState({ selectedCategory: e.target.value })
  }

  handleTextChange (e) {
    this.setState({ question: e.target.value })
  }

  getPrivacyPolicyLabel () {
    const termsOfUseUrl = '/terms-of-use'
    const privacyPolicyUrl = '/datenschutz'
    const labelPart1 = 'I hereby expressly consent to the collection and processing (storage) of my data and expressly consent to the processing and publication of my ideas, comments and contributions as described in the privacy policy. I also confirm that I have read and accept the '
    const labelPart2 = ' and the '
    return (
      <span>
        {labelPart1}
        <a href={termsOfUseUrl} target="_blank">terms of use</a>
        {labelPart2}
        <a href={privacyPolicyUrl} target="_blank">privacy policy</a>.
      </span>
    )
  }

  addQuestion (e) {
    e.preventDefault()
    const url = this.props.questions_api_url
    const data = {
      text: this.state.question,
      category: this.state.selectedCategory
    }
    updateItem(data, url, 'POST')
    this.setState({ question: '' })
  }

  render () {
    return (
      <div className="container">
        <form action="" onSubmit={this.addQuestion.bind(this)}>
          <h2>{django.gettext('Here you can ask your question')}</h2>
          {Object.keys(this.props.category_dict).length > 0 &&
            <div className="control-bar">
              <label for="categorySelect">{django.gettext('Characteristic')}*</label>
              <div className="dropdown">
                <select
                  name="categorySelect"
                  id="categorySelect"
                  className="btn btn--light btn--select live_questions__filters--dropdown dropdown-toggle"
                  onChange={this.selectCategory.bind(this)}
                  required="required"
                >
                  <option className="dropdown-item" value="">---------</option>
                  {Object.keys(this.props.category_dict).map((categoryPk, index) => {
                    return <option className="dropdown-item" key={index} value={categoryPk}>{this.props.category_dict[categoryPk]}</option>
                  })}
                </select>
              </div>
            </div>}
          <label for="questionTextField">{django.gettext('Question')}*</label>
          <textarea
            placeholder={django.gettext('Add Question')}
            id="questionTextField"
            className="form-control"
            name="questionTextFieldName"
            rows="3"
            onChange={this.handleTextChange.bind(this)}
            required="required"
            value={this.state.question}
          />

          <div class="form-check">
            <label class="form-check__label">
              <input type="checkbox" name="data_protection" id="data_protection_check" required="required" />
              {this.getPrivacyPolicyLabel()}
            </label>
          </div>
          <input type="submit" value={django.gettext('Add Question')} className="submit-button" />
        </form>
      </div>
    )
  }
}
