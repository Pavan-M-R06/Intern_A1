"use client";

import Link from "next/link";
import { useState } from "react";
import {
  BookOpen,
  Brain,
  Calendar,
  FileText,
  Home,
  Search,
  Sparkles,
  TrendingUp,
} from "lucide-react";

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("home");

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="glass border-b border-border sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <Link href="/" className="flex items-center gap-3 group">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-600 to-cyan-500 flex items-center justify-center glow-sm transition-all group-hover:glow">
                <Brain className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold gradient-text">Intern_AI</span>
            </Link>

            {/* Nav Items */}
            <div className="hidden md:flex items-center gap-1">
              <NavItem icon={<Home className="w-4 h-4" />} label="Dashboard" active={activeTab === "home"} onClick={() => setActiveTab("home")} />
              <NavItem icon={<Calendar className="w-4 h-4" />} label="Daily Log" onClick={() => setActiveTab("log")} />
              <NavItem icon={<FileText className="w-4 h-4" />} label="VTU Diary" onClick={() => setActiveTab("diary")} />
              <NavItem icon={<Search className="w-4 h-4" />} label="Search" onClick={() => setActiveTab("search")} />
              <NavItem icon={<TrendingUp className="w-4 h-4" />} label="Analytics" onClick={() => setActiveTab("analytics")} />
            </div>

            {/* CTA */}
            <button className="btn-primary hidden md:flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              <span>Ask AI</span>
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="relative overflow-hidden">
        {/* Background gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 via-background to-cyan-900/20" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(124,58,237,0.1),transparent_50%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_80%,rgba(6,182,212,0.1),transparent_50%)]" />

        <div className="relative max-w-7xl mx-auto px-6 py-20">
          <div className="text-center space-y-6 animate-in">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass border border-primary/30">
              <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
              <span className="text-sm text-muted-foreground">Backend Connected</span>
            </div>

            <h1 className="text-5xl md:text-7xl font-bold">
              <span className="gradient-text">Your AI Learning</span>
              <br />
              <span className="text-foreground">Companion</span>
            </h1>

            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Track your internship journey, generate VTU diary entries, and get personalized AI mentorship - all in one place
            </p>

            <div className="flex items-center justify-center gap-4 pt-4">
              <Link href="/log" className="btn-primary">
                Start Logging
              </Link>
              <Link href="/diary" className="btn-secondary">
                Generate Diary
              </Link>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="max-w-7xl mx-auto px-6 -mt-8 relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <StatCard
            icon={<Calendar className="w-6 h-6" />}
            label="Days Logged"
            value="0"
            trend="+0 this week"
          />
          <StatCard
            icon={<BookOpen className="w-6 h-6" />}
            label="Concepts Learned"
            value="0"
            trend="Ready to start"
          />
          <StatCard
            icon={<FileText className="w-6 h-6" />}
            label="Diary Entries"
            value="0"
            trend="Generate your first"
          />
          <StatCard
            icon={<Sparkles className="w-6 h-6" />}
            label="AI Interactions"
            value="0"
            trend="Ask me anything"
          />
        </div>
      </div>

      {/* Quick Actions */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        <h2 className="text-2xl font-bold mb-6">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <ActionCard
            icon={<Calendar className="w-8 h-8" />}
            title="Add Daily Log"
            description="Record what you learned and did today"
            href="/log"
            color="purple"
          />
          <ActionCard
            icon={<FileText className="w-8 h-8" />}
            title="Generate VTU Diary"
            description="Create professional diary entries instantly"
            href="/diary"
            color="cyan"
          />
          <ActionCard
            icon={<Brain className="w-8 h-8" />}
            title="Ask AI Mentor"
            description="Get personalized explanations and guidance"
            href="/query"
            color="purple"
          />
          <ActionCard
            icon={<Search className="w-8 h-8" />}
            title="Search Memory"
            description="Find concepts and logs with semantic search"
            href="/search"
            color="cyan"
          />
          <ActionCard
            icon={<BookOpen className="w-8 h-8" />}
            title="Explore Concepts"
            description="View all concepts you've learned"
            href="/concepts"
            color="purple"
          />
          <ActionCard
            icon={<TrendingUp className="w-8 h-8" />}
            title="View Analytics"
            description="Track your learning progress and patterns"
            href="/analytics"
            color="cyan"
          />
        </div>
      </div>

      {/* Recent Activity */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        <h2 className="text-2xl font-bold mb-6">Recent Activity</h2>
        <div className="card-glass">
          <div className="text-center py-12 text-muted-foreground">
            <Calendar className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p className="text-lg">No activity yet</p>
            <p className="text-sm mt-2">Start by adding your first daily log!</p>
          </div>
        </div>
      </div>
    </div>
  );
}

// Components
function NavItem({ icon, label, active, onClick }: any) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-2 px-4 py-2 rounded-lg transition-all ${
        active
          ? "bg-primary/10 text-primary"
          : "text-muted-foreground hover:text-foreground hover:bg-muted/50"
      }`}
    >
      {icon}
      <span className="text-sm font-medium">{label}</span>
    </button>
  );
}

function StatCard({ icon, label, value, trend }: any) {
  return (
    <div className="card-glass">
      <div className="flex items-start justify-between">
        <div className="space-y-2">
          <p className="text-sm text-muted-foreground">{label}</p>
          <p className="text-3xl font-bold">{value}</p>
          <p className="text-xs text-muted-foreground">{trend}</p>
        </div>
        <div className="p-3 rounded-lg bg-primary/10 text-primary">{icon}</div>
      </div>
    </div>
  );
}

function ActionCard({ icon, title, description, href, color }: any) {
  const colorClasses = color === "purple" 
    ? "from-purple-600/20 to-purple-600/5 hover:from-purple-600/30 hover:to-purple-600/10 border-purple-500/20 hover:border-purple-500/40"
    : "from-cyan-600/20 to-cyan-600/5 hover:from-cyan-600/30 hover:to-cyan-600/10 border-cyan-500/20 hover:border-cyan-500/40";

  return (
    <Link
      href={href}
      className={`block p-6 rounded-xl border bg-gradient-to-br transition-all duration-200 hover:scale-[1.02] group ${colorClasses}`}
    >
      <div className={`inline-flex p-3 rounded-lg mb-4 ${color === "purple" ? "bg-purple-500/10" : "bg-cyan-500/10"}`}>
        <div className={color === "purple" ? "text-purple-400" : "text-cyan-400"}>{icon}</div>
      </div>
      <h3 className="text-lg font-semibold mb-2 group-hover:text-primary transition-colors">{title}</h3>
      <p className="text-sm text-muted-foreground">{description}</p>
    </Link>
  );
}
