"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowLeft, FileText, Calendar, Download, Loader2, Sparkles } from "lucide-react";
import { api } from "@/lib/api";

export default function DiaryPage() {
  const [mode, setMode] = useState<'daily' | 'weekly' | 'monthly'>('weekly');
  const [startDate, setStartDate] = useState(new Date().toISOString().split('T')[0]);
  const [endDate, setEndDate] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    setSummary('');

    try {
      const result = await api.generateSummary({
        mode,
        start_date: startDate,
        end_date: endDate || undefined,
      });
      setSummary(result.summary);
    } catch (err: any) {
      setError(err.message || 'Failed to generate summary');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(summary);
    alert('Copied to clipboard!');
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="glass border-b border-border sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <Link href="/" className="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Dashboard</span>
          </Link>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto px-6 py-12">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Settings Panel */}
          <div className="lg:col-span-1 space-y-6">
            <div className="space-y-2">
              <h1 className="text-3xl font-bold gradient-text">VTU Diary Generator</h1>
              <p className="text-sm text-muted-foreground">Generate professional diary entries instantly</p>
            </div>

            <div className="card-glass space-y-6">
              {/* Mode Selection */}
              <div className="space-y-3">
                <label className="text-sm font-medium">Summary Type</label>
                <div className="grid grid-cols-3 gap-2">
                  <button
                    onClick={() => setMode('daily')}
                    className={`py-2 px-3 rounded-lg text-sm font-medium transition-all ${
                      mode === 'daily'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-muted hover:bg-muted/80'
                    }`}
                  >
                    Daily
                  </button>
                  <button
                    onClick={() => setMode('weekly')}
                    className={`py-2 px-3 rounded-lg text-sm font-medium transition-all ${
                      mode === 'weekly'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-muted hover:bg-muted/80'
                    }`}
                  >
                    Weekly
                  </button>
                  <button
                    onClick={() => setMode('monthly')}
                    className={`py-2 px-3 rounded-lg text-sm font-medium transition-all ${
                      mode === 'monthly'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-muted hover:bg-muted/80'
                    }`}
                  >
                    Monthly
                  </button>
                </div>
              </div>

              {/* Date Range */}
              <div className="space-y-3">
                <label className="flex items-center gap-2 text-sm font-medium">
                  <Calendar className="w-4 h-4" />
                  Start Date
                </label>
                <input
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  className="input"
                />
              </div>

              {mode !== 'daily' && (
                <div className="space-y-3">
                  <label className="text-sm font-medium">End Date (Optional)</label>
                  <input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    className="input"
                  />
                  <p className="text-xs text-muted-foreground">
                    Leave empty to auto-calculate based on mode
                  </p>
                </div>
              )}

              {/* Generate Button */}
              <button
                onClick={handleGenerate}
                disabled={loading || !startDate}
                className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>Generating with AI...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    <span>Generate Summary</span>
                  </>
                )}
              </button>

              {/* Info Box */}
              <div className="p-4 rounded-lg bg-primary/10 border border-primary/20">
                <p className="text-xs text-primary font-medium mb-1">✨ AI-Powered</p>
                <p className="text-xs text-muted-foreground">
                  Uses your real logged data to create authentic, professional diary entries
                </p>
              </div>
            </div>
          </div>

          {/* Preview Panel */}
          <div className="lg:col-span-2">
            <div className="card-glass min-h-[600px] flex flex-col">
              <div className="flex items-center justify-between mb-6 pb-4 border-b border-border">
                <h2 className="text-xl font-semibold flex items-center gap-2">
                  <FileText className="w-5 h-5 text-primary" />
                  Generated Summary
                </h2>
                {summary && (
                  <div className="flex items-center gap-2">
                    <button
                      onClick={copyToClipboard}
                      className="btn-ghost px-4 py-2 text-sm"
                    >
                      Copy
                    </button>
                    <button className="btn-secondary px-4 py-2 text-sm flex items-center gap-2">
                      <Download className="w-4 h-4" />
                      Export PDF
                    </button>
                  </div>
                )}
              </div>

              {/* Content */}
              <div className="flex-1">
                {error && (
                  <div className="p-4 rounded-lg bg-destructive/10 border border-destructive/20 text-destructive">
                    <p className="text-sm font-medium">{error}</p>
                  </div>
                )}

                {!summary && !loading && !error && (
                  <div className="h-full flex flex-col items-center justify-center text-center text-muted-foreground">
                    <FileText className="w-16 h-16 mb-4 opacity-20" />
                    <p className="text-lg font-medium">No summary generated yet</p>
                    <p className="text-sm mt-2">Select dates and click generate to create your VTU diary entry</p>
                  </div>
                )}

                {loading && (
                  <div className="h-full flex flex-col items-center justify-center">
                    <Loader2 className="w-12 h-12 animate-spin text-primary mb-4" />
                    <p className="text-sm text-muted-foreground">AI is generating your summary...</p>
                  </div>
                )}

                {summary && (
                  <div className="space-y-4 animate-in">
                    {/* Metadata */}
                    <div className="p-4 rounded-lg bg-muted/50 border border-border">
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <p className="text-muted-foreground">Type</p>
                          <p className="font-medium capitalize">{mode}</p>
                        </div>
                        <div>
                          <p className="text-muted-foreground">Date</p>
                          <p className="font-medium">{startDate}</p>
                        </div>
                      </div>
                    </div>

                    {/* Summary Text */}
                    <div className="prose prose-invert max-w-none">
                      <div className="whitespace-pre-wrap leading-relaxed text-foreground">
                        {summary}
                      </div>
                    </div>

                    {/* Word Count */}
                    <div className="pt-4 border-t border-border">
                      <p className="text-xs text-muted-foreground">
                        Word Count: {summary.split(/\s+/).length} words
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
