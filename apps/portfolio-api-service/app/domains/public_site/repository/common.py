from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Literal

from sqlalchemy import select

from app.db.models import BlogPost, MediaFile, Project, ProjectState, PublicationStatus
from app.domains.public_site.schema import PublicMediaAssetOut
from app.domains.media.resolver import PublicMediaUrlResolver

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


PublicLocale = Literal['en', 'nl']
DEFAULT_PUBLIC_LOCALE: PublicLocale = 'en'

_PUBLIC_COPY: dict[PublicLocale, dict[str, str]] = {
    'en': {
        'avatar_suffix': 'avatar',
        'hero_image_suffix': 'hero image',
        'resume_suffix': 'resume',
        'availability_internships': 'Open to internships',
        'availability_remote': 'Remote friendly',
        'availability_portfolio': 'Portfolio projects',
        'availability_jobs': 'Job opportunities',
        'availability_meeting': 'Scheduling a meeting',
        'contact_email_label': 'Email',
        'contact_email_action': 'Send Email',
        'contact_email_description': 'Best for project enquiries, internships, and collaboration.',
        'contact_phone_label': 'Phone',
        'contact_phone_action': 'Call',
        'contact_phone_description': 'Useful for quick coordination or planning a meeting.',
        'contact_social_action_connect': 'Connect',
        'contact_social_action_open': 'Open',
        'contact_social_description_github': 'Code samples, experiments, and project work.',
        'contact_social_description_linkedin': 'Professional background and experience.',
        'contact_social_description_default': 'Direct line for portfolio contact.',
        'contact_location_label': 'Location',
        'contact_location_action': 'View Map',
        'contact_location_description': 'Available for on-site, hybrid, or remote collaboration.',
        'years_suffix': 'y',
        'stats_label_public_repos': 'Public repos',
        'stats_description_public_repos': 'Public repositories currently visible on GitHub.',
        'stats_meta_latest_snapshot': '{username} · latest snapshot',
        'stats_meta_no_snapshot': 'No snapshot available',
        'stats_footnote_total_commits': '{count} total commits',
        'stats_footnote_github_unavailable': 'GitHub snapshot not available',
        'stats_label_unique_views': 'Unique views',
        'stats_description_unique_views': 'Distinct visitors/sessions recorded across the public portfolio.',
        'stats_label_likes': 'Like counter',
        'stats_description_likes': 'Visitors who tapped the portfolio like button.',
        'stats_action_like': 'Love this portfolio',
        'stats_label_projects': 'Projects',
        'stats_description_projects': 'Published portfolio projects.',
        'stats_label_posts': 'Blog posts',
        'stats_description_posts': 'Posts available on the public blog.',
        'stats_label_featured_projects': 'Featured projects',
        'stats_description_featured_projects': 'Projects currently highlighted on the portfolio.',
        'stats_label_featured_posts': 'Featured posts',
        'stats_description_featured_posts': 'Blog posts currently featured for discovery.',
        'stats_label_skills': 'Skills',
        'stats_description_skills': 'Skills currently modeled in the portfolio.',
        'stats_label_experience': 'Experience entries',
        'stats_description_experience': 'Experience timeline rows available publicly.',
    },
    'nl': {
        'avatar_suffix': 'profielfoto',
        'hero_image_suffix': 'hero-afbeelding',
        'resume_suffix': 'cv',
        'availability_internships': 'Open voor stages',
        'availability_remote': 'Remote vriendelijk',
        'availability_portfolio': 'Portfolio-projecten',
        'availability_jobs': 'Jobkansen',
        'availability_meeting': 'Een gesprek inplannen',
        'contact_email_label': 'E-mail',
        'contact_email_action': 'E-mail sturen',
        'contact_email_description': 'Ideaal voor projectvragen, stages en samenwerking.',
        'contact_phone_label': 'Telefoon',
        'contact_phone_action': 'Bellen',
        'contact_phone_description': 'Handig voor snelle afstemming of het plannen van een gesprek.',
        'contact_social_action_connect': 'Verbinden',
        'contact_social_action_open': 'Openen',
        'contact_social_description_github': 'Codevoorbeelden, experimenten en projectwerk.',
        'contact_social_description_linkedin': 'Professionele achtergrond en ervaring.',
        'contact_social_description_default': 'Rechtstreeks contact via mijn portfolio.',
        'contact_location_label': 'Locatie',
        'contact_location_action': 'Kaart bekijken',
        'contact_location_description': 'Beschikbaar voor samenwerking op locatie, hybride of remote.',
        'years_suffix': 'j',
        'stats_label_public_repos': 'Publieke repositories',
        'stats_description_public_repos': 'Publieke repositories die momenteel zichtbaar zijn op GitHub.',
        'stats_meta_latest_snapshot': '{username} · nieuwste snapshot',
        'stats_meta_no_snapshot': 'Geen snapshot beschikbaar',
        'stats_footnote_total_commits': '{count} commits in totaal',
        'stats_footnote_github_unavailable': 'GitHub-snapshot niet beschikbaar',
        'stats_label_unique_views': 'Unieke weergaven',
        'stats_description_unique_views': 'Unieke bezoekers of sessies die op het publieke portfolio zijn geregistreerd.',
        'stats_label_likes': 'Like-teller',
        'stats_description_likes': 'Bezoekers die op de portfolio-like-knop hebben gedrukt.',
        'stats_action_like': 'Geef dit portfolio liefde',
        'stats_label_projects': 'Projecten',
        'stats_description_projects': 'Gepubliceerde portfolio-projecten.',
        'stats_label_posts': 'Blogposts',
        'stats_description_posts': 'Berichten die beschikbaar zijn op de publieke blog.',
        'stats_label_featured_projects': 'Uitgelichte projecten',
        'stats_description_featured_projects': 'Projecten die momenteel worden uitgelicht op het portfolio.',
        'stats_label_featured_posts': 'Uitgelichte blogposts',
        'stats_description_featured_posts': 'Blogposts die momenteel worden uitgelicht om ontdekt te worden.',
        'stats_label_skills': 'Vaardigheden',
        'stats_description_skills': 'Vaardigheden die momenteel in het portfolio zijn gemodelleerd.',
        'stats_label_experience': 'Ervaringsitems',
        'stats_description_experience': 'Ervaringstijdlijn-items die publiek beschikbaar zijn.',
    },
}


