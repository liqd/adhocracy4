import React, { useState, useEffect } from 'react'
import ReactDOM from 'react-dom'
import django from 'django'
import Alert from '../../../static/Alert'
import api from '../../../static/api'
import config from '../../../static/config'

const translated = {
  followDescription: django.gettext(
    'Click to be updated about this project via email.'
  ),
  followingDescription: django.gettext(
    'Click to no longer be updated about this project via email.'
  ),
  followAlert: django.gettext('From now on, we\'ll keep you updated on all changes. Make sure email notifications are enabled in your %(linkStart)s profile settings%(linkEnd)s'),
  followingAlert: django.gettext('You will no longer be updated via email.'),
  follow: django.gettext('Follow'),
  following: django.gettext('Following')
}

export const FollowButton = ({
  project,
  authenticatedAs,
  customClasses = '',
  alertTarget = null
}) => {
  const [following, setFollowing] = useState(null)
  const [alert, setAlert] = useState(null)

  const linkParts = {
    linkStart: '<a href="/account/profile" target="_blank">',
    linkEnd: '<i class="fas fa-external-link-alt" role="img" aria-label="Opens in new window"></i></a>'
  }

  const fullFollowAlertText = django.interpolate(translated.followAlert, linkParts, true)

  const followBtnText = following ? translated.following : translated.follow
  const followDescriptionText = following
    ? translated.followingDescription
    : translated.followDescription

  useEffect(() => {
    if (authenticatedAs) {
      api.follow
        .get(project)
        .done((follow) => {
          setFollowing(follow.enabled)
        })
        .fail((response) => {
          if (response.status === 404) {
            setFollowing(false)
          }
        })
    }
  }, [project, authenticatedAs])

  const removeAlert = () => {
    setAlert(null)
  }

  const toggleFollow = () => {
    if (authenticatedAs === null) {
      window.location.href = config.getLoginUrl()
      return
    }

    api.follow.change({ enabled: !following }, project).done((follow) => {
      setFollowing(follow.enabled)
      setAlert({
        type: follow.enabled ? 'success' : 'warning',
        htmlMessage: follow.enabled ? fullFollowAlertText : translated.followingAlert
      })
    })
  }

  const buttonClasses = following ? 'a4-btn a4-btn--following' : 'a4-btn a4-btn--follow'

  const AlertPortal = () => {
    if (!alert) return null

    if (!alertTarget) {
      console.error('AlertPortal: No alert target provided')
      return null
    }

    const container = document.getElementById(alertTarget)

    if (!container) {
      console.error('AlertPortal: Target element with ID "' + alertTarget + '" not found in DOM')
      return null
    }

    return ReactDOM.createPortal(
      <Alert onClick={removeAlert} {...alert} />,
      container
    )
  }

  return (
    <span className={'a4-follow ' + customClasses}>
      <button
        className={buttonClasses}
        type="button"
        onClick={toggleFollow}
        aria-describedby="follow-description"
        aria-pressed={following}
        disabled={following === null && authenticatedAs !== null}
      >
        <span className="a4-follow__btn--content">{followBtnText}</span>

        <span className="a4-sr-only" id="follow-description">
          {followDescriptionText}
        </span>
      </button>

      {alertTarget
        ? (
          <AlertPortal />
          )
        : (
          <span className="a4-follow__notification">
            <Alert onClick={removeAlert} {...alert} />
          </span>
          )}
    </span>
  )
}

export default FollowButton
