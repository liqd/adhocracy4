var api = require('adhocracy4').api
var React = require('react')
var django = require('django')
var Alert = require('../../contrib/assets/Alert')
var update = require('immutability-helper')

class Question extends React.Component {
  constructor (props) {
    super(props)

    const choices = this.props.question.choices
    const isReadOnly = this.props.question.isReadOnly
    const userChoices = this.props.question.userChoices
    this.state = {
      totalCount: this.props.question.totalVoteCount,
      counts: this.countChoices(choices),
      userChoices: userChoices,
      selectedChoices: userChoices,
      showResult: !(userChoices.length === 0) || isReadOnly,
      alert: null
    }
  }

  countChoices (choices) {
    let counts = {}
    for (const index in choices) {
      const choice = choices[index]
      counts[choice.id] = choice.count
    }
    return counts
  }

  toggleShowResult () {
    this.setState({
      selectedChoices: this.state.userChoices,
      showResult: !this.state.showResult
    })
  }

  handleSubmit (event) {
    event.preventDefault()

    if (this.props.question.isReadOnly) {
      return false
    }

    let newChoices = this.state.selectedChoices

    let submitData = {
      choices: newChoices,
      urlReplaces: {questionId: this.props.question.id}
    }

    api.poll.vote(submitData)
      .done((data) => {
        let newChoices = data.choices

        /*
        let counts = this.state.counts
        counts[newChoice]++

        if (this.state.ownChoice !== null) {
          counts[this.state.ownChoice]--
        }
        */

        this.setState({
          showResult: true,
          userChoices: newChoices,
          selectedChoices: newChoices,
          counts: [],
          alert: {
            type: 'success',
            message: django.gettext('Vote counted')
          }
        })
      })
      .fail((xhr, status, err) => {
        this.setState({
          showResult: false,
          selectedChoices: newChoices,
          alert: {
            type: 'danger',
            message: django.gettext('Vote has not been counted due to a server error.')
          }
        })
      })
  }

  removeAlert () {
    this.setState({
      alert: null
    })
  }

  handleOnChange (event) {
    var diff = {'$set': [parseInt(event.target.value)]}

    this.setState({
      selectedChoices: update(this.state.selectedChoices, diff)
    })
  }

  handleOnMultiChange (event) {
    var diff = {}
    if (event.target.checked) {
      diff = {'$push': [parseInt(event.target.value)]}
    } else {
      var index = this.state.selectedChoices.indexOf(parseInt(event.target.value))
      diff = {'$splice': [[index, 1]]}
    }

    this.setState({
      selectedChoices: update(this.state.selectedChoices, diff)
    })
  }

  getVoteButton () {
    if (this.props.question.isReadOnly) {
      return null
    }

    if (this.props.question.authenticated) {
      return (
        <button
          type="submit"
          className="btn btn--primary"
          disabled={this.state.selectedChoices === this.state.userChoices}>
          { django.gettext('Vote') }
        </button>
      )
    } else {
      let loginUrl = '/accounts/login/?next=' +
        encodeURIComponent(window.adhocracy4.getCurrentPath())

      return (
        <a href={loginUrl} className="btn btn--primary">
          { django.gettext('Please login to vote') }
        </a>
      )
    }
  }

  doBarTransition (node, style) {
    if (node && node.style) {
      window.requestAnimationFrame(() => Object.assign(node.style, style))
    }
  }

  render () {
    const total = this.state.totalCount
    let max = 0
    for (const choiceId in this.state.counts) {
      if (this.state.counts[choiceId] > max) {
        max = this.state.counts[choiceId]
      }
    }

    let footer
    let totalString = `${total} ${django.ngettext('vote', 'votes', total)}`
    if (this.state.showResult) {
      footer = (
        <div className="poll__actions">
          { totalString }
          &nbsp;
          {!this.props.question.isReadOnly &&
            <button type="button" className="btn btn--link" onClick={this.toggleShowResult.bind(this)}>
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
          <button type="button" className="btn btn--link" onClick={this.toggleShowResult.bind(this)}>
            { django.gettext('Show preliminary results') }
          </button>
        </div>
      )
    }

    return (
      <form onSubmit={this.handleSubmit.bind(this)} className="poll">
        <h2>{ this.props.question.label }</h2>

        <div className="poll__rows">
          {
            this.props.question.choices.map((choice, i) => {
              let checked = this.state.selectedChoices.indexOf(choice.id) !== -1
              let chosen = this.state.userChoices.indexOf(choice.id) !== -1
              let count = this.state.counts[choice.id]
              let percent = total === 0 ? 0 : Math.round(count / total * 100)
              let highlight = count === max && max > 0

              if (this.state.showResult) {
                return (
                  <div className="poll-row" key={choice.id}>
                    <div className="poll-row__number">{ percent }%</div>
                    <div className="poll-row__label">{ choice.label }</div>
                    { chosen ? <i className="fa fa-check-circle u-primary" aria-label={django.gettext('Your choice')} /> : '' }
                    <div className={'poll-row__bar' + (highlight ? ' poll-row__bar--highlight' : '')}
                      ref={node => this.doBarTransition(node, {width: percent + '%'})} />
                  </div>
                )
              } else {
                if (!this.props.question.multiple_choice) {
                  return (
                    <label className="poll-row radio" key={choice.id}>
                      <input
                        className="poll-row__radio radio__input"
                        type="radio"
                        name="question"
                        value={choice.id}
                        checked={checked}
                        onChange={this.handleOnChange.bind(this)}
                        disabled={!this.props.question.authenticated}
                      />
                      <span className="radio__text">{ choice.label }</span>
                    </label>
                  )
                } else {
                  return (
                    <label className="poll-row checkbox" key={choice.id}>
                      <input
                        className="poll-row__checkbox checkbox__input"
                        type="checkbox"
                        name="question"
                        value={choice.id}
                        checked={checked}
                        onChange={this.handleOnMultiChange.bind(this)}
                        disabled={!this.props.question.authenticated}
                      />
                      <span className="checkbox__text">{ choice.label }</span>
                    </label>
                  )
                }
              }
            })
          }
        </div>

        <Alert onClick={this.removeAlert.bind(this)} {...this.state.alert} />
        { footer }
      </form>
    )
  }
}

module.exports = Question
