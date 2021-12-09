import React from 'react'
import django from 'django'
import CheckboxButton from '../../contrib/assets/CheckboxButton'

export const VoteButton = (props) => {
  return (
    <>
      <CheckboxButton
        onText={django.gettext('Voted')}
        offText={django.gettext('Give my vote')}
        onClass="btn btn--full"
        offClass="btn btn--full btn--light"
        uniqueID={123}
      />
    </>
  )
}
