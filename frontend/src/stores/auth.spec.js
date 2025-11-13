import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from './auth'
import api from '@/axios'

beforeEach(() => {
  vi.clearAllMocks()
  setActivePinia(createPinia())
  localStorage.clear()
})

describe('Auth Store', () => {
  it('initial state is correct (not authenticated)', () => {
    const auth = useAuthStore()
    expect(auth.token).toBe(null)
    expect(auth.user).toBe(null)
    expect(auth.isAuthenticated).toBe(false)
  })

  it('login action successfully logs in a user', async () => {
    const auth = useAuthStore()
    
    const mockToken = 'fake-access-token'
    const mockUser = { user: { username: 'testuser' } }
    
    api.post.mockResolvedValue({ data: { access: mockToken } })
    api.get.mockResolvedValue({ data: mockUser })

    const result = await auth.login('testuser', 'password')

    expect(result.success).toBe(true)
    expect(auth.token).toBe(mockToken)
    expect(auth.user).toEqual(mockUser)
    expect(auth.isAuthenticated).toBe(true)
    expect(localStorage.getItem('token')).toBe(mockToken)
    expect(api.post).toHaveBeenCalledWith('/api/auth/login/', {
      username: 'testuser',
      password: 'password'
    })
    expect(api.get).toHaveBeenCalledWith('/api/auth/check/')
  })

  it('login action handles failure', async () => {
    const auth = useAuthStore()
    
    const mockError = { detail: 'No active account found with given credentials' }
    api.post.mockRejectedValue({ response: { data: mockError } })

    const result = await auth.login('wrong', 'user')

    expect(result.success).toBe(false)
    expect(auth.token).toBe(null)
    expect(auth.isAuthenticated).toBe(false)
    expect(auth.error).toEqual(mockError)
    expect(localStorage.getItem('token')).toBe(null)
  })
  
  it('logout action clears state and localStorage', async () => {
    const auth = useAuthStore()
    auth.token = 'fake-token'
    auth.user = { user: { username: 'testuser' } }
    localStorage.setItem('token', 'fake-token')

    auth.logout()

    expect(auth.token).toBe(null)
    expect(auth.user).toBe(null)
    expect(auth.isAuthenticated).toBe(false)
    expect(localStorage.getItem('token')).toBe(null)
  })
})