import { useState } from 'react'
import './App.css'
import Feed from './components/Feed'
import Leaderboard from './components/Leaderboard'

function App() {

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Playto Community Feed</h1>
      </header>
      <main className="main-layout">
        <section className="feed-section">
          <Feed />
        </section>
        <aside className="sidebar-section">
          <Leaderboard />
        </aside>
      </main>
    </div>
  )
}

export default App
