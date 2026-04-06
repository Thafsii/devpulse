import Link from 'next/link';

const SOURCE_LABELS = {
    github: '⬡ GitHub',
    hackernews: '▲ HN',
    producthunt: '🔺 PH',
};

export default function UpdateCard({ update, index = 0 }) {
    const sourceLabel = SOURCE_LABELS[update.source] || update.source;
    const date = update.published_at
        ? new Date(update.published_at).toLocaleDateString('en-US', {
            month: 'short', day: 'numeric',
        })
        : '';

    return (
        <article
            className={`card animate-slide-up stagger-${(index % 8) + 1}`}
            id={`update-${update.id}`}
        >
            <div className="card-header">
                <div>
                    <h3 className="card-title">{update.tool_name}</h3>
                    <div className="card-meta">
                        {update.category && (
                            <span className="badge badge-category">{update.category}</span>
                        )}
                        {update.version && (
                            <span className="badge badge-version">v{update.version}</span>
                        )}
                    </div>
                </div>
                <button className="bookmark-btn" title="Bookmark this update">🔖</button>
            </div>

            <div className="card-body">
                <p>{update.summary}</p>
            </div>

            <div className="card-meta" style={{ marginTop: '0.75rem' }}>
                <span className={`source-icon ${update.source}`}>{sourceLabel}</span>
                <span>·</span>
                <span>{date}</span>
                {update.source_url && (
                    <>
                        <span>·</span>
                        <a
                            href={update.source_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            style={{ color: 'var(--accent-indigo)' }}
                        >
                            Source ↗
                        </a>
                    </>
                )}
            </div>

            {update.trend_score > 0 && (
                <div className="trend-bar">
                    <div
                        className="trend-bar-fill"
                        style={{ width: `${Math.min(update.trend_score, 100)}%` }}
                    />
                </div>
            )}
        </article>
    );
}
