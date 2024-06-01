from enum import Enum


class SubmissionState(Enum):
    NOT_ENTERED = "Not Entered"
    ENTERED = "Entered"
    SUBMITTED = "Submitted"
    PENDING_FEEDBACK = "Pending Feedback"
    COMPLETE = "Complete"
