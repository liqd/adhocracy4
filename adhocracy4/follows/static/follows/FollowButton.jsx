var api = require('../../../static/api')
var django = require('django')
var PropTypes = require('prop-types')
var React = require('react')
var Alert = require('../../../static/Alert')

class FollowButton extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      followed: undefined,
      follows: 0,
      alert: null
    }
  }

  removeAlert () {
    this.setState({
      alert: null
    })
  }

  toggleFollow () {
    var followAlertText
    if (this.state.followed) {
      followAlertText = django.gettext('You unfollowed this project. You will no longer receive e-mails regarding this project.')
    } else {
      followAlertText = django.gettext('Thank you for your interest! From now on you will be kept up to date via e-mail.')
    }
    api.follow.change({ enabled: !this.state.followed }, this.props.project)
      .done((follow) => {
        this.setState({
          followed: follow.enabled,
          follows: follow.follows,
          alert: {
            type: 'success',
            message: followAlertText
          }
        })
      })
  }

  componentDidMount () {
    api.follow.get(this.props.project)
      .done((follow) => {
        this.setState({
          followed: follow.enabled,
          follows: follow.follows,
          alert: follow.alert
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
    var followTag = django.gettext('Follow')
    var followingTag = django.gettext('Following')
    return (
      <span className="follow">
        <button className={this.state.followed ? 'btn btn--sm btn--light' : 'btn btn--sm btn--secondary'} type="button" onClick={this.toggleFollow.bind(this)}>
          <i className={this.state.followed ? 'fa fa-check' : 'fa fa-plus'} aria-hidden="true" />&nbsp;<span className="follow__btn--content">{this.state.followed ? followingTag : followTag}</span>
        </button>
        <span class="follow__notification">
          <Alert onClick={this.removeAlert.bind(this)} {...this.state.alert} />
        </span>
      </span>
    )
  }
}

FollowButton.propTypes = {
  project: PropTypes.string.isRequired
}

module.exports = FollowButton
