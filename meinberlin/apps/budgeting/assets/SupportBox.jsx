import React, { useState } from 'react'
import django from 'django'

const api = require('adhocracy4').api
const config = require('adhocracy4').config

export const SupportBox = (props) => {
  const [support, setSupport] = useState(props.support)
  const [userSupported, setUserSupported] = useState(props.userSupported)
  const [userSupportId, setUserSupportId] = useState(props.userSupportId)

  const translations = {
    support: django.ngettext(
      'person supports this proposal.',
      'persons support this proposal.',
      props.support
    ),
    clickToSupport: django.gettext('Click to support.'),
    clickToUnsupport: django.gettext('You support this proposal. Click to unsupport.'),
    supportButtonDisabled: django.gettext('Support button inactive.')
  }

  const getSupportClickStr = () => {
    if (props.isReadOnly) {
      return translations.supportButtonDisabled
    }
    return userSupported
      ? translations.clickToUnsupport
      : translations.clickToSupport
  }

  const handleSupportCreate = (value) => {
    api.rating.add({
      urlReplaces: {
        objectPk: props.objectId,
        contentTypeId: props.contentType
      },
      value
    })
      .done((data) => {
        setSupport(data.meta_info.positive_ratings_on_same_object)
        setUserSupported(true)
        setUserSupportId(data.id)
      })
      .fail((xhr, status, err) => {
        if (status === 400 &&
           xhr.responseJSON.length === 1 &&
           Number.isInteger(parseInt(xhr.responseJSON[0]))) {
          setUserSupported(true)
          setUserSupportId(xhr.responseJSON[0])
          handleSupportModify(value, userSupportId)
        }
      })
  }

  const handleSupportModify = (value, id) => {
    api.rating.change({
      urlReplaces: {
        objectPk: props.objectId,
        contentTypeId: props.contentType
      },
      value
    }, id)
      .done((data) => {
        setSupport(data.meta_info.positive_ratings_on_same_object)
        setUserSupported(!userSupported)
      })
  }

  const handleSupport = (e) => {
    if (!props.authenticated) {
      window.location.href = config.getLoginUrl()
      return
    }
    if (props.isReadOnly) {
      e.preventDefault()
      return
    }
    if (userSupportId >= 0) {
      handleSupportModify(+!userSupported, userSupportId)
    } else {
      handleSupportCreate(1)
    }
  }

  const getSupportClass = () => {
    if (props.isArchived) {
      return 'is-archived'
    }
    if (props.isReadOnly) {
      return 'is-read-only'
    }
    if (userSupported) {
      return 'is-selected'
    }
  }

  return (
    <div className="rating">
      <button
        aria-label={support + ' ' + translations.support + ' ' + getSupportClickStr()}
        className={'rating-button rating-up ' + getSupportClass()}
        aria-disabled={props.isReadOnly}
        onClick={handleSupport}
        title={getSupportClickStr()}
      >
        <i className="far fa-thumbs-up" aria-hidden="true" />
        <span aria-hidden="true">{support}</span>
      </button>
    </div>
  )
}
