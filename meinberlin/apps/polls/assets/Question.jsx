var api = require('adhocracy4').api
var React = require('react')
var django = require('django')
var Alert = require('../../contrib/assets/Alert')

var Question = React.createClass({
  getInitialState: function () {
    const choices = this.props.question.choices
    const hasFinished = this.props.question.hasFinished
    const ownChoice = this.findOwnChoice(choices)
    return {
      counts: choices.map(o => o.count),
      ownChoice: ownChoice,
      selectedChoice: ownChoice,
      active: true,
      showResult: !(ownChoice === null) || hasFinished,
      alert: null
    }
  },

  findOwnChoice: function (choices) {
    let ownChoice = null
    choices.forEach(function (choice, i) {
      if (choice.ownChoice) {
        ownChoice = i
      }
    })
    return ownChoice
  },

  findIndexForChoiceId: function (id) {
    let index = null
    this.props.question.choices.forEach(function (choice, i) {
      if (choice.id === id) {
        index = i
      }
    })
    return index
  },

  toggleShowResult: function () {
    this.setState({
      selectedChoice: this.state.ownChoice,
      showResult: !this.state.showResult
    })
  },

  handleSubmit: function (event) {
    event.preventDefault()

    if (this.props.question.hasFinished) {
      return false
    }

    let newChoice = this.state.selectedChoice

    let submitData = {
      choice: this.props.question.choices[newChoice].id
    }

    api.poll.vote(submitData, this.props.question.id)
      .done((data) => {
        let newChoice = this.findIndexForChoiceId(data.choice)

        let counts = this.state.counts
        counts[newChoice]++

        if (this.state.ownChoice !== null) {
          counts[this.state.ownChoice]--
        }

        this.setState({
          showResult: true,
          ownChoice: newChoice,
          selectedChoice: newChoice,
          counts: counts,
          alert: {
            type: 'success',
            message: django.gettext('Vote counted')
          }
        })
      })
      .fail((xhr, status, err) => {
        this.setState({
          showResult: false,
          selectedChoice: newChoice,
          alert: {
            type: 'danger',
            message: django.gettext('Vote has not been counted due to a server error.')
          }
        })
      })
  },

  removeAlert: function () {
    this.setState({
      alert: null
    })
  },

  handleOnChange: function (event) {
    this.setState({
      selectedChoice: parseInt(event.target.value)
    })
  },

  getVoteButton: function () {
    if (this.props.question.hasFinished) {
      return null
    }

    if (this.props.question.authenticated) {
      return (
        <button
          type="submit"
          className="button button--primary"
          disabled={this.state.selectedChoice === this.state.ownChoice}>
          { django.gettext('Vote') }
        </button>
      )
    } else {
      let loginUrl = '/accounts/login/?next=' +
        encodeURIComponent(window.adhocracy4.getCurrentHref())

      return (
        <a href={loginUrl} className="button button--primary">
          { django.gettext('Vote') }
        </a>
      )
    }
  },

  render: function () {
    let counts = this.state.counts
    let total = counts.reduce((sum, c) => sum + c, 0)
    let max = Math.max.apply(null, counts)

    let footer
    let totalString = `${total} ${django.ngettext('vote', 'votes', total)}`
    if (!this.state.active) {
      footer = totalString
    } else if (this.state.showResult) {
      footer = (
        <div className="poll__actions">
          { totalString }
          &nbsp;
          {!this.props.question.hasFinished &&
            <button type="button" className="button button--link" onClick={this.toggleShowResult}>
              { django.gettext('To poll') }
            </button>
          }
        </div>
      )
    } else {
      footer = (
        <div className="poll__actions">
          {this.getVoteButton()}
          &nbsp;
          <button type="button" className="button button--link" onClick={this.toggleShowResult}>
            { django.gettext('Show preliminary results') }
          </button>
        </div>
      )
    }

    return (
      <form onSubmit={this.handleSubmit} className="poll">
        <h2>{ this.props.question.label }</h2>

        <div className="poll__rows">
          {
            this.props.question.choices.map((choice, i) => {
              let checked = this.state.selectedChoice === i
              let chosen = this.state.ownChoice === i
              let count = this.state.counts[i]
              let percent = total === 0 ? 0 : Math.round(count / total * 100)
              let highlight = count === max && max > 0

              if (this.state.showResult || !this.state.active) {
                return (
                  <div className="poll-row" key={i}>
                    <div className="poll-row__number">{ percent }%</div>
                    <div className="poll-row__label">{ choice.label }</div>
                    { chosen ? <i className="fa fa-check-circle u-primary" aria-label={django.gettext('Your choice')} /> : '' }
                    <div className={'poll-row__bar' + (highlight ? ' poll-row__bar--highlight' : '')} style={{width: percent + '%'}} />
                  </div>
                )
              } else {
                return (
                  <label className="poll-row radio" key={i}>
                    <input
                      className="poll-row__radio radio__input"
                      type="radio"
                      name="question"
                      value={i}
                      checked={checked}
                      onChange={this.handleOnChange}
                    />
                    <span className="radio__text">{ choice.label }</span>
                  </label>
                )
              }
            })
          }
        </div>

        <Alert onClick={this.removeAlert} {...this.state.alert} />
        { footer }
      </form>
    )
  }
})

module.exports = Question
