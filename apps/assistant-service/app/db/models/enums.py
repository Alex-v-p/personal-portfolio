from enum import Enum


class AssistantRole(str, Enum):
    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'


class EventType(str, Enum):
    PAGE_VIEW = 'page_view'
    PORTFOLIO_LIKE = 'portfolio_like'
    BLOG_VIEW = 'blog_view'
    PROJECT_CLICK = 'project_click'
    CONTACT_SUBMIT = 'contact_submit'
    ASSISTANT_MESSAGE = 'assistant_message'


class KnowledgeSourceType(str, Enum):
    PROFILE = 'profile'
    PROJECT = 'project'
    BLOG_POST = 'blog_post'
    EXPERIENCE = 'experience'
    ASSISTANT_NOTE = 'assistant_note'
