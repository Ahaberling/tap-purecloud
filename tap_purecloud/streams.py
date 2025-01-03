"""Stream type classes for tap-purecloud."""

from __future__ import annotations

import sys
import typing as t
import datetime
from flatten_json import flatten

import logging
#from loguru import logger as logger_guru

from PureCloudPlatformClientV2 import (
    UsersApi, UserDetailsQuery, GroupsApi,
    AnalyticsApi, QueueObservationQuery, UserAggregationQuery,
    LocationsApi, LocationSearchRequest, PresenceApi,
    RoutingApi, WorkforceManagementApi, WfmHistoricalAdherenceQuery,
    UserListScheduleRequestBody, ConversationsApi, ConversationQuery,
    PagingSpec
)

from tap_purecloud.client import EnrichedPurecloudStream
import tap_purecloud.schemas as schemas

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

#logger_guru.configure(
#    handlers=[
#        dict(sink="LOGURU_DEBUG_STREAM_{time}.log", level='DEBUG', enqueue=True, encoding='utf-8', diagnose=True),
#    ],
#)

# Configuring the logging
logging.basicConfig(level=logging.INFO,  # Adjust the level to control verbosity (DEBUG, INFO, WARNING, etc.)
                    format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

class ConversationStream(EnrichedPurecloudStream):
    name = "conversation"
    primary_keys: t.ClassVar[list[str]] = ["conversation_id"]
    replication_key = None
    schema = schemas.conversation

    body = ConversationQuery()
    body.order = "asc"
    body.orderBy = "conversationStart"
    body.paging = PagingSpec()
    body.paging.page_size = 100      # cant be greater than 100
    body.paging.page_number = 1

    load_config = {
        "query_body": body,
        "parent_id_name": "",
        "page_size": "",
        "page_start": "",
        "api_function_params": ""
    }

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        records = []

        start_date = self.config['start_date']
        end_date = self.config['end_date']

        # Convert strings to datetime objects
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

        next_date = start_date

        while next_date <= end_date:
            
            current_end_date = min(next_date + datetime.timedelta(days=7), end_date)

            # Format the dates in the required ISO 8601 format with zero time and milliseconds
            next_date_str = next_date.strftime('%Y-%m-%dT00:00:00.000Z')
            current_end_date_str = current_end_date.strftime('%Y-%m-%dT00:00:00.000Z')

            # Combining to form interval
            interval = f"{next_date_str}/{current_end_date_str}"
            interval_logging = f'{next_date.strftime("%Y-%m-%d")} // {current_end_date.strftime("%Y-%m-%d")}'

            self.load_config["query_body"].interval = interval

            interval_record = self.purecloud_api_wrapper_paged(
                api_class=ConversationsApi,
                method_name="post_analytics_conversations_details_query",
                entity_attr="conversations",
                load_config=self.load_config
            )

            logger.info(f"Processing Conversations for interval {interval_logging}")
            c = 0
            for record in interval_record:
                records.append(record.copy())
                c = c + 1
                if c % 1000 == 0:
                    logger.info(f"Processed first \t {c} records in interval {interval_logging}")
            logger.info(f"Processed all \t {c} records in interval {interval_logging}")

            next_date = current_end_date + datetime.timedelta(days=7)

        return records

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""

        return {
            "conversation_id": record.get("conversation_id", ""),
            "participants": record.get("participants", {}),
        }


class ConversationParticipantStream(EnrichedPurecloudStream):
    name = "conversation_participant"
    primary_keys: t.ClassVar[list[str]] = ["conversation_id", "participant_id"]
    replication_key = None
    schema = schemas.conversation_participant

    parent_stream_type = ConversationStream
    ignore_parent_replication_keys = True

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        return self.post_processing_and_str_casting(id_columns=['conversation_id'], context_column='participants', context=context)

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "conversation_id": record.get("conversation_id", ""),
            "participant_id": record.get("participant_id", ""),
            "sessions": record.get("sessions", {}),
        }


