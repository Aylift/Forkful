import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createTestingPinia } from '@pinia/testing'
import AppLogin from './AppLogin.vue'
import { useAuthStore } from '@/stores/auth'


const mockRouter = {
  push: vi.fn()
}
vi.mock('vue-router', () => ({
  useRouter: () => mockRouter
}))

describe('AppLogin.vue', () => {

  beforeEach(() => {
    mockRouter.push.mockClear()
    vi.useRealTimers()
  })

  it('calls auth.login on button click and redirects on success', async () => {
    vi.useFakeTimers()
    const wrapper = mount(AppLogin, {
      global: {
        plugins: [
          createTestingPinia({
            stubActions: false,
            createSpy: vi.fn, 
          }),
        ],
      },
    })
    
    const auth = useAuthStore()

    auth.login = vi.fn(() => Promise.resolve({ success: true }))
    auth.token = 'fake-token'

    await wrapper.find('input[placeholder="Username"]').setValue('testuser')
    await wrapper.find('input[placeholder="Password"]').setValue('password')
    await wrapper.find('button').trigger('click')
    
    expect(auth.clearError).toHaveBeenCalledOnce()
    expect(auth.login).toHaveBeenCalledWith('testuser', 'password')

    await flushPromises()

    expect(wrapper.text()).toContain('Logged in successfully! Redirecting...')

    vi.advanceTimersByTime(1500)
    await flushPromises()

    expect(mockRouter.push).toHaveBeenCalledWith('/profile')
  })

  it('shows an error message on login failure', async () => {
    const wrapper = mount(AppLogin, {
      global: {
        plugins: [ createTestingPinia({ createSpy: vi.fn }) ],
      },
    })

    const auth = useAuthStore()
    
    auth.login = vi.fn(() => Promise.resolve({ success: false }))
    auth.error = { detail: 'Wrong username or password' }

    await wrapper.find('button').trigger('click')
    await flushPromises()

    expect(wrapper.text()).toContain('Wrong username or password')
    expect(wrapper.text()).not.toContain('Logged in successfully!')
    expect(mockRouter.push).not.toHaveBeenCalled()
  })
})