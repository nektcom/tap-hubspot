from __future__ import annotations

from tap_hubspot.client import DynamicIncrementalHubspotStream


class FeedbackSubmissionsStream(DynamicIncrementalHubspotStream):
    """
    https://developers.hubspot.com/docs/api/crm/feedback-submissions

    Feedback Submissions is a read-only CRM object (NPS/CSAT/CES/custom survey
    responses). Requires the `crm.objects.feedback_submissions.read` scope;
    accounts without it are skipped at discovery by `_safe_streams`.
    """

    name = "feedback_submissions"
    path = "/objects/feedback_submissions"
    incremental_path = "/objects/feedback_submissions/search"
    primary_keys = ["id"]
    replication_key = "hs_lastmodifieddate"
    records_jsonpath = "$[results][*]"

    @property
    def url_base(self) -> str:
        return "https://api.hubapi.com/crm/v3"
