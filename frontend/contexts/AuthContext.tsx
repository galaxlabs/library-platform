'use client';

import { createContext, useContext, useEffect, useMemo, useState } from 'react';

import api from '../lib/api';

export interface User {
  id: number;
  public_id?: string;
  email: string;
  full_name: string;
  arabic_name?: string;
  preferred_lang_pair?: string;
  institute_name?: string;
  institute_public_id?: string;
  class_darjah_name?: string;
  membership_roles?: string[];
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<User>;
  register: (payload: Record<string, unknown>) => Promise<User>;
  refreshMe: () => Promise<User | null>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const persistAuth = (nextUser: User, access: string, refresh: string) => {
    window.localStorage.setItem('access_token', access);
    window.localStorage.setItem('refresh_token', refresh);
    window.localStorage.setItem('user', JSON.stringify(nextUser));
    setUser(nextUser);
  };

  const login = async (email: string, password: string) => {
    const response = await api.post('/auth/login/', { email, password });
    const nextUser = response.data.user as User;
    persistAuth(nextUser, response.data.tokens.access, response.data.tokens.refresh);
    return nextUser;
  };

  const register = async (payload: Record<string, unknown>) => {
    const response = await api.post('/auth/register/', payload);
    const nextUser = response.data.user as User;
    persistAuth(nextUser, response.data.tokens.access, response.data.tokens.refresh);
    return nextUser;
  };

  const refreshMe = async () => {
    try {
      const response = await api.get('/accounts/me/');
      setUser(response.data);
      window.localStorage.setItem('user', JSON.stringify(response.data));
      return response.data;
    } catch {
      setUser(null);
      window.localStorage.removeItem('user');
      return null;
    }
  };

  const logout = () => {
    setUser(null);
    window.localStorage.removeItem('access_token');
    window.localStorage.removeItem('refresh_token');
    window.localStorage.removeItem('user');
  };

  useEffect(() => {
    const bootstrap = async () => {
      const storedUser = window.localStorage.getItem('user');
      const accessToken = window.localStorage.getItem('access_token');

      if (storedUser) {
        try {
          setUser(JSON.parse(storedUser));
        } catch {
          window.localStorage.removeItem('user');
        }
      }

      if (!accessToken) {
        setLoading(false);
        return;
      }

      await refreshMe();
      setLoading(false);
    };

    bootstrap();
  }, []);

  const value = useMemo(
    () => ({
      user,
      loading,
      isAuthenticated: !!user,
      login,
      register,
      refreshMe,
      logout,
    }),
    [loading, user]
  );

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
