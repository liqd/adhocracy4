var api = require('../../../static/api')
var django = require('django')
var React = require('react')

class FollowDropdown extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      followed: undefined,
      follows: 0
    }
  }
  setFollow (enabled) {
    if (enabled === this.state.followed) {
      return false
    }

    api.follow.change({ enabled: enabled }, this.props.project)
      .done((follow) => {
        this.setState({
          followed: follow.enabled,
          follows: follow.follows
        })
      })
  }
  enableFollow () {
    this.setFollow(true)
  }
  disableFollow () {
    this.setFollow(false)
  }
  componentDidMount () {
    api.follow.get(this.props.project)
      .done((follow) => {
        this.setState({
          followed: follow.enabled,
          follows: follow.follows
        })
      })
      .fail((response) => {
        if (response.status === 404) {
          this.setState({
            followed: false
          })
        }
      })
  }
  render () {
    // FIXME: string extraction seems to be broken with JSX
    var notFollowingLabel = django.gettext('Not following')
    var notFollowingHelp = django.gettext('Never be notified.')
    var followingLabel = django.gettext('Following')
    var followingHelp = django.gettext('Receive email notifications about this project.')

    return (
      <span className="btngroup btngroup-gray">
        <span className="dropdown">
          <button className="btn btn-secondary dropdown-toggle" type="button" id="follow-dropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <i className="fa fa-star" aria-hidden="true" />&nbsp;
            {this.state.followed ? django.gettext('Unfollow') : django.gettext('Follow')}&nbsp;
            <i className="fa fa-caret-down" aria-hidden="true" />
          </button>
          <span className="dropdown-menu" aria-labelledby="follow-dropdown">
            <button className="dropdown-item select-item" onClick={this.disableFollow.bind(this)}>
              {!this.state.followed ? <i className="fa fa-check select-item-indicator" aria-hidden="true" /> : null}
              {notFollowingLabel}
              <span className="select-item-desc">
                {notFollowingHelp}
              </span>
            </button>
            <button className="dropdown-item select-item" onClick={this.enableFollow.bind(this)}>
              {this.state.followed ? <i className="fa fa-check select-item-indicator" aria-hidden="true" /> : null}
              {followingLabel}
              <span className="select-item-desc">
                {followingHelp}
              </span>
            </button>
          </span>
        </span>
        <span className="btn btn-sm btn-dark btn-primary">{this.state.follows}</span>
      </span>
    )
  }
}

module.exports = FollowDropdown
