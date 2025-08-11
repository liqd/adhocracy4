import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import django from 'django';
import Alert from '../../../static/Alert';
import api from '../../../static/api';
import {getLoginUrl} from '../../../static/config';

interface TranslatedTexts {
  followDescription: string;
  followingDescription: string;
  followAlert: string;
  followingAlert: string;
  follow: string;
  following: string;
}

const translated: TranslatedTexts = {
  followDescription: django.gettext(
    'Click to be updated about this project via email.'
  ),
  followingDescription: django.gettext(
    'Click to no longer be updated about this project via email.'
  ),
  followAlert: django.gettext('You will be updated via email.'),
  followingAlert: django.gettext('You will no longer be updated via email.'),
  follow: django.gettext('Follow'),
  following: django.gettext('Following')
};

interface FollowButtonProps {
  project: string;
  authenticatedAs: boolean;
  customClasses?: string;
  alertTarget?: string | null;
}

interface AlertState {
  type: 'success' | 'warning';
  message: string;
}

interface FollowResponse {
  enabled: boolean;
}

export const FollowButton: React.FC<FollowButtonProps> = ({
  project,
  authenticatedAs,
  customClasses = '',
  alertTarget = null
}) => {
  const [following, setFollowing] = useState<boolean | null>(null);
  const [alert, setAlert] = useState<AlertState | null>(null);

  const followBtnText = following ? translated.following : translated.follow;
  const followDescriptionText = following
    ? translated.followingDescription
    : translated.followDescription;

  useEffect(() => {
    if (authenticatedAs) {
      api.follow
        .get(project)
        .done((follow: FollowResponse) => {
          setFollowing(follow.enabled);
        })
        .fail((response: { status: number }) => {
          if (response.status === 404) {
            setFollowing(false);
          }
        });
    }
  }, [project, authenticatedAs]);

  const removeAlert = () => {
    setAlert(null);
  };

  const toggleFollow = () => {
    if (authenticatedAs === null) {
      window.location.href = getLoginUrl();
      return;
    }

    api.follow.change({ enabled: !following }, project).done((follow: FollowResponse) => {
      setFollowing(follow.enabled);
      setAlert({
        type: follow.enabled ? 'success' : 'warning',
        message: follow.enabled ? translated.followAlert : translated.followingAlert
      });
    });
  };

  const buttonClasses = following ? 'a4-btn a4-btn--following' : 'a4-btn a4-btn--follow';

  const AlertPortal: React.FC = () => {
    if (!alert) return null;

    if (!alertTarget) {
      console.error('AlertPortal: No alert target provided');
      return null;
    }

    const container = document.getElementById(alertTarget)

    if (!container) {
      console.error('AlertPortal: Target element with ID "' + alertTarget + '" not found in DOM');
      return null;
    }

    return ReactDOM.createPortal(
      <Alert onClick={removeAlert} {...alert} />,
      container
    );
  };

  return (
    <span className={'a4-follow ' + customClasses}>
      <button
        className={buttonClasses}
        type="button"
        onClick={toggleFollow}
        aria-describedby="follow-description"
        aria-pressed={following || undefined}
        disabled={following === null && authenticatedAs !== null}
      >
        <span className="a4-follow__btn--content">{followBtnText}</span>

        <span className="a4-sr-only" id="follow-description">
          {followDescriptionText}
        </span>
      </button>

      {alertTarget
        ? <AlertPortal />
        : (
          <span className="a4-follow__notification">
            <Alert onClick={removeAlert} {...alert} />
          </span>
        )}
    </span>
  );
};

export default FollowButton;