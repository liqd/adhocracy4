var api = require('adhocracy4').api
var React = require('react')
var django = require('django')
var Alert = require('../../contrib/static/js/Alert')

var Question = React.createClass({
  getInitialState: function () {
    const choices = this.props.question.choices
    const ownChoice = this.findOwnChoice(choices)
    return {
      counts: choices.map(o => o.count),
      ownChoice: ownChoice,
      selectedChoice: ownChoice,
      active: true,
      showResult: !(ownChoice === null),
      alert: null
    }
  },

  setStateWithAlert: function (state, alert, timeout) {
    state['alert'] = alert
    this.setState(state, () => {
      if (timeout) {
        setTimeout(() => {
          this.setState({
            alert: null
          })
        }, timeout)
      }
    })
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

        this.setStateWithAlert({
          showResult: true,
          ownChoice: newChoice,
          selectedChoice: newChoice,
          counts: counts
        }, {
          type: 'success',
          message: django.gettext('Vote counted')
        }, 1500)
      })
      .fail((xhr, status, err) => {
        this.setStateWithAlert({
          showResult: false,
          selectedChoice: newChoice
        }, {
          type: 'danger',
          message: django.gettext('Vote has not been counted due to a server error.')
        }, 1500)
      })
  },

  handleOnChange: function (event) {
    this.setState({
      selectedChoice: parseInt(event.target.value)
    })
  },

  render: function () {
    let counts = this.state.counts
    let total = counts.reduce((sum, c) => sum + c, 0)
    let max = Math.max.apply(null, counts)

    let footer
    if (!this.state.active) {
      footer = '' + total + ' ' + django.ngettext('vote', 'votes', total)
    } else if (this.state.showResult) {
      footer = (
        <button type="button" className="button button--light" onClick={this.toggleShowResult}>
          { django.gettext('To poll') }
        </button>
      )
    } else {
      footer = (
        <div>
          <button type="submit" className="button button--secondary">
            { django.gettext('Vote') }
          </button>
          &nbsp;
          <button type="button" className="button button--light" onClick={this.toggleShowResult}>
            { django.gettext('Show preliminary results') }
          </button>
        </div>
      )
    }

    return (
      <form onSubmit={this.handleSubmit}>
        <h2>{ this.props.question.label }</h2>

        <div className="poll">
          {
            this.props.question.choices.map((choice, i) => {
              let checked = this.state.selectedChoice === i
              let chosen = this.state.ownChoice === i
              let count = this.state.counts[i]
              let percent = total === 0 ? 0 : Math.round(count / total * 100)
              let highlight = count === max

              if (this.state.showResult || !this.state.active) {
                return (
                  <div className="poll-row" key={i}>
                    <div className={'poll-row__bar' + (highlight ? ' poll-row__bar--highlight' : '')} style={{width: percent + '%'}} />
                    <div className="poll-row__number">{ percent }%</div>
                    <div className="poll-row__label">{ choice.label }</div>
                    { chosen ? <i className="fa fa-check-circle u-secondary" aria-label={django.gettext('Your choice')} /> : '' }
                  </div>
                )
              } else {
                return (
                  <label className="poll-row" key={i}>
                    <input
                      className="poll-row__radio"
                      type="radio"
                      name="question"
                      value={i}
                      checked={checked}
                      onChange={this.handleOnChange}
                    />
                    { choice.label }
                  </label>
                )
              }
            })
          }
        </div>

        <Alert {...this.state.alert} />
        { footer }
      </form>
    )
  }
})

module.exports = Question
