"""
DevPulse — Rule-Based Parser
First-pass regex extraction of tool_name and version from raw text.
"""
import re
from typing import Optional


# Common version patterns: v1.2.3, 1.2, V2, etc.
VERSION_PATTERN = re.compile(
    r"""
    (?:v|version\s*)               # prefix: v, V, version
    (\d+(?:\.\d+){0,3})            # major.minor.patch.build
    (?:-[a-zA-Z0-9.]+)?            # optional pre-release suffix
    """,
    re.IGNORECASE | re.VERBOSE,
)

# "ToolName v1.2" or "ToolName 1.2 released"
TOOL_VERSION_PATTERN = re.compile(
    r"""
    ([A-Z][a-zA-Z0-9.]*            # tool name starts with uppercase
    (?:\s[A-Z][a-zA-Z0-9.]*)*)     # optional multi-word
    \s+
    v?(\d+(?:\.\d+){0,3})          # version
    """,
    re.VERBOSE,
)

# Known tool names for exact matching
KNOWN_TOOLS = {
    "react", "next.js", "nextjs", "vue", "angular", "svelte", "sveltekit",
    "nuxt", "astro", "remix", "vite", "webpack", "esbuild", "rollup",
    "bun", "deno", "node", "nodejs", "typescript", "tailwind", "tailwindcss",
    "django", "flask", "fastapi", "express", "nestjs", "spring",
    "docker", "kubernetes", "terraform", "ansible", "jenkins",
    "pytorch", "tensorflow", "langchain", "openai", "huggingface",
    "supabase", "firebase", "prisma", "drizzle", "postgres", "mongodb",
    "redis", "kafka", "elasticsearch", "graphql", "trpc",
    "flutter", "react native", "expo", "kotlin", "swift",
    "rust", "go", "python", "java", "ruby", "php", "elixir", "zig",
}


class ExtractionResult:
    def __init__(
        self,
        tool_name: Optional[str] = None,
        version: Optional[str] = None,
        confidence: float = 0.0,
    ):
        self.tool_name = tool_name
        self.version = version
        self.confidence = confidence

    @property
    def is_complete(self) -> bool:
        return bool(self.tool_name and self.version)

    @property
    def has_tool(self) -> bool:
        return bool(self.tool_name)


def extract(text: str) -> ExtractionResult:
    """
    Attempt to extract tool_name and version using regex patterns.
    Returns ExtractionResult with confidence score.
    """
    if not text:
        return ExtractionResult()

    # Normalize
    text_clean = text.strip()
    text_lower = text_clean.lower()

    tool_name: Optional[str] = None
    version: Optional[str] = None
    confidence = 0.0

    # Strategy 1: known tool name + version pattern
    for known in KNOWN_TOOLS:
        if known in text_lower:
            tool_name = known.title().replace(".", "").replace("Nextjs", "Next.js").replace("Tailwindcss", "Tailwind CSS").replace("Nodejs", "Node.js").replace("Sveltekit", "SvelteKit").replace("Fastapi", "FastAPI").replace("Nestjs", "NestJS").replace("Graphql", "GraphQL").replace("Trpc", "tRPC").replace("Mongodb", "MongoDB").replace("Postgresql", "PostgreSQL").replace("Elasticsearch", "Elasticsearch").replace("Huggingface", "HuggingFace").replace("Langchain", "LangChain").replace("Pytorch", "PyTorch").replace("Tensorflow", "TensorFlow")
            confidence += 0.5
            break

    # Strategy 2: Tool + version pattern match
    tv_match = TOOL_VERSION_PATTERN.search(text_clean)
    if tv_match:
        if not tool_name:
            tool_name = tv_match.group(1).strip()
        version = tv_match.group(2)
        confidence += 0.4

    # Strategy 3: standalone version
    if not version:
        v_match = VERSION_PATTERN.search(text_clean)
        if v_match:
            version = v_match.group(1)
            confidence += 0.2

    return ExtractionResult(tool_name=tool_name, version=version, confidence=min(confidence, 1.0))


def categorize(tool_name: str) -> str:
    """Best-effort category assignment based on known tool mappings."""
    CATEGORY_MAP = {
        "react": "Frontend Framework", "next.js": "Frontend Framework",
        "vue": "Frontend Framework", "angular": "Frontend Framework",
        "svelte": "Frontend Framework", "sveltekit": "Frontend Framework",
        "nuxt": "Frontend Framework", "astro": "Frontend Framework",
        "remix": "Frontend Framework",
        "vite": "Build Tool", "webpack": "Build Tool", "esbuild": "Build Tool",
        "rollup": "Build Tool",
        "bun": "Runtime", "deno": "Runtime", "node.js": "Runtime",
        "typescript": "Language",
        "tailwind css": "CSS Framework",
        "django": "Backend Framework", "flask": "Backend Framework",
        "fastapi": "Backend Framework", "express": "Backend Framework",
        "nestjs": "Backend Framework", "spring": "Backend Framework",
        "docker": "DevOps", "kubernetes": "DevOps", "terraform": "DevOps",
        "ansible": "DevOps", "jenkins": "DevOps",
        "pytorch": "AI/ML", "tensorflow": "AI/ML", "langchain": "AI/ML",
        "openai": "AI/ML", "huggingface": "AI/ML",
        "supabase": "Backend-as-a-Service", "firebase": "Backend-as-a-Service",
        "prisma": "Database", "drizzle": "Database", "postgresql": "Database",
        "mongodb": "Database", "redis": "Database",
        "flutter": "Mobile", "react native": "Mobile", "expo": "Mobile",
        "rust": "Language", "go": "Language", "python": "Language",
        "java": "Language", "ruby": "Language", "php": "Language",
    }
    return CATEGORY_MAP.get(tool_name.lower(), "Other")
