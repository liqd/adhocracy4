var api = require('../../../static/api')
var config = require('../../../static/config')

var React = require('react')
var ReactDOM = require('react-dom')
var classnames = require('classnames')

class RatingBox extends React.Component {
  constructor (props) {
    super(props)

    this.state = {
      positiveRatings: this.props.positiveRatings,
      negativeRatings: this.props.negativeRatings,
      userHasRating: this.props.userRating !== null,
      userRating: this.props.userRating,
      userRatingId: this.props.userRatingId
    }
  }

  handleRatingCreate (number) {
    api.rating.add({
      urlReplaces: {
        objectPk: this.props.objectId,
        contentTypeId: this.props.contentType
      },
      value: number
    })
      .done(function (data) {
        this.setState({
          positiveRatings: data.meta_info.positive_ratings_on_same_object,
          negativeRatings: data.meta_info.negative_ratings_on_same_object,
          userRating: data.meta_info.user_rating_on_same_object_value,
          userHasRating: true,
          userRatingId: data.id
        })
      }.bind(this))
      .fail(function (jqXhr) {
        if (jqXhr.status === 400 &&
           jqXhr.responseJSON.length === 1 &&
           Number.isInteger(parseInt(jqXhr.responseJSON[0]))) {
          this.setState({
            userHasRating: true,
            userRatingId: jqXhr.responseJSON[0]
          })
          this.handleRatingModify(number, this.state.userRatingId)
        }
      }.bind(this))
  }

  handleRatingModify (number, id) {
    api.rating.change({
      urlReplaces: {
        objectPk: this.props.objectId,
        contentTypeId: this.props.contentType
      },
      value: number
    }, id)
      .done(function (data) {
        this.setState({
          positiveRatings: data.meta_info.positive_ratings_on_same_object,
          negativeRatings: data.meta_info.negative_ratings_on_same_object,
          userRating: data.meta_info.user_rating_on_same_object_value
        })
      }.bind(this))
  }

  updateUserRating (data) {
    this.state.ratings[this.state.userRatingIndex] = data
  }

  ratingUp (e) {
    e.preventDefault()
    if (this.props.authenticatedAs === null) {
      window.location.href = config.getLoginUrl()
      return
    }
    if (this.props.isReadOnly) {
      return
    }
    if (this.state.userHasRating) {
      var number
      if (this.state.userRating === 1) {
        number = 0
      } else {
        number = 1
      }
      this.handleRatingModify(number, this.state.userRatingId)
    } else {
      this.handleRatingCreate(1)
    }
  }

  ratingDown (e) {
    e.preventDefault()
    if (this.props.authenticatedAs === null) {
      window.location.href = config.getLoginUrl()
      return
    }
    if (this.props.isReadOnly) {
      return
    }
    if (this.state.userHasRating) {
      var number
      if (this.state.userRating === -1) {
        number = 0
      } else {
        number = -1
      }
      this.handleRatingModify(number, this.state.userRatingId)
    } else {
      this.handleRatingCreate(-1)
    }
  }

  render () {
    const getRatingClasses = ratingType => {
      const valueForRatingType = ratingType === 'up' ? 1 : -1
      return classnames(`rating-button rating-${ratingType}`, {
        'is-selected': this.state.userRating === valueForRatingType
      })
    }

    return (
      <div className="rating">
        <button
          className={getRatingClasses('up')}
          disabled={this.props.isReadOnly}
          onClick={this.ratingUp.bind(this)}
        >
          <i className="fa fa-chevron-up" aria-hidden="true" />
          {this.state.positiveRatings}
        </button>
        <button
          className={getRatingClasses('down')}
          disabled={this.props.isReadOnly}
          onClick={this.ratingDown.bind(this)}
        >
          <i className="fa fa-chevron-down" aria-hidden="true" />
          {this.state.negativeRatings}
        </button>
      </div>
    )
  }
}

module.exports.RatingBox = RatingBox

module.exports.renderRatings = function (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))
  ReactDOM.render(<RatingBox {...props} />, el)
}
