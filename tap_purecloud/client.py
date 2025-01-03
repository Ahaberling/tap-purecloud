"""REST client handling, including purecloudStream base class."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, Iterable

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator  # noqa: TCH002
from singer_sdk.streams import RESTStream

from PureCloudPlatformClientV2.api_client import ApiClient

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

if TYPE_CHECKING:
    import requests
    from singer_sdk.helpers.types import Auth, Context

#from loguru import logger as logger_guru

#logger_guru.configure(
#    handlers=[
#        dict(sink="LOGURU_DEBUG_STREAM_{time}.log", level='DEBUG', enqueue=True, encoding='utf-8', diagnose=True),
#    ],
#)

class PurecloudStream(RESTStream):
    """purecloud stream class."""

    # Update this value if necessary or override `parse_response`.
    records_jsonpath = "$[*]"

    # Update this value if necessary or override `get_new_paginator`.
    next_page_token_jsonpath = "$.next_page"  # noqa: S105

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        # TODO: hardcode a value here, or retrieve it from self.config
        return f"https://api.{self.config['domain']}.de"

    @property
    def authentification_client(self) -> str:

        api_client = ApiClient(host=self.url_base)
        api_client = api_client.get_client_credentials_token(
            client_id=self.config['client_id'],
            client_secret=self.config['client_secret']
        )
        return api_client

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {}
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_new_paginator(self) -> BaseAPIPaginator:
        """Create a new pagination helper instance.

        If the source API can make use of the `next_page_token_jsonpath`
        attribute, or it contains a `X-Next-Page` header in the response
        then you can remove this method.

        If you need custom pagination that uses page numbers, "next" links, or
        other approaches, please read the guide: https://sdk.meltano.com/en/v0.25.0/guides/pagination-classes.html.

        Returns:
            A pagination helper instance.
        """
        return super().get_new_paginator()

    def get_url_params(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: Any | None,  # noqa: ANN401
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            params["sort"] = "asc"
            params["order_by"] = self.replication_key
        return params

    def prepare_request_payload(
        self,
        context: Context | None,  # noqa: ARG002
        next_page_token: Any | None,  # noqa: ARG002, ANN401
    ) -> dict | None:
        """Prepare the data payload for the REST API request.

        By default, no payload will be sent (return None).

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary with the JSON body for a POST requests.
        """
        # TODO: Delete this method if no payload is required. (Most REST APIs.)
        return None

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        # TODO: Parse response body and return a set of records.
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(
        self,
        row: dict,
        context: Context | None = None,  # noqa: ARG002
    ) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        # TODO: Delete this method if not needed.
        return row



class EnrichedPurecloudStream(PurecloudStream):

    def purecloud_api_wrapper_paged(
            self,
            api_class,
            method_name: str,
            entity_attr: str,
            load_config: Optional[dict] = None,
            context: Optional[dict] = None,
    ) -> Iterable[dict]:

        #preparing arguments for api call
        args = []
        kwargs = {}

        # preparing non-paging args:
        if load_config["parent_id_name"] and not load_config["query_body"]:
            args.append(context[load_config["parent_id_name"]])
        elif not load_config["parent_id_name"] and load_config["query_body"]:
            args.append(load_config["query_body"])
        elif load_config["parent_id_name"] and load_config["query_body"]:
            # todo: inject actual values into error message instead of "..."
            raise Exception(
                'In class EnrichedPurecloudStream(PurecloudStream): \n'
                'In purecloud_api_wrapper_paged(...):'
                'Both "parent_id_name" and "query" are provided. Choose one'
            )

        if load_config["page_size"]:
            kwargs['page_size'] = load_config["page_size"]
        if load_config["page_start"]:
            kwargs['page_number'] = load_config["page_start"]
        if load_config["api_function_params"]:
            kwargs.update(load_config["api_function_params"])

        continue_bool = True
        api_instance = api_class(self.authentification_client)
        method = getattr(api_instance, method_name)

        while continue_bool:
            if args:
                records = method(*args, **kwargs)
            else:
                records = method(**kwargs)

            entities = getattr(records, entity_attr)
            if entities:
                if len(entities) == 0:
                    break
            else:
                break

            processed_record = {}
            for record in entities:
                record_dict = record.to_dict()
                for key, value in record_dict.items():
                    if not value == None and value != {}:
                        if isinstance(value, (dict, list)):
                            processed_record[key] = value
                        else:
                            processed_record[key] = str(value)
                    else:
                        processed_record[key] = None
                yield processed_record

            if len(args) >=1:
                if hasattr(args[0], 'page_number'):
                    args[0].page_number = args[0].page_number + 1
                elif hasattr(args[0], 'paging'):
                    args[0].paging.page_number = args[0].paging.page_number + 1
                else:
                    continue_bool = False
            elif kwargs.get('page_number', None):
                kwargs['page_number'] = str(int(kwargs['page_number']) + 1)
            else:
                continue_bool = False

    def post_processing_and_str_casting(
            self,
            id_columns: list,
            context_column: str,
            context
    ):
        records = []

        if isinstance(context[context_column], list):
            for child_column in context[context_column]:
                record = {}
                for id_column in id_columns:
                    record[id_column] = context[id_column]

                for column in child_column:
                    if not child_column[column] == None:
                        if isinstance(child_column[column], (dict, list)):
                            record[column] = child_column[column]
                        else:
                            record[column] = str(child_column[column])
                    else:
                        record[column] = None

                records.append(record)

        elif isinstance(context[context_column], dict):
            record = {}
            for id_column in id_columns:
                record[id_column] = context[id_column]
            for column in context[context_column]:
                if not context[context_column][column] == None:
                    record[column] = str(context[context_column][column])
                else:
                    record[column] = None
            records.append(record)

        return records