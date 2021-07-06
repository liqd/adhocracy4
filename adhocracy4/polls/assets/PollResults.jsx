import Slider from 'react-slick'

const React = require('react')
const django = require('django')

export default class PollResult extends React.Component {
  constructor (props) {
    super(props)

    const question = this.props.question

    this.state = {
      question: question,
      selectedChoices: question.userChoices,
      showResult: !(question.userChoices.length === 0) || question.isReadOnly,
      alert: null
    }
  }

  toggleShowResult () {
    this.setState({
      selectedChoices: this.state.question.userChoices,
      showResult: !this.state.showResult
    })
  }

  // FIXME - should add animation for poll results but not current priority
  // doBarTransition (node, style) {
  //   if (node && node.style) {
  //     window.requestAnimationFrame(() => Object.assign(node.style, style))
  //   }
  // }

  getHelpText () {
    let helpText
    if (!this.state.showResult) {
      if (this.state.question.multiple_choice) {
        helpText = <div className="poll__help-text">{django.gettext('Multiple answers are possible.')}</div>
      }
    }
    return (
      helpText
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

  render () {
    const max = Math.max.apply(null, this.state.question.choices.map(c => c.count))
    const total = this.state.question.totalVoteCount
    const settings = {
      dots: true,
      infinite: true,
      speed: 500,
      slidesToShow: 1,
      slidesToScroll: 1,
      className: 'sliderContainerTest'
    }

    return (
      <div className="poll">
        <h2>{this.state.question.label}</h2>
        {this.getHelpText()}
        <div className="poll__rows">
          {this.state.question.choices.map((choice, i) => {
            const percent = total === 0 ? 0 : Math.round(choice.count / total * 100)
            const highlight = choice.count === max && max > 0
            if (!this.state.question.is_open) {
              return (
                <div key={choice.id}>
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
                      <Slider {...settings}>
                        {this.state.question.other_choice_answers.map((slide, index) => {
                          return (
                            <div className="react-slider" key={index}>
                              {this.state.question.userAnswer}
                            </div>
                          )
                        })}
                      </Slider>
                    </div>}
                </div>
              )
            } else {
              return (
                <div>
                  <Slider {...settings}>
                    {this.state.question.userAnswer.map((slide, index) => {
                      <div className="react-slider" key={index}>
                        {this.state.question.userAnswer}
                      </div>
                    })}
                  </Slider>
                </div>
              )
            }
          })}
          {this.getHelpTextAnswer()}
        </div>
      </div>
    )
  }
}
