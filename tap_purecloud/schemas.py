from singer_sdk import typing as th  # JSON Schema typing helpers


conversation = th.PropertiesList(
        th.Property("conversation_end", th.StringType),
        th.Property("conversation_id", th.StringType),
        th.Property("conversation_initiator", th.StringType),
        th.Property("conversation_start", th.StringType),
        th.Property("customer_participation", th.StringType),
        th.Property("external_tag", th.StringType),
        th.Property("knowledge_base_ids", th.StringType),
        th.Property("media_stats_min_conversation_mos", th.StringType),
        th.Property("media_stats_min_conversation_r_factor", th.StringType),
        th.Property("originating_direction", th.StringType),
        th.Property("self_served", th.StringType),
        th.Property("evaluations", th.StringType),
        th.Property("surveys", th.StringType),
    ).to_dict()

conversation_participant = th.PropertiesList(
        th.Property("external_contact_id", th.StringType),
        th.Property("external_organization_id", th.StringType),
        th.Property("flagged_reason", th.StringType),
        th.Property("participant_id", th.StringType),
        th.Property("participant_name", th.StringType),
        th.Property("purpose", th.StringType),
        th.Property("team_id", th.StringType),
        th.Property("user_id", th.StringType),
        th.Property("conversation_id", th.StringType),
    ).to_dict()

conversation_participant_session = th.PropertiesList(
        th.Property("acw_skipped", th.StringType),
        th.Property("address_from", th.StringType),
        th.Property("address_other", th.StringType),
        th.Property("address_self", th.StringType),
        th.Property("address_to", th.StringType),
        th.Property("agent_assistant_id", th.StringType),
        th.Property("agent_bullseye_ring", th.StringType),
        th.Property("agent_owned", th.StringType),
        th.Property("ani", th.StringType),
        th.Property("assigner_id", th.StringType),
        th.Property("authenticated", th.StringType),
        th.Property("callback_scheduled_time", th.StringType),
        th.Property("callback_user_name", th.StringType),
        th.Property("coached_participant_id", th.StringType),
        th.Property("cobrowse_role", th.StringType),
        th.Property("cobrowse_room_id", th.StringType),
        th.Property("delivery_status", th.StringType),
        th.Property("delivery_status_change_date", th.StringType),
        th.Property("direction", th.StringType),
        th.Property("disposition_analyzer", th.StringType),
        th.Property("disposition_name", th.StringType),
        th.Property("dnis", th.StringType),
        th.Property("edge_id", th.StringType),
        th.Property("eligible_agent_counts", th.StringType),
        th.Property("extended_delivery_status", th.StringType),
        th.Property("flow_in_type", th.StringType),
        th.Property("flow_out_type", th.StringType),
        th.Property("journey_action_id", th.StringType),
        th.Property("journey_action_map_id", th.StringType),
        th.Property("journey_action_map_version", th.StringType),
        th.Property("journey_customer_id", th.StringType),
        th.Property("journey_customer_id_type", th.StringType),
        th.Property("journey_customer_session_id", th.StringType),
        th.Property("journey_customer_session_id_type", th.StringType),
        th.Property("media_bridge_id", th.StringType),
        th.Property("media_count", th.StringType),
        th.Property("media_type", th.StringType),
        th.Property("message_type", th.StringType),
        th.Property("monitored_participant_id", th.StringType),
        th.Property("outbound_campaign_id", th.StringType),
        th.Property("outbound_contact_id", th.StringType),
        th.Property("outbound_contact_list_id", th.StringType),
        th.Property("peer_id", th.StringType),
        th.Property("protocol_call_id", th.StringType),
        th.Property("provider", th.StringType),
        th.Property("recording", th.StringType),
        th.Property("remote", th.StringType),
        th.Property("remote_name_displayable", th.StringType),
        th.Property("room_id", th.StringType),
        th.Property("routing_ring", th.StringType),
        th.Property("screen_share_address_self", th.StringType),
        th.Property("screen_share_room_id", th.StringType),
        th.Property("script_id", th.StringType),
        th.Property("selected_agent_id", th.StringType),
        th.Property("selected_agent_rank", th.StringType),
        th.Property("session_dnis", th.StringType),
        th.Property("session_id", th.StringType),
        th.Property("sharing_screen", th.StringType),
        th.Property("skip_enabled", th.StringType),
        th.Property("timeout_seconds", th.StringType),
        th.Property("used_routing", th.StringType),
        th.Property("video_address_self", th.StringType),
        th.Property("video_room_id", th.StringType),
        th.Property("waiting_interaction_counts", th.StringType),
        th.Property("proposed_agents", th.StringType),
        th.Property("agent_groups", th.StringType),
        th.Property("conversation_id", th.StringType),
        th.Property("participant_id", th.StringType),
    ).to_dict()

