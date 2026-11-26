import React from 'react'
import { render } from '@testing-library/react'
import CapCaptcha from '../CapCaptcha'

describe('CapCaptcha', () => {
  test('renders the cap widget with the configured endpoint', () => {
    const { container } = render(
      <CapCaptcha
        endpoint="http://localhost:3000/sitekey/"
        widgetUrl="http://localhost:3000/assets/widget.js"
        name="captcha"
        lang="de"
        onChange={() => {}}
      />
    )

    const widget = container.querySelector('cap-widget')

    expect(widget).toBeInTheDocument()
    expect(widget).toHaveAttribute(
      'data-cap-api-endpoint',
      'http://localhost:3000/sitekey/'
    )
    expect(widget).toHaveAttribute('data-cap-hidden-field-name', 'captcha')
  })
})
