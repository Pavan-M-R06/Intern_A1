"use client";

import { useState } from "react";
import Link from "next/link";
import { ArrowLeft, Search as SearchIcon, Loader2, Clock, BookOpen, Calendar } from "lucide-react";
import { api } from "@/lib/api";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [searchType, setSearchType] = useState<'concepts' | 'logs'>('concepts');
  const [results, setResults] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResults([]);

    try {
      const response = await api.semanticSearch(query, searchType, 10);
      setResults(response.results || []);
    } catch (err: any) {
      setError(err.message || "Search failed");
    } finally {
      setLoading(false);
    }
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
        <div className="space-y-8">
          {/* Title */}
          <div className="space-y-2">
            <h1 className="text-4xl font-bold gradient-text">Semantic Search</h1>
            <p className="text-muted-foreground">Find concepts and logs using AI-powered semantic search</p>
          </div>

          {/* Search Bar */}
          <div className="card-glass space-y-4">
            {/* Search Type Toggle */}
            <div className="flex items-center gap-2">
              <button
                onClick={() => setSearchType('concepts')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  searchType === 'concepts'
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-muted hover:bg-muted/80'
                }`}
              >
                <BookOpen className="w-4 h-4 inline mr-2" />
                Search Concepts
              </button>
              <button
                onClick={() => setSearchType('logs')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  searchType === 'logs'
                    ? 'bg-primary text-primary-foreground'
                    : 'bg-muted hover:bg-muted/80'
                }`}
              >
                <Calendar className="w-4 h-4 inline mr-2" />
                Search Logs
              </button>
            </div>

            {/* Search Input */}
            <div className="flex gap-3">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                placeholder={searchType === 'concepts' ? "e.g., authentication, async programming..." : "e.g., debugging issues, API development..."}
                className="input flex-1"
              />
              <button
                onClick={handleSearch}
                disabled={loading || !query.trim()}
                className="btn-primary px-6 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <>
                    <SearchIcon className="w-5 h-5" />
                    <span className="ml-2">Search</span>
                  </>
                )}
              </button>
            </div>

            {error && (
              <div className="p-4 rounded-lg bg-destructive/10 border border-destructive/20 text-destructive">
                <p className="text-sm font-medium">{error}</p>
              </div>
            )}
          </div>

          {/* Results */}
          {loading && (
            <div className="card-glass flex items-center justify-center py-12">
              <div className="text-center">
                <Loader2 className="w-12 h-12 animate-spin text-primary mx-auto mb-4" />
                <p className="text-sm text-muted-foreground">Searching with AI...</p>
              </div>
            </div>
          )}

          {results.length > 0 && (
            <div className="space-y-4 animate-in">
              <p className="text-sm text-muted-foreground">
                Found {results.length} result{results.length !== 1 ? 's' : ''} for "{query}"
              </p>

              <div className="grid grid-cols-1 gap-4">
                {results.map((result, i) => (
                  <div key={i} className="card hover:shadow-lg hover:shadow-primary/10 transition-all">
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex-1 space-y-2">
                        {searchType === 'concepts' ? (
                          <>
                            <div className="flex items-center gap-3">
                              <h3 className="text-lg font-semibold">{result.content.name}</h3>
                              {result.content.category && (
                                <span className="px-2 py-1 rounded-md bg-primary/10 text-primary text-xs">
                                  {result.content.category}
                                </span>
                              )}
                            </div>
                            {result.content.definition && (
                              <p className="text-sm text-muted-foreground line-clamp-2">
                                {result.content.definition}
                              </p>
                            )}
                          </>
                        ) : (
                          <>
                            <div className="flex items-center gap-3">
                              <Calendar className="w-4 h-4 text-primary" />
                              <p className="text-sm font-medium">{result.content.log_date}</p>
                            </div>
                            <p className="text-sm text-muted-foreground line-clamp-3">
                              {result.content.summary}
                            </p>
                            {result.content.concepts && result.content.concepts.length > 0 && (
                              <div className="flex flex-wrap gap-2 mt-2">
                                {result.content.concepts.slice(0, 5).map((concept: string, idx: number) => (
                                  <span key={idx} className="px-2 py-1 rounded-md bg-muted text-xs">
                                    {concept}
                                  </span>
                                ))}
                              </div>
                            )}
                          </>
                        )}
                      </div>

                      {/* Similarity Score */}
                      <div className="flex flex-col items-end gap-1">
                        <div className="px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-medium">
                          {(result.score * 100).toFixed(0)}% match
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {!loading && results.length === 0 && query && (
            <div className="card-glass text-center py-12">
              <SearchIcon className="w-16 h-16 mx-auto mb-4 opacity-20" />
              <p className="text-lg font-medium">No results found</p>
              <p className="text-sm text-muted-foreground mt-2">
                Try searching with different keywords
              </p>
            </div>
          )}

          {!query && !loading && (
            <div className="card-glass">
              <div className="flex items-start gap-4">
                <div className="p-3 rounded-lg bg-primary/10">
                  <SearchIcon className="w-6 h-6 text-primary" />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold mb-2">How Semantic Search Works</h3>
                  <p className="text-sm text-muted-foreground mb-4">
                    Unlike keyword search, semantic search understands the meaning behind your query.
                    It finds related concepts and logs even if they don't contain the exact words you searched for.
                  </p>
                  <div className="space-y-2">
                    <p className="text-sm"><span className="text-primary">•</span> Search by concepts, not just keywords</p>
                    <p className="text-sm"><span className="text-primary">•</span> Find similar ideas and related topics</p>
                    <p className="text-sm"><span className="text-primary">•</span> Results ranked by relevance using AI</p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
