let comments: any = null
let following: { enabled: boolean } | null = null

const api = {
  comments: {
    get: jest.fn(() => {
      const instance = {
        done: (fn: (data: any) => void) => {
          if (comments !== null) {
            fn(comments)
          }
          return instance
        },
        fail: (fn: (err: { status: number }) => void) => {
          if (comments === null) {
            fn({ status: 400 })
          }
          return instance
        }
      }
      return instance
    }),
    setComments: (value: any) => {
      comments = value
    }
  },
  follow: {
    get: jest.fn(() => {
      const instance = {
        done: (fn: (data: { enabled: boolean }) => void) => {
          if (following !== null) {
            fn(following)
          }
          return instance
        },
        fail: (fn: (err: { status: number }) => void) => {
          if (following === null) {
            fn({ status: 400 })
          }
          return instance
        }
      }
      return instance
    }),
    change: jest.fn((enabled: boolean) => {
      following = { enabled }
      const instance = {
        done: (fn: (data: { enabled: boolean }) => void) => {
          if (following !== null) {
            fn(following)
          }
          return instance
        },
        fail: (fn: (err: { status: number }) => void) => {
          if (following === null) {
            fn({ status: 400 })
          }
          return instance
        }
      }
      return instance
    }),
    setFollowing: (value: { enabled: boolean } | null) => {
      following = value
    }
  }
}

export default api
