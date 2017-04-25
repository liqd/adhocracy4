var React = require('react')
var ReactDOM = require('react-dom')
var django = require('django')

var Poll = React.createClass({
  getInitialState: function () {
    // FIXME: example data
    return {
      title: 'Getrennte Eltern: Ist das Wechselmodell die beste Lösung für alle?',
      options: [{
        label: 'Ja',
        count: 22434
      }, {
        label: 'Nein',
        count: 40062
      }, {
        label: 'Vielleicht',
        count: 17627
      }],
      own: null,
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
        own: value
      })
    }
  },

  render: function () {
    let counts = this.state.options.map(o => o.count)
    let total = counts.reduce((sum, c) => sum + c, 0)
    let max = Math.max.apply(null, counts)

    return (
      <form onSubmit={this.vote}>
        <h2>{ this.state.title }</h2>

        <div className="poll">
          {
            this.state.options.map((option, i) => {
              let checked = this.state.own === i
              let percent = Math.round(option.count / total * 100)
              let highlight = option.count === max

              if (this.state.showResult || !this.state.active) {
                return (
                  <div className="poll-row" key={i}>
                    <div className={'poll-row__bar' + (highlight ? ' poll-row__bar--highlight' : '')} style={{width: percent + '%'}} />
                    <div className="poll-row__number">{ percent }%</div>
                    <div className="poll-row__label">{ option.label }</div>
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
                    &nbsp;
                    { option.label }
                  </label>
                )
              }
            })
          }
        </div>

        { !this.state.active ? (
          '' + total + ' ' + django.ngettext(total, 'votes')
        ) : this.state.showResult ? (
          <button type="button" className="button button--light" onClick={this.toggleShowResult}>
            { django.gettext('To poll') }
          </button>
        ) : (
          <div>
            <button type="submit" className="button button--secondary">
              { django.gettext('Vote') }
            </button>
            &nbsp;
            <button type="button" className="button button--light" onClick={this.toggleShowResult}>
              { django.gettext('Show preliminary results') }
            </button>
          </div>
        ) }
      </form>
    )
  }
})

module.exports.renderPolls = function (mountpoint) {
  let element = document.getElementById(mountpoint)
  ReactDOM.render(<Poll />, element)
}
