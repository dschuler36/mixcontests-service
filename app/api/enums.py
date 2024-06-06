from enum import Enum


class SubmissionState(Enum):
    # NOT_ENTERED = "Not Entered"
    # ENTERED = "Enter Contest"
    # DOWNLOADED_STEMS = "Download Stems"
    # SUBMITTED = "Submitted"
    # PENDING_FEEDBACK = "Pending Feedback"
    # COMPLETE = "Complete"

    ENTER_CONTEST = "Enter Contest"
    DOWNLOAD_STEMS = "Download Stems"
    SUBMIT_MIX = "Submit Mix"
    GIVE_FEEDBACK = "Give Feedback"
    CHECK_RESULTS = "Check Results"