class ConversationParticipantSessionStream(EnrichedPurecloudStream):
    name = "conversation_participant_session"
    primary_keys: t.ClassVar[list[str]] = ["conversation_id", "session_id"]
    replication_key = None
    schema = schemas.conversation_participant_session

    parent_stream_type = ConversationParticipantStream
    ignore_parent_replication_keys = True

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        return self.post_processing_and_str_casting(id_columns=['conversation_id', 'participant_id'], context_column='sessions', context=context)

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "conversation_id": record.get("conversation_id", ""),
            "participant_id": record.get("participant_id", ""),
            "session_id": record.get("session_id", ""),
            "metrics": record.get("metrics", {}),
            "segments": record.get("segments", {}),
        }

class ConversationParticipantSessionMetricStream(EnrichedPurecloudStream):
    name = "conversation_participant_session_metric"
    primary_keys: t.ClassVar[list[str]] = ["conversation_id", "session_id", "emit_date", "name"]
    replication_key = None
    schema = schemas.conversation_participant_session_metric

    parent_stream_type = ConversationParticipantSessionStream
    ignore_parent_replication_keys = True

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        return self.post_processing_and_str_casting(id_columns=['conversation_id', 'participant_id', 'session_id'], context_column='metrics', context=context)

class ConversationParticipantSessionSegmentStream(EnrichedPurecloudStream):
    name = "conversation_participant_session_segment"
    primary_keys: t.ClassVar[list[str]] = ["conversation_id", "session_id", "segment_type", "segment_start"]
    replication_key = None
    schema = schemas.conversation_participant_session_segment

    parent_stream_type = ConversationParticipantSessionStream
    ignore_parent_replication_keys = True

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        return self.post_processing_and_str_casting(id_columns=['conversation_id', 'participant_id', 'session_id'], context_column='segments', context=context)

class GroupStream(EnrichedPurecloudStream):
    name = "groups"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema = schemas.group

    load_config = {
        "query_body": "",
        "parent_id_name": "",
        "page_size": "100",
        "page_start": "1",
        "api_function_params": ""
    }

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        records = self.purecloud_api_wrapper_paged(
            api_class=GroupsApi,
            method_name="get_groups",
            entity_attr="entities",
            load_config=self.load_config,
            context=context
        )
        return records

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "group_id": record.get("id", ""),
            "images": record.get("images", {}),
            "owners": record.get("owners", {}),
        }


class GroupImageStream(EnrichedPurecloudStream):
    name = "group_image"
    primary_keys: t.ClassVar[list[str]] = ["group_id", "image_uri"]
    replication_key = None
    schema = schemas.group_image

    parent_stream_type = GroupStream
    ignore_parent_replication_keys = True

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        return self.post_processing_and_str_casting(id_columns=['group_id'], context_column='images', context=context)


class GroupOwnerStream(EnrichedPurecloudStream):
    name = "group_owner"
    primary_keys: t.ClassVar[list[str]] = ["group_id","id"]
    replication_key = None
    schema = schemas.group_owner

    parent_stream_type = GroupStream
    ignore_parent_replication_keys = True

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        return self.post_processing_and_str_casting(id_columns=['group_id'], context_column='owners', context=context)


class LanguageStream(EnrichedPurecloudStream):
    name = "languages"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema = schemas.language

    load_config = {
        "query_body": "",
        "parent_id_name": "",
        "page_size": "100",
        "page_start": "1",
        "api_function_params": ""
    }

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        records = self.purecloud_api_wrapper_paged(
            api_class=RoutingApi,
            method_name="get_routing_languages",
            entity_attr="entities",
            context=context,
            load_config=self.load_config,
        )
        return records

class LocationStream(EnrichedPurecloudStream):
    name = "locations"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema = schemas.location

    body = LocationSearchRequest()
    body.page_size = 100      # cant be greater than 100
    body.page_number = 1

    load_config = {
        "query_body": body,
        "parent_id_name": "",
        "page_size": "",
        "page_start": "",
        "api_function_params": ""
    }

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        records = self.purecloud_api_wrapper_paged(
            api_class=LocationsApi,
            method_name="post_locations_search",
            entity_attr="results",
            load_config=self.load_config,
        )
        return records


class PresenceStream(EnrichedPurecloudStream):
    name = "presences"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema = schemas.presence

    load_config = {
        "query_body": "",
        "parent_id_name": "",
        "page_size": "100",
        "page_start": "1",
        "api_function_params": ""
    }

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        records = self.purecloud_api_wrapper_paged(
            api_class=PresenceApi,
            method_name="get_presencedefinitions",
            entity_attr="entities",
            load_config=self.load_config,
        )
        return records

