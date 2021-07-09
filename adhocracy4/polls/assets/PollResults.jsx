import React from 'react'
import Slider from 'react-slick'
import django from 'django'

export default class PollResult extends React.Component {
  constructor (props) {
    super(props)

    const question = this.props.question

    this.state = {
      question: question,
      selectedChoices: question.userChoices,
      showResult: (question.userChoices.length !== 0) || question.isReadOnly,
      alert: null,
      showOtherAnswers: false
    }
  }

  // FIXME - should add animation for poll results but not current priority
  // doBarTransition (node, style) {
  //   if (node && node.style) {
  //     window.requestAnimationFrame(() => Object.assign(node.style, style))
  //   }
  // }

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
      } else if (total === 1 && totalMulti > 1) {
        helpTextAnswerPlural = django.gettext('%s participant gave %s answers.', total)
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
      helpTextOpenAnswer = django.gettext('noone has answered this question')
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
      infinite: true,
      centerMode: false
    }

    return (
      <div className="poll">
        <h2>{this.state.question.label}</h2>
        <div className="poll__rows">
          {this.state.question.choices.map((choice, i) => {
            const percent = total === 0 ? 0 : Math.round(choice.count / total * 100)
            const chosen = this.state.question.userChoices.indexOf(choice.id) !== -1
            const highlight = choice.count === max && max > 0
            if (!this.state.question.is_open) {
              return (
                <div key={choice.id} className="poll-row__container">
                  {chosen ? <i className="poll-row__chosen fa fa-check" aria-label={django.gettext('Your choice')} /> : ''}
                  <div className="poll-row poll-row--answered">
                    <div className="poll-row__number">{percent}%</div>
                    <div className="poll-row__label">{choice.label}</div>
                    <div
                      className={'poll-row__bar' + (highlight ? ' poll-row__bar--highlight' : '')}
                      style={{ width: percent + '%' }}
                    />
                  </div>
                  {choice.is_other_choice &&
                    <div>
                      <button type="button" className="btn btn--link" onClick={() => this.toggleOtherAnswers()}>
                        {this.getOtherAnswerText()}
                      </button>
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
                                  {slide.answer}
                                </div>
                                <div className="poll-slider__count">
                                  {index + 1}/{this.props.question.other_choice_answers.length}
                                </div>
                              </div>
                            ))}
                          </Slider>
                        </div>}
                    </div>}
                </div>
              )
            }
          })}
          {this.state.question.is_open &&
            <div className="poll-slider__container">
              <Slider {...settings} id={this.state.question.id}>
                {this.props.question.answers.map((slide, index) => (
                  <div
                    className="poll-slider__item"
                    data-index={index}
                    key={index}
                  >
                    <div className="poll-slider__answer">
                      {slide.answer}
                    </div>
                    <div className="poll-slider__count">
                      {index + 1}/{this.props.question.answers.length}
                    </div>
                  </div>
                ))}
              </Slider>
            </div>}
          {this.state.question.is_open ? (
            <div className="u-muted">{this.getHelpTextOpenAnswer()}</div>
          ) : (
            <div className="u-muted">{this.getHelpTextAnswer()}</div>
          )}
        </div>
      </div>
    )
  }
}
