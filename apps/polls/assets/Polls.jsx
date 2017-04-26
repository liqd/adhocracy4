var React = require('react')
var ReactDOM = require('react-dom')
var django = require('django')

var Poll = React.createClass({
  getInitialState: function () {
    // FIXME: example data
    return {
      title: 'Getrennte Eltern: Ist das Wechselmodell die beste Lösung für alle?',
      choices: [{
        label: 'Ja',
        count: 22434
      }, {
        label: 'Nein',
        count: 40062
      }, {
        label: 'Vielleicht',
        count: 17627
      }],
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

    let rawValue = event.target.poll.value
    if (!rawValue) {
      // TODO: show error
    } else {
      let value = parseInt(rawValue)
      // TODO: sent to server
      // TODO: show success/error message
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
        <h2>{ this.state.title }</h2>

        <div className="poll">
          {
            this.state.choices.map((choice, i) => {
              let checked = this.state.ownChoice === i
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

module.exports.renderPolls = function (mountpoint) {
  let element = document.getElementById(mountpoint)
  ReactDOM.render(<Poll />, element)
}
