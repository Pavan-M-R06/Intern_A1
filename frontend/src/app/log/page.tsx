"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Calendar, ArrowLeft, Loader2, Brain, CheckCircle } from "lucide-react";
import { api } from "@/lib/api";

export default function DailyLogPage() {
  const router = useRouter();
  const [logDate, setLogDate] = useState(new Date().toISOString().split('T')[0]);
  const [rawText, setRawText] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [extractedData, setExtractedData] = useState<any>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccess(false);

    try {
      const result = await api.createDailyLog(logDate, rawText);
      setExtractedData(result.structured_data);
      setSuccess(true);
      
      // Reset form after 2 seconds
      setTimeout(() => {
        setRawText("");
        setExtractedData(null);
        setSuccess(false);
      }, 3000);
    } catch (err: any) {
      setError(err.message || "Failed to create log");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="glass border-b border-border sticky top-0 z-50">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <Link href="/" className="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
            <ArrowLeft className="w-4 h-4" />
            <span>Back to Dashboard</span>
          </Link>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-6 py-12">
        <div className="space-y-8">
          {/* Title */}
          <div className="space-y-2">
            <h1 className="text-4xl font-bold gradient-text">Daily Log Entry</h1>
            <p className="text-muted-foreground">Record what you learned and did today. AI will extract structured data automatically.</p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Date Picker */}
            <div className="card-glass space-y-3">
              <label className="flex items-center gap-2 text-sm font-medium">
                <Calendar className="w-4 h-4" />
                Date
              </label>
              <input
                type="date"
                value={logDate}
                onChange={(e) => setLogDate(e.target.value)}
                className="input"
                required
              />
            </div>

            {/* Text Input */}
            <div className="card-glass space-y-3">
              <label className="flex items-center gap-2 text-sm font-medium">
                <Brain className="w-4 h-4" />
                What did you learn and do today?
              </label>
              <textarea
                value={rawText}
                onChange={(e) => setRawText(e.target.value)}
                className="textarea min-h-[300px]"
                placeholder="Example: Today I learned FastAPI routing and created 2 REST endpoints. My mentor assigned me to implement JWT authentication. I struggled with async/await but figured it out. Spent 4 hours coding..."
                required
              />
              <p className="text-xs text-muted-foreground">
                Write freely! The AI will automatically extract:
                <span className="block mt-1">• Concepts learned • Activities • Assignments • Mood • Difficulty level</span>
              </p>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading || !rawText.trim()}
              className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Processing with AI...</span>
                </>
              ) : success ? (
                <>
                  <CheckCircle className="w-5 h-5" />
                  <span>Log Saved!</span>
                </>
              ) : (
                <span>Save Daily Log</span>
              )}
            </button>

            {/* Error Message */}
            {error && (
              <div className="p-4 rounded-lg bg-destructive/10 border border-destructive/20 text-destructive">
                <p className="text-sm font-medium">{error}</p>
              </div>
            )}
          </form>

          {/* Extracted Data Preview */}
          {extractedData && (
            <div className="card-glass space-y-4 animate-in">
              <h3 className="text-lg font-semibold flex items-center gap-2">
                <Brain className="w-5 h-5 text-primary" />
                AI Extracted Data
              </h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Concepts */}
                {extractedData.concepts && extractedData.concepts.length > 0 && (
                  <div className="p-4 rounded-lg bg-purple-500/10 border border-purple-500/20">
                    <p className="text-sm font-medium text-purple-400 mb-2">Concepts Learned</p>
                    <div className="flex flex-wrap gap-2">
                      {extractedData.concepts.map((concept: string, i: number) => (
                        <span key={i} className="px-2 py-1 rounded-md bg-purple-500/20 text-xs">
                          {concept}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Mood & Difficulty */}
                <div className="p-4 rounded-lg bg-cyan-500/10 border border-cyan-500/20">
                  <p className="text-sm font-medium text-cyan-400 mb-2">Metrics</p>
                  <div className="space-y-1 text-sm">
                    {extractedData.mood && <p>Mood: <span className="text-foreground capitalize">{extractedData.mood}</span></p>}
                    {extractedData.difficulty_level && <p>Difficulty: <span className="text-foreground capitalize">{extractedData.difficulty_level}</span></p>}
                  </div>
                </div>
              </div>

              {/* Activities */}
              {extractedData.activities && extractedData.activities.length > 0 && (
                <div className="p-4 rounded-lg bg-muted/50">
                  <p className="text-sm font-medium mb-2">Activities</p>
                  <ul className="space-y-2">
                    {extractedData.activities.map((activity: any, i: number) => (
                      <li key={i} className="text-sm flex items-start gap-2">
                        <span className="text-primary">•</span>
                        <span>{activity.description} {activity.duration_minutes && `(${activity.duration_minutes}min)`}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
