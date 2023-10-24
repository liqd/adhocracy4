let following = null

const api = {
  follow: {
    get: jest.fn(() => {
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
    change: jest.fn((enabled) => {
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