class QueueStream(EnrichedPurecloudStream):
    name = "queues"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema = schemas.queue

    load_config = {
        "query_body": "",
        "parent_id_name": "",
        "page_size": "100",
        "page_start": "1",
        "api_function_params": ""
    }

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        records = self.purecloud_api_wrapper_paged(
            api_class=RoutingApi,
            method_name="get_routing_queues",
            entity_attr="entities",
            load_config=self.load_config,
        )
        return records

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "queue_id": record.get("id", ""),
            "division": record.get("division", {})
        }


class QueueDivisionStream(EnrichedPurecloudStream):
    name = "queue_division"
    primary_keys: t.ClassVar[list[str]] = ["queue_id", "id"]
    replication_key = None
    schema = schemas.queue_division

    parent_stream_type = QueueStream
    ignore_parent_replication_keys = True

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        return self.post_processing_and_str_casting(id_columns=['queue_id'], context_column='division', context=context)


class QueueMembershipStream(EnrichedPurecloudStream):
    name = "queue_membership"
    primary_keys: t.ClassVar[list[str]] = ["queue_id", "id"]
    replication_key = None
    schema = schemas.queue_membership

    load_config = {
        "query_body": "",
        "parent_id_name": "queue_id",
        "page_size": "100",
        "page_start": "1",
        "api_function_params": ""
    }

    parent_stream_type = QueueStream
    ignore_parent_replication_keys = True

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        records = self.purecloud_api_wrapper_paged(
            api_class=RoutingApi,
            method_name="get_routing_queue_users",
            entity_attr="entities",
            load_config=self.load_config,
            context=context
        )
        return records


class QueueWrapUpCodeStream(EnrichedPurecloudStream):
    name = "queue_wrapup_code"
    primary_keys: t.ClassVar[list[str]] = ["queue_id", "id"]
    replication_key = None
    schema = schemas.queue_wrapup_code

    load_config = {
        "query_body": "",
        "parent_id_name": "queue_id",
        "page_size": "100",
        "page_start": "1",
        "api_function_params": ""
    }

    parent_stream_type = QueueStream
    ignore_parent_replication_keys = True

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        records = self.purecloud_api_wrapper_paged(
            api_class=RoutingApi,
            method_name="get_routing_queue_wrapupcodes",
            entity_attr="entities",
            load_config=self.load_config,
            context=context
        )
        return records



class UserStream(EnrichedPurecloudStream):
    name = "users"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema = schemas.user

    load_config = {
        "query_body": "",
        "parent_id_name": "",
        "page_size": "100",
        "page_start": "1",
        "api_function_params": {'expand': ['locations']}
    }

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        records = self.purecloud_api_wrapper_paged(
            api_class=UsersApi,
            method_name="get_users",
            entity_attr="entities",
            #api_function_params={'expand': ['locations']},
            load_config=self.load_config,
            context=context
        )
        return records

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "user_id": record.get("id", ""),
            "division": record.get("division", {}),
            "locations": record.get("locations", {}),
        }


class UserDivisionStream(EnrichedPurecloudStream):
    name = "users_division"
    primary_keys: t.ClassVar[list[str]] = ["user_id", "id"]
    replication_key = None
    schema = schemas.user_division

    parent_stream_type = UserStream
    ignore_parent_replication_keys = True

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
       return self.post_processing_and_str_casting(id_columns=['user_id'], context_column='division', context=context)


class UserLanguageStream(EnrichedPurecloudStream):
    name = "users_language"
    primary_keys: t.ClassVar[list[str]] = ["user_id", "id"]
    replication_key = None
    schema = schemas.user_language

    load_config = {
        "query_body": "",
        "parent_id_name": "user_id",
        "page_size": "100",
        "page_start": "1",
        "api_function_params": ""
    }

    parent_stream_type = UserStream
    ignore_parent_replication_keys = True

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        records = self.purecloud_api_wrapper_paged(
            api_class=UsersApi,
            method_name="get_user_routinglanguages",
            entity_attr="entities",
            load_config=self.load_config,
            context=context
        )
        return records


