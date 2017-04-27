var React = require('react')
var django = require('django')

var Question = React.createClass({
  getInitialState: function () {
    // FIXME: example data
    return {
      label: this.props.question.label,
      choices: this.props.question.choices,
      ownChoice: null,
      active: true,
      showResult: false
    }
  },

  toggleShowResult: function () {
    this.setState({
      showResult: !this.state.showResult
    })
  },

  vote: function (event) {
    event.preventDefault()

    let rawValue = event.target.question.value
    if (!rawValue) {
      // TODO: show error
    } else {
      let value = parseInt(rawValue)
      // TODO: sent to server
      // TODO: show success/error message
      // TODO: Fix for ownChoice within choice
      this.setState({
        showResult: true,
        ownChoice: value
      })
    }
  },

  render: function () {
    let counts = this.state.choices.map(o => o.count)
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
      <form onSubmit={this.vote}>
        <h2>{ this.state.label }</h2>

        <div className="poll">
          {
            this.state.choices.map((choice, i) => {
              let checked = choice.ownChoice
              let percent = Math.round(choice.count / total * 100)
              let highlight = choice.count === max

              if (this.state.showResult || !this.state.active) {
                return (
                  <div className="poll-row" key={i}>
                    <div className={'poll-row__bar' + (highlight ? ' poll-row__bar--highlight' : '')} style={{width: percent + '%'}} />
                    <div className="poll-row__number">{ percent }%</div>
                    <div className="poll-row__label">{ choice.label }</div>
                    { checked ? <i className="fa fa-check-circle u-secondary" aria-label={django.gettext('Your choice')} /> : '' }
                  </div>
                )
              } else {
                return (
                  <label className="poll-row" key={i}>
                    <input
                      className="poll-row__radio"
                      type="radio"
                      name="poll"
                      value={i}
                      defaultChecked={checked} />
                    { choice.label }
                  </label>
                )
              }
            })
          }
        </div>

        { footer }
      </form>
    )
  }
})

module.exports = Question
