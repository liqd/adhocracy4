import React, { useCallback, useEffect, useState } from 'react'
import ReactDOM from 'react-dom'
import django from 'django'
import Alert from '../../../static/Alert'
import api from '../../../static/api'
import config from '../../../static/config'

const notificationSettingsLink = {
  linkStart: '<a href="/account/notification-settings/" target="_blank">',
  linkEnd:
    '<i class="fas fa-external-link-alt" role="img" aria-label="Opens in new window"></i></a>'
}

export const followStrings = {
  followDescription: django.gettext(
    'Click to be updated about this project via email.'
  ),
  followingDescription: django.gettext(
    'Click to no longer be updated about this project via email.'
  ),
  followAlert: django.gettext(
    'From now on, we\'ll keep you updated on all changes.<br/>Make sure email notifications are enabled in your %(linkStart)s notification settings%(linkEnd)s'
  ),
  followingAlert: django.gettext('You will no longer be updated via email.'),
  follow: django.gettext('Follow'),
  following: django.gettext('Following')
}

export function buildFollowSuccessAlert () {
  return django.interpolate(
    followStrings.followAlert,
    notificationSettingsLink,
    true
  )
}

export const FollowButton = ({
  project,
  authenticatedAs,
  customClasses = '',
  alertTarget = null,
  buttonTarget = null,
  buttonClassName = '',
  descriptionId = 'follow-description',
  onFollowChange = null,
  onFollowStateChange = null
}) => {
  const [following, setFollowing] = useState(null)
  const [alert, setAlert] = useState(null)

  useEffect(() => {
    if (!authenticatedAs) {
      return
    }
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
  }, [project, authenticatedAs])

  const removeAlert = useCallback(() => {
    setAlert(null)
  }, [])

  const toggleFollow = useCallback(() => {
    if (!authenticatedAs) {
      window.location.href = config.getLoginUrl()
      return
    }

    api.follow.change({ enabled: !following }, project).done((follow) => {
      const isFollowing = follow.enabled
      setFollowing(isFollowing)
      setAlert({
        type: isFollowing ? 'success' : 'warning',
        htmlMessage: isFollowing
          ? buildFollowSuccessAlert()
          : followStrings.followingAlert
      })
      if (onFollowChange) {
        onFollowChange(isFollowing)
      }
    })
  }, [authenticatedAs, following, onFollowChange, project])

  useEffect(() => {
    if (onFollowStateChange) {
      onFollowStateChange({ following, toggleFollow })
    }
  }, [following, toggleFollow, onFollowStateChange])

  const followBtnText = following ? followStrings.following : followStrings.follow
  const followDescriptionText = following
    ? followStrings.followingDescription
    : followStrings.followDescription

  const buttonClasses = [
    following ? 'a4-btn a4-btn--following' : 'a4-btn a4-btn--follow',
    buttonClassName
  ]
    .filter(Boolean)
    .join(' ')

  const buttonContent = (
    <span className={'a4-follow ' + customClasses}>
      <button
        className={buttonClasses}
        type="button"
        onClick={toggleFollow}
        aria-describedby={descriptionId}
        aria-pressed={following}
        disabled={following === null && authenticatedAs !== null}
      >
        <span className="a4-follow__btn--content">{followBtnText}</span>
        <span className="a4-sr-only" id={descriptionId}>
          {followDescriptionText}
        </span>
      </button>
    </span>
  )

  const AlertPortal = () => {
    if (!alert) return null

    if (!alertTarget) {
      console.error('AlertPortal: No alert target provided')
      return null
    }

    const container = document.getElementById(alertTarget)

    if (!container) {
      console.error(
        'AlertPortal: Target element with ID "' + alertTarget + '" not found in DOM'
      )
      return null
    }

    return ReactDOM.createPortal(
      <Alert onClick={removeAlert} {...alert} />,
      container
    )
  }

  const alertContent = alertTarget
    ? (
      <AlertPortal />
      )
    : (
      <span className="a4-follow__notification">
        <Alert onClick={removeAlert} {...alert} />
      </span>
      )

  const buttonTargetEl = buttonTarget ? document.getElementById(buttonTarget) : null

  if (buttonTargetEl) {
    return (
      <>
        {ReactDOM.createPortal(buttonContent, buttonTargetEl)}
        {alertContent}
      </>
    )
  }

  return (
    <>
      {buttonContent}
      {alertContent}
    </>
  )
}

export default FollowButton
