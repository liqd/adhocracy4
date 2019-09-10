var api = require('../../../static/api')
var django = require('django')
var PropTypes = require('prop-types')
var React = require('react')

class FollowButton extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      followed: undefined,
      follows: 0
    }
  }

  toggleFollow () {
    api.follow.change({ enabled: !this.state.followed }, this.props.project)
      .done((follow) => {
        this.setState({
          followed: follow.enabled,
          follows: follow.follows
        })
      })
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
    return (
      <span>
        <button className={this.state.followed ? 'btn btn-sm btn-secondary' : 'btn btn-sm btn-transparent'} type="button" onClick={this.toggleFollow.bind(this)}>
          <i className={this.state.followed ? 'fa fa-check' : 'fa fa-plus'} aria-hidden="true" />&nbsp;<span className="follow__btn--content">{this.state.followed ? django.gettext('Following') : django.gettext('Follow project')}</span>
        </button>
      </span>
    )
  }
}

FollowButton.propTypes = {
  project: PropTypes.string.isRequired
}

module.exports = FollowButton
