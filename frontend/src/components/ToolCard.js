import Link from 'next/link';

export default function ToolCard({ tool, index = 0 }) {
    const initial = (tool.name || '?')[0].toUpperCase();

    return (
        <Link href={`/tools/${tool.id}`}>
            <article
                className={`card animate-slide-up stagger-${(index % 8) + 1}`}
                id={`tool-${tool.id}`}
            >
                <div className="card-header">
                    <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
                        <div className="tool-icon" style={{ width: 48, height: 48, fontSize: '1.1rem', borderRadius: '0.6rem' }}>
                            {initial}
                        </div>
                        <div>
                            <h3 className="card-title">{tool.name}</h3>
                            <span className="badge badge-category" style={{ marginTop: 4 }}>{tool.category}</span>
                        </div>
                    </div>
                    {tool.trend_score && (
                        <span className="badge badge-trending">🔥 {tool.trend_score}</span>
                    )}
                </div>

                <div className="card-body">
                    <p>{tool.description}</p>
                </div>

                {tool.website && (
                    <div className="card-meta" style={{ marginTop: '0.75rem' }}>
                        <span style={{ color: 'var(--accent-indigo)' }}>{tool.website.replace(/https?:\/\//, '')} ↗</span>
                    </div>
                )}
            </article>
        </Link>
    );
}