conversation_participant_session_segment = th.PropertiesList(
        th.Property("audio_muted", th.StringType),
        th.Property("conference", th.StringType),
        th.Property("destination_conversation_id", th.StringType),
        th.Property("destination_session_id", th.StringType),
        th.Property("disconnect_type", th.StringType),
        th.Property("error_code", th.StringType),
        th.Property("group_id", th.StringType),
        th.Property("queue_id", th.StringType),
        th.Property("requested_language_id", th.StringType),
        th.Property("segment_end", th.StringType),
        th.Property("segment_start", th.StringType),
        th.Property("segment_type", th.StringType),
        th.Property("source_conversation_id", th.StringType),
        th.Property("source_session_id", th.StringType),
        th.Property("subject", th.StringType),
        th.Property("video_muted", th.StringType),
        th.Property("wrap_up_code", th.StringType),
        th.Property("wrap_up_note", th.StringType),
        th.Property("wrap_up_tags", th.StringType),
        th.Property("scored_agents", th.StringType),
        th.Property("properties", th.StringType),
        th.Property("conversation_id", th.StringType),
        th.Property("participant_id", th.StringType),
        th.Property("session_id", th.StringType),
    ).to_dict()

conversation_participant_session_metric = th.PropertiesList(
        th.Property("emit_date", th.StringType),
        th.Property("name", th.StringType),
        th.Property("value", th.StringType),
        th.Property("conversation_id", th.StringType),
        th.Property("participant_id", th.StringType),
        th.Property("session_id", th.StringType),
    ).to_dict()

group = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("date_modified", th.StringType),
        th.Property("member_count", th.StringType),
        th.Property("state", th.StringType),
        th.Property("version", th.StringType),
        th.Property("type", th.StringType),
        th.Property("rules_visible", th.StringType),
        th.Property("visibility", th.StringType),
        th.Property("self_uri", th.StringType)
    ).to_dict()

group_image = th.PropertiesList(
        th.Property("resolution", th.StringType),
        th.Property("image_uri", th.StringType),
        th.Property("group_id", th.StringType),
    ).to_dict()

group_owner = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("division", th.StringType),
        th.Property("chat", th.StringType),
        th.Property("department", th.StringType),
        th.Property("email", th.StringType),
        th.Property("primary_contact_info", th.StringType),
        th.Property("addresses", th.StringType),
        th.Property("state", th.StringType),
        th.Property("title", th.StringType),
        th.Property("username", th.StringType),
        th.Property("manager", th.StringType),
        th.Property("images", th.StringType),
        th.Property("version", th.StringType),
        th.Property("certifications", th.StringType),
        th.Property("biography", th.StringType),
        th.Property("employer_info", th.StringType),
        th.Property("routing_status", th.StringType),
        th.Property("presence", th.StringType),
        th.Property("integration_presence", th.StringType),
        th.Property("conversation_summary", th.StringType),
        th.Property("out_of_office", th.StringType),
        th.Property("geolocation", th.StringType),
        th.Property("station", th.StringType),
        th.Property("authorization", th.StringType),
        th.Property("profile_skills", th.StringType),
        th.Property("locations", th.StringType),
        th.Property("groups", th.StringType),
        th.Property("team", th.StringType),
        th.Property("skills", th.StringType),
        th.Property("languages", th.StringType),
        th.Property("acd_auto_answer", th.StringType),
        th.Property("language_preference", th.StringType),
        th.Property("last_token_issued", th.StringType),
        th.Property("date_last_login", th.StringType),
        th.Property("self_uri", th.StringType),
        th.Property("group_id", th.StringType),
    ).to_dict()

language = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("date_modified", th.StringType),
        th.Property("state", th.StringType),
        th.Property("version", th.StringType),
        th.Property("self_uri", th.StringType),
    ).to_dict()

location = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("state", th.StringType),
        th.Property("notes", th.StringType),
        th.Property("version", th.StringType),
        th.Property("path", th.StringType),
        th.Property("profile_image", th.StringType),
        th.Property("floorplan_image", th.StringType),
        th.Property("address_verification_details", th.StringType),
        th.Property("address_verified", th.StringType),
        th.Property("address_stored", th.StringType),
        th.Property("images", th.StringType),
        th.Property("self_uri", th.StringType),
    ).to_dict()

presence = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("system_presence", th.StringType),
        th.Property("deactivated", th.StringType),
        th.Property("primary", th.StringType),
        th.Property("created_date", th.StringType),
        th.Property("modified_date", th.StringType),
        th.Property("self_uri", th.StringType),
    ).to_dict()

queue = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("date_created", th.StringType),
        th.Property("date_modified", th.StringType),
        th.Property("modified_by", th.StringType),
        th.Property("created_by", th.StringType),
        th.Property("member_count", th.StringType),
        th.Property("user_member_count", th.StringType),
        th.Property("joined_member_count", th.StringType),
        th.Property("routing_rules", th.StringType),
        th.Property("skill_evaluation_method", th.StringType),
        th.Property("member_groups", th.StringType),
        th.Property("email_in_queue_flow", th.StringType),
        th.Property("message_in_queue_flow", th.StringType),
        th.Property("whisper_prompt", th.StringType),
        th.Property("on_hold_prompt", th.StringType),
        th.Property("auto_answer_only", th.StringType),
        th.Property("enable_transcription", th.StringType),
        th.Property("calling_party_name", th.StringType),
        th.Property("enable_manual_assignment", th.StringType),
        th.Property("calling_party_number", th.StringType),
        #th.Property("default_scripts", th.StringType), #Neither supported nor needed yet
        th.Property("outbound_messaging_addresses", th.StringType),
        th.Property("outbound_email_address", th.StringType),
        th.Property("peer_id", th.StringType),
        th.Property("self_uri", th.StringType),
    ).to_dict()

