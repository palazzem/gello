# -*- coding: utf-8 -*-

#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""pull_request_service.py

Service-helpers for creating and mutating pull_request data.
"""

from . import CRUDService
from .. import db
from ..models import PullRequest


class PullRequestService(CRUDService):
    """CRUD persistent storage service.

    A class with the single responsibility of creating/mutating PullRequest
    data.
    """

    def create(self, name, url, github_pull_request_id, repo_id,
               trello_board_id, trello_card_id, trello_card_url, trello_list_id):
        """Creates and persists a new pull_request record to the database.

        Args:
            name (str): The name of the GitHub pull request.
            url (str): The GitHub url of the pull request.
            github_pull request_id (int): The id of the GitHub pull request.
            repo_id (int): The id of the GitHub repo corresponding to the
                pull request.
            trello_board_id (str): The id of the board the card corresponding
                to the pull request was created on.
            trello_card_id (str): The id of the card created corresponding to
                the isuse.
            trello_card_url (str): The url for the created card corresponding
                to the pull request.
            trello_list_id (str): The id for the list the card corresponding
                to the issue was created on.

        Returns:
            None
        """
        pull_request = PullRequest(
            name=name,
            url=url,
            github_pull_request_id=github_pull_request_id,
            repo_id=repo_id,
            trello_board_id=trello_board_id,
            trello_card_id=trello_card_id,
            trello_card_url=trello_card_url,
            trello_list_id=trello_list_id
        )
        db.session.add(pull_request)

        # Persists the pull_request
        db.session.commit()

    def update(self, github_pull_request_id, name):
        """Updates a persisted pull_request.

        Args:
            github_pull_request_id (int): The id of the GitHub pull request.
            name (str): The updated name of the GitHub pull request.

        Returns:
            None
        """
        pull_request = PullRequest.query.filter_by(
            github_pull_request_id=github_pull_request_id
        ).first()
        pull_request.name = name
        db.session.commit()

    def delete(self, github_pull_request_id):
        """Deletes an old, persisted pull_request.

        Args:
            github_pull_request_id (int): The id of the GitHub pull request.

        Returns:
            None
        """
        PullRequest.query.filter_by(
               github_pull_request_id=github_pull_request_id).delete()
        db.session.commit()
