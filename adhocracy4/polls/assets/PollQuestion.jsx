const React = require('react')
const django = require('django')
const update = require('immutability-helper')

export default class PollQuestion extends React.Component {
  constructor (props) {
    super(props)

    const question = this.props.question

    this.state = {
      question: question,
      questionHelpText: props.question.help_text,
      selectedChoices: question.userChoices,
      otherChoice: ''
    }
  }

  handleOnChange (event) {
    const choiceId = parseInt(event.target.value)
    this.setState({
      selectedChoices: [choiceId]
    })
  }

  handleTextChange (event) {
    this.setState({ otherChoice: event.target.value })
  }

  handleOnMultiChange (event) {
    const choiceId = parseInt(event.target.value)
    const index = this.state.selectedChoices.indexOf(choiceId)

    let diff = {}
    if (index === -1) {
      diff = { $push: [choiceId] }
    } else {
      diff = { $splice: [[index, 1]] }
    }

    this.setState({
      selectedChoices: update(this.state.selectedChoices, diff)
    })
  }

  getFormHelpText () {
    let formHelpText
    if (this.state.question.multiple_choice) {
      formHelpText = <div className="poll__help-text">{django.gettext('Multiple answers are possible.')}</div>
    }
    return (
      formHelpText
    )
  }

  render () {
    return (
      <form className="poll u-border">
        <h2>{this.state.question.label}</h2>
        <div className="poll__help-text">{this.state.questionHelpText}</div>
        {this.getFormHelpText()}
        <div className="poll__rows">
          {
            this.state.question.choices.map((choice, i) => {
              const checked = this.state.selectedChoices.indexOf(choice.id) !== -1

              if (!this.state.question.multiple_choice) {
                return (
                  <label className="poll-row radio" key={choice.id} htmlFor={'id_choice-' + choice.id + '-single'}>
                    <input
                      className="poll-row__radio radio__input"
                      type="radio"
                      name="question"
                      id={'id_choice-' + choice.id + '-single'}
                      value={choice.id}
                      checked={checked}
                      onChange={this.handleOnChange.bind(this)}
                      disabled={!this.state.question.authenticated}
                    />
                    <span className="radio__text">{choice.label}</span>
                    {choice.is_other_choice &&
                      <input
                        className="input-group__input"
                        type="text"
                        name="question"
                        id={'id_choice-' + choice.id + '-single'}
                        onChange={this.handleTextChange.bind(this)}
                        disabled={!this.state.question.authenticated}
                      />}
                  </label>
                )
              } else {
                return (
                  <label className="poll-row radio" key={choice.id} htmlFor={'id_choice-' + choice.id + '-multiple'}>
                    <input
                      className="poll-row__radio radio__input"
                      type="checkbox"
                      name="question"
                      id={'id_choice-' + choice.id + '-multiple'}
                      value={choice.id}
                      checked={checked}
                      onChange={this.handleOnMultiChange.bind(this)}
                      disabled={!this.state.question.authenticated}
                    />
                    <span className="radio__text radio__text--checkbox">{choice.label}</span>
                    {choice.is_other_choice &&
                      <input
                        className="input-group__input"
                        type="text"
                        name="question"
                        id={'id_choice-' + choice.id + '-single'}
                        onChange={this.handleTextChange.bind(this)}
                        disabled={!this.state.question.authenticated}
                      />}
                  </label>
                )
              }
            })
          }
        </div>
      </form>
    )
  }
}