queue_division = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("self_uri", th.StringType),
        th.Property("queue_id", th.StringType),
    ).to_dict()

queue_membership = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("ring_number", th.StringType),
        th.Property("joined", th.StringType),
        th.Property("member_by", th.StringType),
        th.Property("routing_status", th.StringType),
        th.Property("self_uri", th.StringType),
        #th.Property("user_id", th.StringType), #Neither supported nor needed yet (hacky coded in the previously used
                                                #official meltano tap
        th.Property("queue_id", th.StringType),
    ).to_dict()

queue_wrapup_code = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("date_created", th.StringType),
        th.Property("date_modified", th.StringType),
        th.Property("modified_by", th.StringType),
        th.Property("created_by", th.StringType),
        th.Property("self_uri", th.StringType),
        th.Property("queue_id", th.StringType),
    ).to_dict()

user = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("email", th.StringType),
        th.Property("state", th.StringType),
        th.Property("title", th.StringType),
        th.Property("username", th.StringType),
        th.Property("version", th.StringType),
        th.Property("certifications", th.StringType),
        th.Property("biography", th.StringType),
        th.Property("employer_info", th.StringType),
        th.Property("routing_status", th.StringType),
        th.Property("presence", th.StringType),
        th.Property("integration_presence", th.StringType),
        th.Property("conversation_summary", th.StringType),
        th.Property("out_of_office", th.StringType),
        th.Property("geolocation", th.StringType),
        th.Property("station", th.StringType),
        th.Property("authorization", th.StringType),
        th.Property("profile_skills", th.StringType),
        th.Property("groups", th.StringType),
        th.Property("team", th.StringType),
        th.Property("skills", th.StringType),
        th.Property("languages", th.StringType),
        th.Property("acd_auto_answer", th.StringType),
        th.Property("language_preference", th.StringType),
        th.Property("last_token_issued", th.StringType),
        th.Property("date_last_login", th.StringType),
        th.Property("self_uri", th.StringType),
    ).to_dict()

user_division = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("self_uri", th.StringType),
        th.Property("user_id", th.StringType),
    ).to_dict()

user_language = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("proficiency", th.StringType),
        th.Property("state", th.StringType),
        th.Property("language_uri", th.StringType),
        th.Property("self_uri", th.StringType),
        th.Property("user_id", th.StringType),
    ).to_dict()

user_location = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("floorplan_id", th.StringType),
        th.Property("coordinates", th.StringType),
        th.Property("notes", th.StringType),
        th.Property("location_definition_id", th.StringType),
        th.Property("location_definition_name", th.StringType),
        th.Property("location_definition_contact_user", th.StringType),
        th.Property("location_definition_emergency_number", th.StringType),
        th.Property("location_definition_address", th.StringType),
        th.Property("location_definition_state", th.StringType),
        th.Property("location_definition_notes", th.StringType),
        th.Property("location_definition_version", th.StringType),
        th.Property("location_definition_path", th.StringType),
        th.Property("location_definition_profile_image", th.StringType),
        th.Property("location_definition_floorplan_image", th.StringType),
        th.Property("location_definition_address_verification_details", th.StringType),
        th.Property("location_definition_address_verified", th.StringType),
        th.Property("location_definition_address_stored", th.StringType),
        th.Property("location_definition_images", th.StringType),
        th.Property("location_definition_self_uri", th.StringType),
        th.Property("user_id", th.StringType),
    ).to_dict()

user_presence = th.PropertiesList(
        th.Property("metric", th.StringType),
        th.Property("qualifier", th.StringType),
        th.Property("stats_max", th.StringType),
        th.Property("stats_min", th.StringType),
        th.Property("stats_count", th.StringType),
        th.Property("stats_count_negative", th.StringType),
        th.Property("stats_count_positive", th.StringType),
        th.Property("stats_sum", th.StringType),
        th.Property("stats_current", th.StringType),
        th.Property("stats_ratio", th.StringType),
        th.Property("stats_numerator", th.StringType),
        th.Property("stats_denominator", th.StringType),
        th.Property("stats_target", th.StringType),
        th.Property("user_id", th.StringType),
        th.Property("date", th.StringType),
    ).to_dict()

user_skill = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("proficiency", th.StringType),
        th.Property("state", th.StringType),
        th.Property("skill_uri", th.StringType),
        th.Property("self_uri", th.StringType),
        th.Property("user_id", th.StringType),
    ).to_dict()

skills = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("date_modified", th.StringType),
        th.Property("state", th.StringType),
        th.Property("version", th.StringType),
        th.Property("self_uri", th.StringType),
    ).to_dict()
