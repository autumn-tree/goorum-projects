from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
from urllib.parse import parse_qs, urlparse

import requests


class ThumbnailExtractionError(ValueError):
    """Raised when a thumbnail cannot be extracted from a provided URL."""


@dataclass(frozen=True)
class ThumbnailCandidate:
    quality: str
    url: str


YOUTUBE_THUMBNAIL_QUALITIES: tuple[str, ...] = (
    "maxresdefault",
    "hqdefault",
    "mqdefault",
    "default",
)

YOUTUBE_HOSTS: tuple[str, ...] = (
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "youtu.be",
    "www.youtu.be",
)


def _is_valid_video_id(video_id: str) -> bool:
    if len(video_id) != 11:
        return False
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-")
    return all(char in allowed for char in video_id)


def extract_video_id_from_url(url: str) -> str:
    """Extract a YouTube video ID from watch/youtu.be/shorts URL formats."""
    parsed = urlparse(url.strip())
    host = parsed.netloc.lower()
    path = parsed.path.strip("/")

    if host not in YOUTUBE_HOSTS:
        raise ThumbnailExtractionError("Unsupported domain. Use a YouTube URL.")

    video_id = ""
    if host.endswith("youtu.be"):
        video_id = path.split("/")[0] if path else ""
    elif path == "watch":
        query_video_id = parse_qs(parsed.query).get("v", [])
        video_id = query_video_id[0] if query_video_id else ""
    elif path.startswith("shorts/"):
        video_id = path.split("/", maxsplit=1)[1].split("/")[0]

    if not _is_valid_video_id(video_id):
        raise ThumbnailExtractionError(
            "Could not extract a valid YouTube video ID from the URL."
        )
    return video_id


def build_thumbnail_candidates(video_id: str) -> list[ThumbnailCandidate]:
    """Build prioritized YouTube thumbnail URL candidates for a video ID."""
    if not _is_valid_video_id(video_id):
        raise ThumbnailExtractionError("Invalid video ID format.")
    return [
        ThumbnailCandidate(
            quality=quality,
            url=f"https://img.youtube.com/vi/{video_id}/{quality}.jpg",
        )
        for quality in YOUTUBE_THUMBNAIL_QUALITIES
    ]


def is_thumbnail_available(
    candidate: ThumbnailCandidate,
    session: requests.Session | None = None,
    timeout: float = 5.0,
) -> bool:
    """Check whether the thumbnail URL is reachable and returns an image response."""
    http = session or requests.Session()
    try:
        response = http.head(candidate.url, allow_redirects=True, timeout=timeout)
        if response.status_code >= 400:
            return False
        content_type = response.headers.get("Content-Type", "")
        return "image" in content_type.lower() if content_type else True
    except requests.RequestException:
        return False


def resolve_best_thumbnail(
    video_id: str,
    session: requests.Session | None = None,
    timeout: float = 5.0,
    checker: Callable[[ThumbnailCandidate], bool] | None = None,
) -> ThumbnailCandidate:
    """Resolve the best available thumbnail candidate in fallback order."""
    candidates = build_thumbnail_candidates(video_id)
    availability_checker = checker or (
        lambda candidate: is_thumbnail_available(
            candidate=candidate,
            session=session,
            timeout=timeout,
        )
    )
    for candidate in candidates:
        if availability_checker(candidate):
            return candidate
    raise ThumbnailExtractionError("No available thumbnail was found for this video.")


def extract_thumbnail_from_url(
    url: str,
    session: requests.Session | None = None,
    timeout: float = 5.0,
    checker: Callable[[ThumbnailCandidate], bool] | None = None,
) -> tuple[str, ThumbnailCandidate]:
    """Extract video ID and resolve the best thumbnail candidate from a YouTube URL."""
    video_id = extract_video_id_from_url(url)
    best = resolve_best_thumbnail(
        video_id=video_id,
        session=session,
        timeout=timeout,
        checker=checker,
    )
    return video_id, best


def fetch_thumbnail_bytes(
    thumbnail_url: str,
    session: requests.Session | None = None,
    timeout: float = 10.0,
) -> bytes:
    """Fetch thumbnail bytes to support Streamlit download buttons."""
    http = session or requests.Session()
    response = http.get(thumbnail_url, timeout=timeout)
    response.raise_for_status()
    return response.content