class UserLocationStream(EnrichedPurecloudStream):
    name = "users_location"
    primary_keys: t.ClassVar[list[str]] = ["user_id", "location_definition_id"]
    replication_key = None
    schema = schemas.user_location

    parent_stream_type = UserStream
    ignore_parent_replication_keys = True

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        records = []

        # locations are always expected as list of dicts
        if isinstance(context['locations'], list):
            for location in context['locations']:
                record = {}
                record_helper = {'user_id': context['user_id']}

                record_helper.update(location)
                record_helper = flatten(record_helper)
                for column in record_helper:
                    if record_helper[column]:
                        record[column] = str(record_helper[column])
                    else:
                        record[column] = None
                records.append(record)

        # just in case
        elif isinstance(context['locations'], dict):
            record = {}
            record_helper = {'user_id': context['user_id']}

            record_helper.update(context['locations'])
            record_helper = flatten(record_helper)
            for column in record_helper:
                if record_helper[column]:
                    record[column] = str(record_helper[column])
                else:
                    record[column] = None
            records.append(record)

        return records


class UserPresenceStream(EnrichedPurecloudStream):
    name = "users_presence"
    primary_keys: t.ClassVar[list[str]] = ["user_id", "qualifier", "date"]
    replication_key = None
    schema = schemas.user_presence

    parent_stream_type = UserStream
    ignore_parent_replication_keys = True

    body = UserAggregationQuery()
    body.metrics = ["tSystemPresence"]

    load_config = {
        "query_body": body,
        "parent_id_name": "",
        "page_size": "",
        "page_start": "",
        "api_function_params": ""
    }

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:

        ### preparing config of query ###
        start_date = self.config['start_date']
        end_date = self.config['end_date']

        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        incr = datetime.timedelta(days=1)

        post_processed_records = []
        loop_date = start_date

        # Granularity behaves unexpected. It is not supported by his code right now.
        # In future, working on this might enhance performance
        while loop_date < end_date:
            self.load_config["query_body"].interval = f"{loop_date}/{loop_date + incr}"
            self.load_config["query_body"].filter = {
                "type": "and",
                "predicates": [
                    {
                        "type": "dimension",
                        "dimension": "userId",
                        "operator": "matches",
                        "value": f"{context['user_id']}"
                    }
                ]
            }

            ### requesting ###
            records = self.purecloud_api_wrapper_paged(
                api_class=AnalyticsApi,
                method_name="post_analytics_users_aggregates_query",
                entity_attr="results",
                #query_body= self.body
                load_config=self.load_config
            )

            ### post processing ###
            for record in records:
                for record_data in record['data']:
                    metrics = record_data['metrics']

                    for metric in metrics:
                        metric = flatten(metric)
                        metric['date'] = loop_date.strftime('%Y-%m-%d')

                        processed_metric = {}
                        for key, value in metric.items():
                            if not value == None and value != {}:
                                if isinstance(value, (dict, list)):
                                    processed_metric[key] = value
                                else:
                                    processed_metric[key] = str(value)
                            else:
                                processed_metric[key] = None

                        post_processed_records.append(processed_metric)
            loop_date = loop_date + incr

        return post_processed_records


class UserSkillStream(EnrichedPurecloudStream):
    name = "users_skill"
    primary_keys: t.ClassVar[list[str]] = ["user_id", "id"]
    replication_key = None
    schema = schemas.user_skill

    load_config = {
        "query_body": "",
        "parent_id_name": "user_id",
        "page_size": "100",
        "page_start": "1",
        "api_function_params": ""
    }

    parent_stream_type = UserStream
    ignore_parent_replication_keys = True

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:

        records = self.purecloud_api_wrapper_paged(
            api_class=UsersApi,
            method_name="get_user_routingskills",
            entity_attr="entities",
            load_config=self.load_config,
            context=context
        )
        return records


class SkillStream(EnrichedPurecloudStream):
    name = "skills"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = None
    schema = schemas.skills

    load_config = {
        "query_body": "",
        "parent_id_name": "",
        "page_size": "100",
        "page_start": "1",
        "api_function_params": ""
    }

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        records = self.purecloud_api_wrapper_paged(
            api_class=RoutingApi,
            method_name="get_routing_skills",
            entity_attr="entities",
            load_config=self.load_config,
            context=context
        )
        return records
