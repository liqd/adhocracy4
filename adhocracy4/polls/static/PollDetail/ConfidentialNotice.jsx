import React from 'react'
import django from 'django'

export const ConfidentialNotice = () => (
  <p className="poll__confidential-notice a4-muted">
    {django.gettext(
      'Your response will be kept confidential and will not be publicly displayed.'
    )}
  </p>
)
