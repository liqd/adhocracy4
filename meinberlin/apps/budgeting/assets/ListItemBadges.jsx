import React from 'react'
import django from 'django'

const translated = {
  more: django.gettext('More')
}

export const ListItemBadges = props => {
  // combine css class names to match different styling, depending
  // on if it is moderator_status or on of the others (category, label etc.)
  const getClass = (badge) => {
    const labelClass = 'label label--big'
    if (badge[0] !== 'moderator_status') {
      return labelClass
    }
    const modTypeClass = 'label--' + badge[2].toLowerCase()
    return labelClass + ' ' + modTypeClass
  }

  // only return icon for pointLabels
  const hasPointLabelIcon = (type) => {
    if (type !== 'point_label') {
      return
    }
    return <i className="fas fa-map-marker-alt u-icon-spacing" aria-hidden="true" />
  }

  return (
    <div className="list-item__labels">
      {props.badges.map((badge, idx) => {
        return (
          <div
            key={'badge_' + idx}
            className={getClass(badge)}
          >
            {hasPointLabelIcon(badge[0])}
            {badge[1]}
          </div>
        )
      })}
      {props.numOfMoreBadges > 0 &&
        <div className="label__link label--big">
          <a
            href={props.proposalUrl}
            className="list-item__link"
          >
            {props.numOfMoreBadges + ' ' + translated.more}
          </a>
        </div>}
    </div>
  )
}
