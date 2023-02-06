import React from 'react'
import Slider from 'react-slick'
import django from 'django'

export default class PollResult extends React.Component {
  constructor (props) {
    super(props)

    const question = this.props.question
    const openOrOtherAnswerId = question.is_open
      ? question.userAnswer
      : question.other_choice_user_answer

    this.state = {
      question,
      selectedChoices: question.userChoices,
      showResult: (question.userChoices.length !== 0) || question.isReadOnly,
      alert: null,
      showOtherAnswers: false,
      userAnswerId: openOrOtherAnswerId
    }
  }

  doBarTransition (node, style) {
    if (node && node.style) {
      window.requestAnimationFrame(() => Object.assign(node.style, style))
    }
  }

  isUserAnswer (slide) {
    const matchedId = this.state.question.is_open
      ? slide.id === this.state.userAnswerId
      : slide.vote_id === this.state.userAnswerId
    return !!matchedId
  }

  toggleOtherAnswers () {
    this.setState(prevState => ({ showOtherAnswers: !prevState.showOtherAnswers }))
  }

  getOtherAnswerText () {
    let otherAnswerText
    if (this.state.showOtherAnswers) {
      otherAnswerText = <span>{django.gettext('Hide other answers')}</span>
    } else {
      otherAnswerText = <span>{django.gettext('Show other answers')}</span>
    }
    return (
      otherAnswerText
    )
  }

  getHelpTextAnswer () {
    const total = this.state.question.totalVoteCount
    const totalMulti = this.state.question.totalVoteCountMulti
    let helpTextAnswer
    let helpTextAnswerPlural
    if (this.state.question.multiple_choice) {
      if (total === 1 && totalMulti === 1) {
        helpTextAnswerPlural = django.gettext('%s participant gave 1 answer.')
      } else {
        helpTextAnswerPlural = django.ngettext('%s participant gave %s answers.', '%s participants gave %s answers.', total)
      }
      helpTextAnswer = helpTextAnswerPlural + django.gettext(' For multiple choice questions the percentages may add up to more than 100%.')
    } else {
      helpTextAnswer = django.ngettext('1 person has answered.', '%s people have answered.', total)
    }
    return django.interpolate(helpTextAnswer, [total, totalMulti])
  }

  getHelpTextOpenAnswer () {
    const total = this.state.question.totalAnswerCount
    let helpTextOpenAnswer
    if (total >= 1) {
      helpTextOpenAnswer = django.ngettext('1 person has answered.', '%s people have answered.', total)
    } else {
      helpTextOpenAnswer = django.gettext('no one has answered this question')
    }
    return django.interpolate(helpTextOpenAnswer, [total])
  }

  render () {
    const max = Math.max.apply(null, this.state.question.choices.map(c => c.count))
    const total = this.state.question.totalVoteCount

    const settings = {
      arrows: true,
      speed: 500,
      slidesToShow: 1,
      slidesToScroll: 1,
      className: 'poll-slider',
      infinite: false,
      centerMode: true,
      centerPadding: '0px'
    }

    return (
      <div className="poll">
        <h2>{this.state.question.label}</h2>
        <div className="poll__rows">
          {this.state.question.choices.map((choice, i) => {
            const percent = total === 0 ? 0 : Math.round(choice.count / total * 100)
            const chosen = this.state.question.userChoices.indexOf(choice.id) !== -1
            const highlight = choice.count === max && max > 0
            return !this.state.question.is_open &&
              <div key={choice.id} className="poll-row__container">
                {chosen ? <i className="poll-row__chosen fas fa-check-circle" aria-label={django.gettext('Your choice')} /> : ''}
                <div className="poll-row poll-row--answered">
                  <div className="poll-row__number">{percent}%</div>
                  <div className="poll-row__label">{choice.is_other_choice ? django.gettext('other') : choice.label}</div>
                  <div
                    className={'poll-row__bar' + (highlight ? ' poll__highlight' : '')}
                    ref={node => this.doBarTransition(node, { width: percent + '%' })}
                  />
                </div>
                {choice.is_other_choice &&
                  <div>
                    {this.props.question.other_choice_answers.length > 0 &&
                      <button type="button" className="btn poll__btn--link" onClick={() => this.toggleOtherAnswers()}>
                        {this.getOtherAnswerText()}
                      </button>}
                    {this.state.showOtherAnswers &&
                      <div className="poll-slider__container" id={this.state.question.id}>
                        <Slider {...settings}>
                          {this.props.question.other_choice_answers.map((slide, index) => (
                            <div
                              className="poll-slider__item"
                              data-index={index}
                              key={index}
                            >
                              <div className="poll-slider__answer">
                                {this.isUserAnswer(slide) && <i className="fas fa-check-circle" />} {slide.answer}
                              </div>
                              <div className={this.props.question.other_choice_answers.length > 1 ? 'poll-slider__count--spaced' : 'poll-slider__count'}>
                                {index + 1}/{this.props.question.other_choice_answers.length}
                              </div>
                            </div>
                          ))}
                        </Slider>
                      </div>}
                  </div>}
              </div>
          }
          )}
          {this.state.question.is_open && this.state.question.answers.length > 0 &&
            <div className="poll-slider__container">
              <Slider {...settings}>
                {this.props.question.answers.map((slide, index) => (
                  <div
                    className="poll-slider__item"
                    data-index={index}
                    key={index}
                  >
                    <div className="poll-slider__answer">
                      {this.isUserAnswer(slide) && <i className="fas fa-check-circle" />} {slide.answer}
                    </div>
                    <div className={this.props.question.answers.length > 1 ? 'poll-slider__count--spaced' : 'poll-slider__count'}>
                      {index + 1}/{this.props.question.answers.length}
                    </div>
                  </div>
                ))}
              </Slider>
            </div>}
          {this.state.question.is_open
            ? (
              <div className="a4-muted">{this.getHelpTextOpenAnswer()}</div>
              )
            : (
              <div className="a4-muted">{this.getHelpTextAnswer()}</div>
              )}
        </div>
      </div>
    )
  }
}
