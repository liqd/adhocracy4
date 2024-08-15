import React from 'react'
import { createRoot } from 'react-dom/client'
import django from 'django'

import api from '../../../static/api'
import config from '../../../static/config'

const translations = {
  upvote: django.gettext('Click to vote up'),
  downvote: django.gettext('Click to vote down'),
  likes: django.gettext('Likes'),
  dislikes: django.gettext('Dislikes')
}

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
      let number
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
      let number
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
      const cssClasses = this.state.userRating === valueForRatingType
        ? 'rating-button rating-' + ratingType + ' is-selected'
        : 'rating-button rating-' + ratingType
      return cssClasses
    }

    return (
      <div className="rating">
        <button
          aria-label={translations.upvote}
          className={getRatingClasses('up')}
          disabled={this.props.isReadOnly}
          onClick={this.ratingUp.bind(this)}
        >
          <i className="fa fa-chevron-up" aria-hidden="true" />
          {this.state.positiveRatings}
          <span className="rating__label">{translations.likes}</span>
        </button>
        <button
          aria-label={translations.downvote}
          className={getRatingClasses('down')}
          disabled={this.props.isReadOnly}
          onClick={this.ratingDown.bind(this)}
        >
          <i className="fa fa-chevron-down" aria-hidden="true" />
          {this.state.negativeRatings}
          <span className="rating__label">{translations.dislikes}</span>
        </button>
      </div>
    )
  }
}

module.exports.RatingBox = RatingBox

module.exports.renderRatings = function (el) {
  const props = JSON.parse(el.getAttribute('data-attributes'))

  const root = createRoot(el)
  root.render(<RatingBox {...props} />)
}
