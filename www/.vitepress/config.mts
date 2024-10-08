import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'SoundStudio',
  description: 'BGMを直感的に放送しよう。',
  themeConfig: {
    nav: [
      { text: 'ホーム', link: '/' },
      { text: '使い方', link: '/docs/usage.md' },
      { text: '開発者', link: '/docs/developer' },
      { text: 'ライセンス', link: '/docs/license' }
    ],
    sidebar: [
      {
        text: 'ガイド',
        items: [
          { text: 'なにこれ', link: '/docs/features.md' },
          { text: '使い方', link: '/docs/usage.md' },
          { text: '開発者', link: '/docs/developer' },
          { text: 'ライセンス', link: '/docs/license' }
        ]
      }
    ],
    logo: '/logo.png'
  }
})