import * as React from 'react'
import { jest } from '@jest/globals'

jest.createMockFromModule('react-flip-move')

const FlipMove = ({ children }) => <>{children}</>

module.exports = { default: FlipMove }
