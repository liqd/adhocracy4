import React, { useState } from 'react'
import django from 'django'

const api = require('adhocracy4').api
const config = require('adhocracy4').config

const translations = {
  support: django.gettext('Click to support')
}

export const SupportBox = (props) => {
  const [support, setSupport] = useState(props.support)
  const [userSupported, setUserSupported] = useState(props.userSupported)
  const [userSupportId, setUserSupportId] = useState(props.userSupportId)

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

  const handleSupport = () => {
    if (!props.authenticated) {
      window.location.href = config.getLoginUrl()
      return
    }
    if (userSupportId >= 0) {
      handleSupportModify(+!userSupported, userSupportId)
    } else {
      handleSupportCreate(1)
    }
  }

  return (
    <div className="rating">
      <button
        aria-label={translations.support}
        className={'rating-button rating-up ' + (userSupported ? 'is-selected' : '')}
        disabled={props.isReadOnly}
        onClick={handleSupport}
      >
        <i className="far fa-thumbs-up" aria-hidden="true" />
        {support}
      </button>
    </div>
  )
}
