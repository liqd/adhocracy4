import django from 'django'
import React, { useState, useEffect } from 'react'
import Alert from '../../../static/Alert'

const api = require('../../../static/api')

const translated = {
  followDescription: django.gettext('Click to be updated about this project via email.'),
  followingDescription: django.gettext('Click to no longer be updated about this project via email.'),
  followAlert: django.gettext('You will be updated via email.'),
  followingAlert: django.gettext('You will no longer be updated via email.'),
  follow: django.gettext('Follow'),
  following: django.gettext('Following')
}

export const FollowButton = (props) => {
  const [following, setFollowing] = useState(null)
  const [alert, setAlert] = useState(null)

  const followBtnText = following
    ? translated.following
    : translated.follow

  const followDescriptionText = following
    ? translated.followingDescription
    : translated.followDescription

  const followAlertText = following
    ? translated.followingAlert
    : translated.followAlert

  useEffect(() => {
    api.follow.get(props.project)
      .done((follow) => {
        setFollowing(follow.enabled)
        setAlert(follow.alert)
      })
      .fail((response) => {
        if (response.status === 404) {
          setFollowing(false)
        }
      })
  }, [props.project])

  const removeAlert = () => {
    setAlert(null)
  }

  const toggleFollow = () => {
    api.follow.change({ enabled: !following }, props.project)
      .done((follow) => {
        setFollowing(follow.enabled)
        setAlert({
          type: 'success',
          message: followAlertText
        })
      })
  }

  return (
    <span className="a4-follow">
      <button
        className={following ? 'a4-btn a4-btn--following' : 'a4-btn a4-btn--follow'}
        type="button"
        onClick={toggleFollow}
        aria-describedby="follow-description"
        disabled={following === null}
      >
        <span className="a4-follow__btn--content">{followBtnText}</span>
        <span className="a4-sr-only" id="follow-description">{followDescriptionText}</span>
      </button>
      <span className="a4-follow__notification">
        <Alert onClick={removeAlert} {...alert} />
      </span>
    </span>
  )
}
