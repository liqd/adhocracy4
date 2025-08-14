import { vi } from 'vitest'

let comments = null
let following = null

const api = {
  comments: {
    get: vi.fn(() => {
      const instance = {
        done: (fn) => {
          if (comments !== null) {
            fn(comments)
          }
          return instance
        },
        fail: (fn) => {
          if (comments === null) {
            fn({ status: 400 })
          }
          return instance
        }
      }
      return instance
    }),
    setComments: (value) => {
      comments = value
    }
  },
  follow: {
    get: vi.fn(() => {
      const instance = {
        done: (fn) => {
          if (following !== null) {
            fn(following)
          }
          return instance
        },
        fail: (fn) => {
          if (following === null) {
            fn({ status: 400 })
          }
          return instance
        }
      }
      return instance
    }),
    change: vi.fn((enabled) => {
      following = { enabled }
      const instance = {
        done: (fn) => {
          if (following !== null) {
            fn(following)
          }
          return instance
        },
        fail: (fn) => {
          if (following === null) {
            fn({ status: 400 })
          }
          return instance
        }
      }
      return instance
    }),
    setFollowing: (value) => {
      following = value
    }
  }
}

module.exports = api
