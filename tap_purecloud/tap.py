"""purecloud tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_purecloud import streams


class Tappurecloud(Tap):
    """purecloud tap class."""

    name = "tap-purecloud"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "start_date",
            th.DateTimeType,
            required=True,
            description="The earliest record date to sync",
        ),
        th.Property(
            "end_date",
            th.DateTimeType,
            required=True,
            description="The latest record date to sync",
        ),
        th.Property(
            "domain",
            th.StringType,
            required=True,
            description="The domain used to construct the url for the API service",
        ),
        th.Property(
            "client_id",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The token to authenticate against the API service",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.purecloudStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.ConversationStream(self),
            streams.ConversationParticipantStream(self),
            streams.ConversationParticipantSessionStream(self),
            streams.ConversationParticipantSessionMetricStream(self),
            streams.ConversationParticipantSessionSegmentStream(self),
            streams.GroupStream(self),
            streams.GroupImageStream(self),
            streams.GroupOwnerStream(self),
            streams.LanguageStream(self),
            streams.LocationStream(self),
            streams.PresenceStream(self),
            streams.QueueStream(self),
            streams.QueueDivisionStream(self),
            streams.QueueMembershipStream(self),
            streams.QueueWrapUpCodeStream(self),
            streams.UserStream(self),
            streams.UserDivisionStream(self),
            streams.UserLanguageStream(self),
            streams.UserLocationStream(self),
            streams.UserPresenceStream(self),
            streams.UserSkillStream(self),
            streams.SkillStream(self),
        ]


if __name__ == "__main__":
    Tappurecloud.cli()