class PublicRepositoryCommonMixin:
    session: Session
    media_resolver: PublicMediaUrlResolver
    locale: PublicLocale

    @staticmethod
    def _publication_cutoff() -> datetime:
        return datetime.now(UTC)

    def _public_project_query(self):
        return select(Project).where(
            Project.state != ProjectState.ARCHIVED,
            Project.published_at <= self._publication_cutoff(),
        )

    def _public_blog_post_query(self):
        return select(BlogPost).where(
            BlogPost.status == PublicationStatus.PUBLISHED,
            BlogPost.published_at.is_not(None),
            BlogPost.published_at <= self._publication_cutoff(),
        )

    def _map_media(self, media_file: MediaFile | None, alt: str | None = None) -> PublicMediaAssetOut | None:
        url = self.media_resolver.resolve(media_file)
        if media_file is None or url is None:
            return None
        return PublicMediaAssetOut(
            id=str(media_file.id),
            url=url,
            download_url=self.media_resolver.resolve_download(media_file),
            alt=alt or media_file.alt_text,
            file_name=media_file.original_filename,
            mime_type=media_file.mime_type,
            width=None,
            height=None,
        )

    def _localized(self, record: object, field_name: str) -> str | None:
        if self.locale != DEFAULT_PUBLIC_LOCALE:
            localized_value = getattr(record, f'{field_name}_{self.locale}', None)
            if isinstance(localized_value, str):
                localized_value = localized_value.strip()
            if localized_value not in (None, ''):
                return localized_value
        return getattr(record, field_name, None)

    def _copy(self, key: str) -> str:
        return _PUBLIC_COPY[self.locale].get(key, _PUBLIC_COPY[DEFAULT_PUBLIC_LOCALE][key])

    def _localized_years_label(self, years: int) -> str:
        return f'{years}{self._copy("years_suffix")}'
