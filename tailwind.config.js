const { fontFamily } = require('tailwindcss/defaultTheme')

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/*.html'
  ],
  safelist: [
    'bg-gradient-to-b',
    'bg-gradient-to-r',
    'bg-gradient-to-br',
    'from-blue-600',
    'from-blue-700',
    'from-blue-800',
    'from-slate-50',
    'from-slate-100',
    'from-white',
    'via-blue-700',
    'to-blue-50',
    'to-blue-800',
    'to-blue-900',
    'to-slate-50',
    'to-white',
    'bg-blue-600',
    'bg-blue-700',
    'bg-blue-800',
    'bg-blue-900',
    'text-white',
    'text-white/90',
    'text-white/95',
    'text-slate-700',
    'text-slate-900',
    'bg-white/10',
    'bg-white/20',
    'bg-blue-800/50',
    'bg-blue-900/95',
    'border-blue-600',
    'border-blue-600/50',
    'border-blue-700/50',
    'border-t-4',
    'border-t-blue-600',
    'border-l-2',
    'border-l-blue-600/50',
    'border-r-2',
    'border-r-blue-600/50',
    'border-b-2',
    'border-b-blue-600/50',
    'backdrop-blur-sm',
    'tracking-wider',
    'tracking-tight',
    'font-extrabold',
    'shadow-2xl',
    'hover:shadow-blue-600/20',
    'rounded-xl',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['"Inter"', ...fontFamily.sans],
        headings: ['"Poppins"', ...fontFamily.sans],
      },
      colors: {
        slate: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
        blue: {
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        indigo: {
          900: '#312e81',
        },
        emerald: {
          500: '#10b981',
        },
        amber: {
          500: '#f59e0b',
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}