from fastapi import APIRouter, Query
import os
import requests

router = APIRouter(prefix="/videos", tags=["Videos"])


def search_youtube_videos(query: str, max_results: int = 5):
    """البحث عن فيديوهات في YouTube"""
    api_key = os.getenv("YOUTUBE_API_KEY")
    
    # إذا ما في مفتاح، نرجع Mock Data
    if not api_key:
        return [
            {
                "title": f"Learn {query} - Introduction",
                "video_id": "dQw4w9WgXcQ",
                "thumbnail": "https://via.placeholder.com/320x180",
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            },
            {
                "title": f"{query} Tutorial for Beginners",
                "video_id": "dQw4w9WgXcQ",
                "thumbnail": "https://via.placeholder.com/320x180",
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            }
        ]
    
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "maxResults": max_results,
        "type": "video",
        "key": api_key
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code != 200:
            print(f"YouTube API error: {response.text}")
            return []
        
        data = response.json()
        videos = []
        for item in data.get("items", []):
            videos.append({
                "title": item["snippet"]["title"],
                "video_id": item["id"]["videoId"],
                "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            })
        return videos
    except Exception as e:
        print(f"Error fetching videos: {e}")
        return []


@router.get("/search")
def search_videos(
    q: str = Query(..., description="كلمة البحث"),
    max_results: int = Query(5, ge=1, le=20)
):
    """Endpoint للبحث عن الفيديوهات"""
    videos = search_youtube_videos(q, max_results)
    return {
        "query": q,
        "count": len(videos),
        "videos": videos
    }


@router.get("/{topic}")
def get_videos_by_topic(topic: str, max_results: int = 5):
    """جلب فيديوهات حسب الموضوع"""
    videos = search_youtube_videos(topic, max_results)
    return {
        "topic": topic,
        "count": len(videos),
        "videos": videos
    }
